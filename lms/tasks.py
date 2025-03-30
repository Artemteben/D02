from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from lms.models import Course, Subscription


@shared_task
def send_course_update_email(user_email, course_title, message):
    send_mail(
        subject=f"Обновление курса: {course_title}",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
    )


@shared_task
def notify_subscribers_about_updating_course(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)
    for subscriber in subscribers:
        send_course_update_email.delay(
            user_email=subscriber.user.email,
            course_title=course.title,
            message=f"Курс '{course.title}' был изменен. {"message"}",
        )
