from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json
from django.http import JsonResponse, HttpResponseBadRequest

def index(request):
    return JsonResponse({"message": "Hello, world!"})

from django.middleware.csrf import get_token

def get_csrf_token(request):
    if request.method == 'GET':
        csrf_token = get_token(request)  # Явно получить CSRF-токен
        print(csrf_token)
        return JsonResponse({"csrf_token": csrf_token})
    return JsonResponse({"error": "Method not allowed"}, status=405)

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful", "user_id": user.id, "filled": user.userprofile.filled})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
    return JsonResponse({"error": "Method not allowed"}, status=405)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({"message": "Logout successful"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return JsonResponse({"message": "User created successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)
    
    
def resume_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        role = data.get('role')

        try:
            user = User.objects.get(id=user_id)
            
            if role == 'freelancer':
                name = data.get('name')
                surname = data.get('surname')
                fathers_name = data.get('fathers_name')
                sex = data.get('sex')
                date_of_birth = data.get('date_of_birth')
                phone_number = data.get('phone_number')
                location = data.get('location')
                education = data.get('education')
                institution = data.get('institution')
                specialization = data.get('specialization')
                skills = data.get('skills')
                
                UserProfile.objects.create(
                    user=user,
                    ROLE=role,
                    NAME=name,
                    SURNAME=surname,
                    FATHERS_NAME=fathers_name,
                    SEX=sex,
                    Date_of_birth=date_of_birth,
                    phone_number=phone_number,
                    location=location,
                    education=education,
                    institution=institution,
                    specialization=specialization,
                    skills=skills,
                    filled=True
                )
            elif role == 'company':
                name = data.get('name')
                location = data.get('location')
                contact_person = data.get('contact_person')
                phone_number = data.get('phone_number')
                link = data.get('link')
                description = data.get('description')
                
                UserProfile.objects.create(
                    user=user,
                    ROLE=role,
                    NAME=name,
                    location=location,
                    contact_person=contact_person,
                    phone_number=phone_number,
                    link=link,
                    description=description,
                    filled=True
                )
                
            elif role == 'private':
                name = data.get('name')
                surname = data.get('surname')
                fathers_name = data.get('fathers_name')
                sex = data.get('sex')
                date_of_birth = data.get('date_of_birth')
                phone_number = data.get('phone_number')
                location = data.get('location')
                link = data.get('link')
                
                UserProfile.objects.create(
                    user=user,
                    ROLE=role,
                    NAME=name,
                    SURNAME=surname,
                    FATHERS_NAME=fathers_name,
                    SEX=sex,
                    Date_of_birth=date_of_birth,
                    phone_number=phone_number,
                    location=location,
                    link=link,
                    filled=True
                )
            else:
                return JsonResponse({"error": "Invalid role"}, status=400)
            
            return JsonResponse({"message": "Resume uploaded successfully"})
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Method not allowed"}, status=405)


def get_user_profile(request, user_id):
    if request.method == 'GET':
        user_id = user_id if user_id else request.user.id
        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
            data = {
                "ROLE": user_profile.ROLE,
                "NAME": user_profile.NAME,
                "SURNAME": user_profile.SURNAME,
                "FATHERS_NAME": user_profile.FATHERS_NAME,
                "SEX": user_profile.SEX,
                "Date_of_birth": user_profile.Date_of_birth,
                "email": user_profile.user.email,
                # "Avatar": user_profile.Avatar if user_profile.Avatar else None,
                "phone_number": user_profile.phone_number,
                "location": user_profile.location,
                "education": user_profile.education,
                "institution": user_profile.institution,
                "specialization": user_profile.specialization,
                "skills": user_profile.skills,
                "industry": user_profile.industry,
                "contact_person": user_profile.contact_person,
                "link": user_profile.link,
                "description": user_profile.description,
                "filled": user_profile.filled,
                "created_at": user_profile.created_at,
                "updated_at": user_profile.updated_at,
            }
            
            return JsonResponse(data)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "User profile not found"}, status=404)
        
        
    return JsonResponse({"error": "Method not allowed"}, status=405)


def vacancy_view(request):
    if request.method == 'GET':
        userprofile = request.user.userprofile
        if userprofile.ROLE == 'freelancer':
            vacancies = Vacancy.objects.all()
            
            return JsonResponse({"vacancies": list(vacancies.values())})
        else:
            vacancies = Vacancy.objects.filter(user_profile=userprofile)
            
            return JsonResponse({"vacancies": list(vacancies.values())})
            
    elif request.method == 'POST':
        data = json.loads(request.body)
        category = data.get('category')
        name = data.get('name')
        position = data.get('position')
        experience = data.get('experience')
        deadline = data.get('deadline')
        salary = data.get('salary')
        work_conditions = data.get('work_conditions')

        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
            Vacancy.objects.create(
                user_profile=user_profile,
                Category=category,
                name=name,
                position=position,
                experience=experience,
                deadline=deadline,
                salary=salary,
                work_conditions=work_conditions
            )
            return JsonResponse({"message": "Vacancy created successfully"})
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "User profile not found"}, status=404)
    return JsonResponse({"error": "Method not allowed"}, status=405)


def candidate_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vacancy_id = data.get('vacancy_id')
        message = data.get('message')

        try: 
            vacancy = Vacancy.objects.get(id=vacancy_id)
            chat = Chat.objects.create(
                sender=request.user.userprofile,
                receiver=vacancy.user_profile
            )
            
            Message.objects.create(
                chat=chat,
                sender=request.user.userprofile,
                message=message
            )
            
            Candidate.objects.create(vacancy=vacancy, candidate=request.user.userprofile)
            return JsonResponse({"message": "Candidate added successfully"})
        except (Vacancy.DoesNotExist, UserProfile.DoesNotExist):
            return JsonResponse({"error": "Vacancy or Candidate not found"}, status=404)
    elif request.method == 'GET':
        userprofile = request.user.userprofile
        candidates = Candidate.objects.filter(vacancy__user_profile=userprofile)
        return JsonResponse({"candidates": list(candidates.values())})
    return JsonResponse({"error": "Method not allowed"}, status=405)


def set_candidate_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        candidate_id = data.get('candidate_id')
        status = data.get('status')

        try:
            candidate = Candidate.objects.get(id=candidate_id)
            candidate.status = status
            candidate.save()
            return JsonResponse({"message": "Candidate status updated successfully"})
        except Candidate.DoesNotExist:
            return JsonResponse({"error": "Candidate not found"}, status=404)
    return JsonResponse({"error": "Method not allowed"}, status=405)


def set_candidate_date_link(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vacancy_id = data.get('vacancy_id')
        time = data.get('time')
        link = data.get('link')

        try:
            candidate = Candidate.objects.get(vacancy=Vacancy.objects.get(id=vacancy_id))
            candidate.time = time
            candidate.link = link
            candidate.save()
            return JsonResponse({"message": "Candidate date and link updated successfully"})
        except Candidate.DoesNotExist:
            return JsonResponse({"error": "Candidate not found"}, status=404)
    return JsonResponse({"error": "Method not allowed"}, status=405)

def chat_view(request):
    if request.method == 'GET':
        userprofile = request.user.userprofile
        chats = Chat.objects.filter(sender=userprofile) | Chat.objects.filter(receiver=userprofile)
        return JsonResponse({"chats": list(chats.values())})
    
    
def message_view(request):
    if request.method == 'GET':
        chat_id = request.GET.get('chat_id')
        try:
            chat = Chat.objects.get(id=chat_id)
            messages = Message.objects.filter(chat=chat)
            return JsonResponse({"messages": list(messages.values())})
        except Chat.DoesNotExist:
            return JsonResponse({"error": "Chat not found"}, status=404)
        
    elif request.method == 'POST':
        data = json.loads(request.body)
        chat_id = data.get('chat_id')
        message = data.get('message')

        try:
            chat = Chat.objects.get(id=chat_id)
            Message.objects.create(
                chat=chat,
                sender=request.user.userprofile,
                message=message
            )
            return JsonResponse({"message": "Message sent successfully"})
        except Chat.DoesNotExist:
            return JsonResponse({"error": "Chat not found"}, status=404)
    return JsonResponse({"error": "Method not allowed"}, status=405)

    

