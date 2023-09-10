import base64
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.http import Http404, JsonResponse
from django.views import View
from django.shortcuts import render
from chat.common import update_room_last_message, exist_user_in_room, set_room_session,exist_user_in_roomId,exist_room,update_last_seen_message
from chat.models import LastMessage, LastSeenMessage, Message, Room,User

ENC_KEY = "M^b%WX!4tE{NFd%-DcAT6Lj"

class JoinRoom(View):
   
    template_name = "home.html"
    def get(self,request, *args, **kwargs):
        return render(self.request ,self.template_name,{})
    def post(self,request, *args, **kwargs):
        active_room = request.POST.get('room',None)
        username = request.POST.get('username',None)
        if username :
            user = User.objects.filter(name = username).first()
            if user is None:
                ints = User()
                ints.name = username
                ints.save()
                user = ints
            
            if active_room:
                print('User',user.id)
                if exist_user_in_room(user,active_room) is not True:
                    if exist_room(active_room):
                        ints = Room.objects.get(name = active_room)
                        ints.participants.add(user)
                    else:
                        ints = Room()
                        ints.name = active_room
                        ints.save()
                        ints.participants.add(user)
                return redirect(reverse(viewname='chatroom_view',kwargs={'user':user.name}))
        return render(request ,self.template_name,{})


class ChatRoomView(View):
    
    def get(self,request,*args,**kwargs):
        
        context = {}
        user = None
        if 'user' in kwargs:
            user = kwargs['user']
        if user:
            ints = User.objects.get(name=user)
            if ints:
                active_room = request.GET.get('room',None)
                if active_room is not None:
                    context['active_room'] = active_room
                    # room_id = AESRoomEnc(ENC_KEY).decrypt(active_room,ENC_KEY)
                    room_id = active_room
                    if exist_user_in_roomId(ints,room_id):
                        set_room_session(ints,room_id)
                        room_chat = Message.objects.filter(room=room_id).order_by('timestamp')
                        if room_chat:
                            update_last_seen_message(ints,room_id)
                            participents = list(room_chat.values_list('sender_id', flat=True))
                            participentsData = { x['id']:{'profile_image':"chat/static/img/users/user-3.png",'name':x['name']} for x in User.objects.filter(id__in = participents).values('name','id')}
                            roomChat = { x['id']:{'message':x["content"],'time':x['timestamp'],'sender':x['sender_id']} for x in room_chat.values('id','sender_id','timestamp','content')}
                            context['room_participents'] = participentsData
                            context['room_chat'] = roomChat

                rooms = Room.objects.filter(participants=ints.id)
                if rooms:
                    
                    roomIdList = list(rooms.values_list('id', flat=True))
                    
                    msgIdList = list(LastMessage.objects.filter(room__in=roomIdList).values_list('message', flat=True))
                    lastMessages = { x['room_id']:{"time":x['timestamp'],"msg":x['content']} for x in Message.objects.filter(id__in=msgIdList).values('timestamp','content','room_id')}
                    print("lastMessage--------s",lastMessages)
                    lastViewMessage = dict(LastSeenMessage.objects.filter(room_id__in=roomIdList,user_id= ints.id).values_list('room_id','message'))
                    print("lastMessage++++s",lastViewMessage)
                    
                    messages = {}
                    roomIdList = []
                    for e in rooms:
                        # encrtped_id = AESRoomEnc(ENC_KEY).encrypt(str(e.id)).decode('utf-8')
                        encrtped_id = str(e.id)
                        # encrtped_id = encrypt_string(str(e.id)., ENC_KEY)
                        roomIdList.append(encrtped_id)
                        count = ''
                            
                        if e.id in lastViewMessage and lastViewMessage[e.id]:
                            count = Message.objects.filter(room_id = e.id,id__gt = lastViewMessage[e.id]).count()
                        count = count if count != 0 else ''
                        data = {
                            "name": e.name,
                            "message_count" : count,
                        }
                        if e.id in lastMessages:
                            data['last_message'] = lastMessages[e.id]["msg"] if lastMessages[e.id]["msg"] else ''
                            data['message_time'] = lastMessages[e.id]["time"] if lastMessages[e.id]["time"] else ''

                        messages[encrtped_id] = data
                    context['room_id_list'] = roomIdList

                    # pass encrtpted user id and it's key
                    # key = str(int(time.time())) #only string value accepted
                    # user_id = str(request.user.id) if request.user.id else '0'
                    # crypt = AESCipher(key)
                    # encrtped_id = crypt.encrypt(user_id).decode("utf-8")



                    context['room_data'] = messages
                context['user_id'] = ints.name
                    # context['hidden_str'] = key

        return render(request ,'chat_room.html',context)

    def post(self,request,*args,**kwargs):
        render_context = {}
        render_context['context'] = {}
        render_context['return_type'] = 'template_response'
        render_context['template'] = 'chatroom/chatroom.html'
        render_context['redirect_url'] = reverse('chatroom_view',request)
        return render_context

    def put(self,request,*args,**kwargs):
        print('Put-------------',request.body)
        if request.is_ajax():
            room = None
            # room = request.PUT.get('room')
            # try:
            #     data = json.loads(request.body)
            #     room = data.get('room')
            #     # Your logic for handling the PUT request data here
            # except json.JSONDecodeError as e:
            #     print("+++++++++++",e)
            room = request.GET.get('room')
            print('Put-------------',room)
            content_data = {}
            try:
                if room is not None:
                    content_data['active_room'] = room
                    # room_id = AESRoomEnc(ENC_KEY).decrypt(room,ENC_KEY)
                    room_id = room
                    print('Put-------------',room_id)
                    # exist_user_in_room(request,room_id)
                    room_chat = Message.objects.filter(room=room_id).order_by('timestamp')
                    if room_chat:
                        content_data['error'] = False
                        participents = list(room_chat.values_list('sender_id', flat=True))
                        participentsData = { x['id']:{'profile_image':"static/img/user-3.png",'name':x['name']} for x in User.objects.filter(id__in = participents).values('name','id')}
                        roomChat = { x['id']:{'message':x["content"],'time':x['timestamp'],'sender':x['sender_id']} for x in room_chat.values('id','sender_id','timestamp','content')}
                        content_data['room_participents'] = participentsData
                        content_data['room_chat'] = roomChat
                    else:
                        content_data['error'] = True
                return JsonResponse(content_data)
            except Exception as e:
                # Handle the error
                print(e)
                error_message = "An error occurred: " + str(e)
                return JsonResponse({'error': error_message}, status=400)
        return JsonResponse({'error': 'An error occurred:'}, status=400)
            
# class ChatDocumentUpload(View):
    
#     def get(self,request,*args,**kwargs):
#         context = {}
#         # form = ChatRoomDocumentForm()
#         # button =[
# 		# 	{'type':"submit" ,'label':_("Save changes"),'class':"btn btn-brand",},
# 		# ]
#         # form.buttons = button
#         # context['form'] = form
#         document_upload_form
#         return None

# def chat_document_upload_ajax(request,*args,**kwargs):
#     print("request",args,kwargs)

#     content_data = {'error': False, 'message': 'Uploaded Successfully','room':"room"}
#     if request.method == 'POST':
#         form = ChatRoomDocumentForm(request.POST,request.FILES)
#         if form.is_valid():

#             print("Form Valid")
#         else:
#             print("Form Valid",form.errors)
#         print("----",request.user)
#     return JsonResponse(content_data)

class ManageRoom(object):

    def update_last_view_message(request, *args, **kwargs):
        if request.method == 'POST':
            active_room = request.POST.get('room',None) 
            user = request.POST.get('user',None) 
            if active_room is not None:
                # room_id = AESRoomEnc(ENC_KEY).decrypt(active_room,ENC_KEY)
                room_id = active_room
                ints = User.objects.filter(name=user).first()
                if ints:
                    exist_user_in_roomId(ints,room_id)
                    update_last_seen_message(ints,room_id)
                    response_data = {'error': False,'success':True}
                    return JsonResponse(response_data)

        return JsonResponse({'error': 'Invalid request'})

class ManageChat(object):
     
     def insert_message(request, *args, **kwargs):
        if request.method == 'POST':
            active_room = request.POST.get('room',None) 
            message = request.POST.get('message',None)
            user = request.POST.get('user',None)
            ints = None
            if user:
                ints = User.objects.get(name=user)
            if active_room is not None and ints is not None:
                content_data = {'error': False,'success':True}
                content_data['active_room'] = active_room
                # room_id = AESRoomEnc(ENC_KEY).decrypt(active_room,ENC_KEY)
                room_id = active_room

                # exist_room(room_id)
                # exist_user_in_room(request,room_id)

                msgInstance = Message()
                msgInstance.room_id = room_id
                msgInstance.content = message
                msgInstance.sender_id = ints.id
                # msgInstance.timestamp =
                msgInstance.save()

                update_room_last_message(msgInstance.id,room_id)
                update_last_seen_message(ints,room_id)
                # encUid = ENC_KEY.encrypt(str(request.user.id))
                encUid = ints.name
                participentsData = { encUid:{'profile_image':'','name':encUid}}
                roomChat = { msgInstance.id :{'message':msgInstance.content,'time':msgInstance.timestamp,'sender':encUid}}

                content_data['room_participents'] = participentsData
                content_data['room_chat'] = roomChat
                
                return JsonResponse(content_data)

        return JsonResponse({'error': 'Invalid request'})


