from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import datetime

class Family(models.Model):
    client_name = models.CharField(max_length=100)
    student_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    price = models.IntegerField(default=40)
    starting_date = models.DateTimeField()
    balance = models.IntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
    )

    # Displays as: Family (Student)
    def __str__(self):
        return self.client_name + " (" + self.student_name + ")"

    def update(self):
        new_balance = 0
        for lesson in self.lesson_set.all():
            lesson.save()
            new_balance += lesson.lesson_balance
        self.balance = new_balance

    # Testing
    def create_first_lesson(self):
        if not self.lesson_set.all():
            lesson = Lesson(family=self, appt_date=self.starting_date)
            lesson.save()

    def get_absolute_url(self):
        return reverse('payments:family')
    
    # Override the default Django save() method
    def save(self, *args, **kwargs):        
        self.update()
        super().save(*args, **kwargs)  # Call the "real" save() method.
        self.create_first_lesson()

class Lesson(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)    
    appt_date = models.DateTimeField()    

    # Default as 0 instead of family.price or family_price, corrected on save()
    lesson_balance = models.IntegerField(default=0)

    # Defining variables here is good for error prevention and logic seperation
    # https://stackoverflow.com/questions/18676156/how-to-properly-use-the-choices-field-option-in-django
    PAID = 'Paid'
    SKIPPED = 'Skipped'
    PENDING = 'Pending'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
        (SKIPPED, 'Skipped'),        
    )

    status = models.CharField(
        max_length=10,        
        choices=STATUS_CHOICES,
        default=PENDING
    )
    
    def update(self):
        if self.status == 'Pending':
            self.lesson_balance = self.family.price
        if self.status == 'Paid':
            self.lesson_balance = 0
        if self.status == 'Skipped':
            self.lesson_balance = 0

    # Call update() on save() by overriding the default Django save() method 
    def save(self, *args, **kwargs):
        self.update()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    # Displays as: Family Name (Child Name) | Date | Status
    def __str__(self):
        str_date = self.appt_date.strftime("%a %d %B %Y")
        name = str(self.family)
        return name + " | " + str_date + " | " + self.status

# Allow future ability to extend default User Model
# See https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class CustomUser(AbstractUser):
    pass

