from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json
from django.http import JsonResponse, HttpResponseBadRequest
from tool.models import Chat, Message

def role(request):
    if request.method == 'GET':
        user = request.user
        role = user.userprofile.role
        return JsonResponse({"role": role}, status=200)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            role = data.get('role')
            user = request.user

            if not role:
                return JsonResponse({"error": "Role is required"}, status=400)

            user.userprofile.role = role
            user.userprofile.save()
            return JsonResponse({"message": "Role set successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")

def chat(request):
    if request.method == 'GET':
        user = request.user
        chats = Chat.objects.filter(sender=user).union(Chat.objects.filter(receiver=user))
        return JsonResponse({"chats": list(chats.values())}, status=200)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            Chat.objects.create(sender=user, receiver=data.get('receiver'))
            return JsonResponse({"message": "Chat created successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")
    
def chat_detail(request, chat_id):
    if request.method == 'GET':
        user = request.user
        chat = Chat.objects.get(id=chat_id)
        messages = Message.objects.get(chat=chat)
        return JsonResponse({"messages": list(messages.values())}, status=200)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            chat = Chat.objects.get(id=chat_id)
            Message.objects.create(chat=chat, sender=user, text=data.get('text'))
            return JsonResponse({"message": "Message sent successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)