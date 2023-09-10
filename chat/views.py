from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.http import Http404, JsonResponse
from django.views import View
from django.shortcuts import render
from chat.common import update_room_last_message, exist_user_in_room, set_room_session,exist_user_in_roomId,exist_room,update_last_seen_message,get_room_chat
from chat.models import LastMessage, LastSeenMessage, Message, Room,User

ENC_KEY = "M^b%WX!4tE{NFd%-DcAT6Lj"

class JoinRoom(View):
   
    template_name = "home.html"
    def get(self,request, *args, **kwargs):
        return render(self.request ,self.template_name,{})
    def post(self,request, *args, **kwargs):
        active_room = request.POST.get('room',None)
        username = request.POST.get('username',None)
        user = User.objects.filter(name = username).first()
        if user is None:
            userInst = User()
            userInst.name = username
            userInst.save()
            user = userInst
        
        if exist_user_in_room(user,active_room) is not True:
            if exist_room(active_room):
                roomInst = Room.objects.get(name = active_room)
                roomInst.participants.add(user)
            else:
                roomInst = Room()
                roomInst.name = active_room
                roomInst.save()
                roomInst.participants.add(user)
                
        return redirect(reverse(viewname='chatroom_view',kwargs={'user':user.name}))


class ChatRoomView(View):
    
    def get(self,request,*args,**kwargs):
        
        context = {}
        user = kwargs.get('user',None)
        active_room = request.GET.get('room',None)
        userInst = User.objects.filter(name=user).first()
        if userInst :
            context['user_id'] = userInst.name
            
            # Get active chat data
            if active_room and exist_user_in_roomId(userInst,active_room):
                context['active_room'] = active_room
                set_room_session(userInst,active_room) #set session
                context.update(get_room_chat(active_room))
                update_last_seen_message(userInst,active_room)
                
            # Get active Roomes
            rooms = Room.objects.filter(participants=userInst.id)
            if rooms:
                roomIdList = list(rooms.values_list('id', flat=True))
                msgIdList = list(LastMessage.objects.filter(room__in=roomIdList).values_list('message', flat=True))
                lastMessages = { x['room_id']:{"time":x['timestamp'],"msg":x['content']} for x in Message.objects.filter(id__in=msgIdList).values('timestamp','content','room_id')}
                lastViewMessage = dict(LastSeenMessage.objects.filter(room_id__in=roomIdList,user_id= userInst.id).values_list('room_id','message'))
                
                messages = {}
                roomIdList = []
                for e in rooms:
                    encrtped_id = str(e.id)
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
                context['room_data'] = messages

        return render(request ,'chat_room.html',context)

    def post(self,request,*args,**kwargs):
        render_context = {}
        render_context['context'] = {}
        render_context['return_type'] = 'template_response'
        render_context['template'] = 'chat_room.html'
        render_context['redirect_url'] = reverse('chatroom_view',request)
        return render_context

    def put(self,request,*args,**kwargs):
        content_data = {}
        if request.is_ajax():
            room_id = request.GET.get('room',None)
            if room_id is not None:
                content_data = get_room_chat(room_id)
                content_data['active_room'] = room_id
        return JsonResponse(content_data)

class ManageRoom(object):

    def update_last_view_message(request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            active_room = request.POST.get('room',None) 
            user = request.POST.get('user',None) 
            userInst = User.objects.filter(name=user).first()
            if active_room and userInst:
                exist_user_in_roomId(userInst,active_room)
                update_last_seen_message(userInst,active_room)
                context = {'success':True}
            else:
                context = {'error': 'Room or user does not exist'}

        return JsonResponse(context)
class ManageChat(object):
     def insert_message(request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            active_room = request.POST.get('room',None) 
            message = request.POST.get('message',None)
            user = request.POST.get('user',None) 
            userInst = User.objects.filter(name=user).first()
            try:
                if active_room and userInst:
                    context['success'] = True
                    context['active_room'] = active_room

                    msgInstance = Message()
                    msgInstance.room_id = active_room
                    msgInstance.content = message
                    msgInstance.sender_id = userInst.id
                    msgInstance.save()

                    update_room_last_message(msgInstance.id,active_room)
                    update_last_seen_message(userInst,active_room)
                    
                    participentsData = { userInst.name:{'profile_image':'{% static  "img/user-1.png" %}','name':userInst.name}}
                    roomChat = { msgInstance.id :{'message':msgInstance.content,'time':msgInstance.timestamp,'sender':userInst.name}}

                    context['room_participents'] = participentsData
                    context['room_chat'] = roomChat
                else:
                    context['error'] = 'Room or user does not exist'
            except Exception as e:
                print("Exception from insert_message",e)
                context['error'] = e
        return JsonResponse(context)