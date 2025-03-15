from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json
from django.http import JsonResponse, HttpResponseBadRequest
from .models import UserProfile, TechStack
import uuid
from time import sleep

def index(request):
    return JsonResponse({"message": "Hello, world!"})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('email')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Login successful"}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")
    
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return JsonResponse({"message": "User created successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")
    
def signout(request):
    logout(request)
    return JsonResponse({"message": "Signout successful"}, status=200)

def form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            fathers_name = data.get('fathers_name')
            sex = data.get('sex')
            birth_date = data.get('birth_date')
            phone_number = data.get('phone_number')
            country = data.get('country')
            city = data.get('city')
            role = data.get('role')
            bin = data.get('bin')
            education = data.get('education')
            institution = data.get('institution')
            specialization = data.get('specialization')
            tech_stack = data.get('tech_stack')

            user = request.user

            user_profile = UserProfile.objects.create(
                user=user,
                id=uuid.uuid4(),
                first_name=first_name,
                last_name=last_name,
                fathers_name=fathers_name,
                sex=sex,
                birth_date=birth_date,
                phone_number=phone_number,
                country=country,
                city=city,
                role=role,
                bin=bin,
                education=education,
                institution=institution,
                specialization=specialization,
                tech_stack=tech_stack
            )

            user_profile.save()

            return JsonResponse({"message": "Profile created successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")
    
def techstacks(request):
    tech_stacks = list(TechStack.objects.all().values('id', 'name'))
    return JsonResponse({"tech_stacks": tech_stacks}, status=200)