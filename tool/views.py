from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json
from django.http import JsonResponse, HttpResponseBadRequest
from .models import UserProfile, TechStack, Company, Links, EducationalInstitution, PrivateEmployer
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


def info(request):
    try:
        data = json.loads(request.body)
        role = data.get('role')
        employer = data.get('employer')
        if employer == 'company':
            company_name = data.get('company_name')
            industry = data.get('industry')
            num_of_employees = data.get('num_of_employees')
            location = data.get('location')
            contact_person = data.get('contact_person')
            contact_person_position = data.get('contact_person_position')
            contact_person_full_name = data.get('contact_person_full_name')
            contact_person_phone_number = data.get('contact_person_phone_number')
            contact_person_email = data.get('contact_person_email')
            bin_of_company = data.get('bin_of_company')
            links = data.get('links')
            if links:
                for link in links:
                    link = Links.objects.create(link=link)
                    link.save()
            description = data.get('description')
            company = Company.objects.create(
                name=company_name,
                industry=industry,
                num_of_employees=num_of_employees,
                location=location,
                contact_person=contact_person,
                contact_person_position=contact_person_position,
                contact_person_full_name=contact_person_full_name,
                contact_person_phone_number=contact_person_phone_number,
                contact_person_email=contact_person_email,
                bin_of_company=bin_of_company,
                links=links,
                description=description
            )
            company.save()
            return JsonResponse({"message": "success"}, status=200)
        
        elif employer == 'institution':
            institution_type = data.get('institution_type')
            institution_name = data.get('institution_name')
            location = data.get('location')
            contact_person_full_name = data.get('contact_person_full_name')
            contact_person_position = data.get('contact_person_position')
            contact_person_phone_number = data.get('contact_person_phone_number')
            contact_person_email = data.get('contact_person_email')
            bin_of_institution = data.get('bin_of_institution')
            links = data.get('links')
            if links:
                for link in links:
                    link = Links.objects.create(link=link)
                    link.save()
            description = data.get('description')
            institution = EducationalInstitution.objects.create(
                name=institution_name,
                institution_type=institution_type,
                location=location,
                contact_person_full_name=contact_person_full_name,
                contact_person_position=contact_person_position,
                contact_person_phone_number=contact_person_phone_number,
                contact_person_email=contact_person_email,
                bin_of_institution=bin_of_institution,
                link=links,
                description=description
            )
            institution.save()

            return JsonResponse({"message": "success"}, status=200)
        
        elif employer == 'private':
            name = data.get('employer_name')
            surname = data.get('employer_surname')
            fathers_name = data.get('employer_fathers_name')
            sex = data.get('sex')
            date_of_birth = data.get('date_of_birth')
            phone_number = data.get('phone_number')
            email = data.get('email')
            location = data.get('location')
            private_employer = PrivateEmployer.objects.create(
                name=name,
                surname=surname,
                fathers_name=fathers_name,
                sex=sex,
                date_of_birth=date_of_birth,
                phone_number=phone_number,
                email=email,
                location=location
            )
            private_employer.save()

            return JsonResponse({"message": "success"}, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")