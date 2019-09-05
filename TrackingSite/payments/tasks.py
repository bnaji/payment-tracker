from background_task import background
from webpush import send_user_notification
from .models import CustomUser, Family, Lesson
import datetime
from django.utils import timezone 

# Create Lessons on a Weekly basis
@background
def lessons_for_week():
    families = Family.objects.all()
    for family in families:
        # Create Lesson
        start_date = family.starting_date
        # Use timezone aware DateTime object
        now = timezone.now()
        while start_date.year < now.year:
            start_date += datetime.timedelta(days=7)
        while start_date.month < now.month:
            start_date += datetime.timedelta(days=7)
        while start_date.day < now.day:
            start_date += datetime.timedelta(days=7)
        lesson = Lesson(family=family, appt_date=start_date)
        lesson.save()

        # Create / Schedule Webpush
        head = str(lesson)
        id = str(lesson.id)
        # CHANGE UPON DEPLOYMENT
        url = "http://127.0.0.1:8000/payments/" + id
        # Cannot send object to background task
        user = lesson.family.user.username
        payload = {'head': head, 'body': 'Tap to change status', "url": url}
        
        time_delta = start_date - timezone.now()
        make_web_push_notification(user, payload, schedule=time_delta)
        
        
@background
def make_web_push_notification(user, payload):
    user_object = CustomUser.objects.get(username=user)        
    send_user_notification(user=user_object, payload=payload, ttl=1000)

