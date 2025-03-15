from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_ROLE_CHOICES = (
        ('freelancer', 'Freelancer'),
        ('employer', 'Employer')
    )
    id = models.CharField(max_length=100, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    fathers_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES)
    tech_stack = models.ManyToManyField('TechStack')
    experience = models.IntegerField()
    company_name = models.CharField(max_length=100, blank=True)
    bank_account = models.CharField(max_length=100, blank=True)
    rating = models.FloatField()
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    resume = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sex = models.CharField(max_length=10, blank=True)
    bin = models.CharField(max_length=12, blank=True)
    education = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    
class TechStack(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Job(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    salary = models.FloatField()
    tech_stack = models.ForeignKey('TechStack', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company_logos/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    id = models.CharField(max_length=100, primary_key=True)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    candidate = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
    
class Review(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    worker = models.ForeignKey('UserProfile', related_name='worker_reviews', on_delete=models.CASCADE)
    employer = models.ForeignKey('UserProfile', related_name='employer_reviews', on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
    
class Chat(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    sender = models.ForeignKey('UserProfile', related_name='sent_chats', on_delete=models.CASCADE)
    receiver = models.ForeignKey('UserProfile', related_name='received_chats', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sender.user.username + ' -> ' + self.receiver.user.username
    
class Message(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    sender = models.ForeignKey('UserProfile', related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey('UserProfile', related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
