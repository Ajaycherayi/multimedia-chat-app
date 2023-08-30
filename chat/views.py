from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View

# Create your views here.



class JoinRoom(View):
   
    def get(self,request, *args, **kwargs):
        template_name = "home.html"

        context = {
            "first_name": "Anjaneyulu",
            "last_name": "Batta",
            "address": "Hyderabad, India"
        }

        return render(self.request ,template_name,{})
    def post(req, *args, **kwargs):
        return redirect(reverse('app:view', kwargs={}))


class ChatView(View):
   
    def get(self,request, *args, **kwargs):
        context = {}
        context['user'] = request.GET['username']
        # 111111
        # room_data = {}
        # room_data['ajay'] = ['111111','22222','333333','55555','65488','98765']
        # room_data['rahul'] = ['111111']
        # room_data['amjad'] = ['111111','333333']
        # room_data['admin'] = ['111111','22222','333333','55555']
        
        # context['rooms'] = room_data[context['user']] if context['user'] in room_data else ['111111','22222','333333']
        
        template_name = "chat.html"
        return render(self.request ,template_name,context)



