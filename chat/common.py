from django.http import Http404
from .models import LastMessage, Room, RoomSession, LastSeenMessage, Message, User


def exist_user_in_room(user,room):
    if Room.objects.filter(participants=user.id,name=room).exists():
        return True
    else:
        return False

def exist_user_in_roomId(user,room):
    if Room.objects.filter(participants=user.id,id=room).exists():
        return True
    else:
        return Http404

def get_room_chat(room):
    context = {}
    try:
        room_chat = Message.objects.filter(room=room).order_by('timestamp')
        if room_chat:
            participents = list(room_chat.values_list('sender_id', flat=True))
            participentsData = { x['id']:{'profile_image':'{% static  "img/user-1.png" %}','name':x['name']} for x in User.objects.filter(id__in = participents).values('name','id')}
            roomChat = { x['id']:{'message':x["content"],'time':x['timestamp'],'sender':x['sender_id']} for x in room_chat.values('id','sender_id','timestamp','content')}
            context['room_participents'] = participentsData
            context['room_chat'] = roomChat
        else:
            context['error'] = True
    except Exception as e:
        print("Exception from get_room_chat",e)
        
    return context

def set_room_session(user,room):
    obj, created = RoomSession.objects.get_or_create( user_id=user.id,
    defaults={'room_id': room})
    return True
    
def exist_room(room):
    if Room.objects.filter(name=room).exists():
        return True
    else:
        return False
    
def update_room_last_message(messageId, room):
    lastMsg,created = LastMessage.objects.get_or_create(room_id=room)
    if lastMsg:
        lastMsg.message = messageId
        lastMsg.save()

def update_last_seen_message(user,room):
    lastViewedMessage,created = LastSeenMessage.objects.get_or_create(room_id=room,user_id=user.id)
    lastMsgId = LastMessage.objects.filter(room_id=room).last()
    if lastViewedMessage and lastMsgId:
        lastViewedMessage.message = lastMsgId.message
        lastViewedMessage.save()