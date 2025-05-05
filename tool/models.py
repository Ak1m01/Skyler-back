from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('freelancer', 'Freelancer'),
        ('company', 'Company'),
        ('private', 'Private Person'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE = models.CharField(max_length=20, choices=ROLE_CHOICES)
    NAME = models.CharField(max_length=100)
    SURNAME = models.CharField(max_length=100)
    FATHERS_NAME = models.CharField(max_length=100, null=True, blank=True)
    SEX = models.CharField(max_length=10)
    Date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    Avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    location = models.CharField(max_length=200)
    education = models.CharField(max_length=200, null=True, blank=True)
    institution = models.CharField(max_length=200, null=True, blank=True)
    specialization = models.CharField(max_length=200, null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    contact_person = models.CharField(max_length=200, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    filled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Vacancy(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('accepted', 'Accepted'),
        ('pending', 'Pending'),
    ]
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    Category = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    work_conditions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Candidate(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    candidate = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    time = models.DateTimeField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Chat(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_chats')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
