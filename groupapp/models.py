from django.db import models
import uuid
from django.utils import timezone


class Group(models.Model):
    group_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    description = models.TextField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name

class Milestone(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField()

    date = models.DateField()

    def __str__(self):
        return self.title

class GroupPhoto(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    image = models.ImageField(upload_to='group_photos/')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Announcement(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Teaching(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    content = models.TextField()

    file = models.FileField(upload_to='teachings/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Training(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField()

    date = models.DateField()

    meeting_link = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Mission(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Member(models.Model):

    ROLE_CHOICES = (
        ('Leader', 'Leader'),
        ('Treasurer', 'Treasurer'),
        ('Secretary', 'Secretary'),
        ('Member', 'Member'),
    )

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)

    email = models.EmailField(blank=True, null=True)

    phone = models.CharField(max_length=20)

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='Member'
    )

    bio = models.TextField(blank=True, null=True)

    profile_photo = models.ImageField(
        upload_to='member_profiles/',
        blank=True,
        null=True
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Vision(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Feedback(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class FundingRecord(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    source = models.CharField(max_length=200)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    purpose = models.TextField()

    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.source


class Event(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField()

    event_date = models.DateField()

    event_time = models.TimeField()

    location = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Notification(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

class Document(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True, null=True)

    file = models.FileField(upload_to='documents/')

    uploaded_by = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class PasswordReset(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class AIChat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)