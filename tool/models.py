from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_ROLE_CHOICES = (
        ('freelancer', 'Freelancer'),
        ('employer', 'Employer')
    )
    id = models.CharField(max_length=100, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    fathers_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, blank=True, null=True)
    tech_stack = models.ManyToManyField('TechStack', blank=True)
    experience = models.IntegerField(blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    bank_account = models.CharField(max_length=100, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    resume = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    bin = models.CharField(max_length=12, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    institution = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
class Links(models.Model):
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.link
    
class Company(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    num_of_employees = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    contact_person_position = models.CharField(max_length=100, blank=True, null=True)
    contact_person_full_name = models.CharField(max_length=100, blank=True, null=True)
    contact_person_phone_number = models.CharField(max_length=15, blank=True, null=True)
    contact_person_email = models.EmailField(blank=True, null=True)
    bin_of_company = models.CharField(max_length=12, blank=True, null=True)
    link = models.ManyToManyField('Links', blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class PrivateEmployer(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    fathers_name = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.surname}'
    
class TechStack(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class Vacancy(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, blank=True, default="Unknown")
    position = models.CharField(max_length=100, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    skills = models.CharField(max_length=100, blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    compensation = models.IntegerField(blank=True, null=True)
    work_conditions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.position
    
class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    id = models.CharField(max_length=100, primary_key=True)
    Vacancy = models.ForeignKey('Vacancy', on_delete=models.CASCADE, blank=True, null=True)
    candidate = models.ForeignKey('UserProfile', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
