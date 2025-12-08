"""
Email notification utilities for Faculty/Trainer Management
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import datetime, timedelta


def send_backup_assignment_notification(backup_schedule):
    """
    Send email to backup faculty when assigned to cover a class
    
    Args:
        backup_schedule: BackupSchedule instance
    """
    backup_faculty = backup_schedule.backup_faculty
    
    if not backup_faculty.email:
        return False
    
    context = {
        'backup_schedule': backup_schedule,
        'backup_faculty': backup_faculty,
        'original_faculty': backup_schedule.original_faculty,
        'course': backup_schedule.course,
    }
    
    subject = f'Backup Class Assignment - {backup_schedule.course.name} on {backup_schedule.date}'
    html_message = render_to_string('xtrainer/email/backup_assignment.html', context)
    plain_message = strip_tags(html_message)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[backup_faculty.email],
    )
    email.attach_alternative(html_message, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending backup assignment notification: {e}")
        return False


def send_backup_student_notification(backup_schedule):
    """
    Send email to students about substitute teacher
    
    Args:
        backup_schedule: BackupSchedule instance
    """
    from xcoursefee.models import StudentEnrollment
    
    # Get enrolled students for this course
    enrollments = StudentEnrollment.objects.filter(
        course=backup_schedule.course,
        status='active'
    ).select_related('student')
    
    if not enrollments.exists():
        return False
    
    # Collect parent emails
    recipients = []
    for enrollment in enrollments:
        student = enrollment.student
        if student.father_email_id:
            recipients.append(student.father_email_id)
        if student.mother_email_id:
            recipients.append(student.mother_email_id)
    
    recipients = list(set(recipients))  # Remove duplicates
    
    if not recipients:
        return False
    
    context = {
        'backup_schedule': backup_schedule,
        'backup_faculty': backup_schedule.backup_faculty,
        'original_faculty': backup_schedule.original_faculty,
        'course': backup_schedule.course,
    }
    
    subject = f'Class Update - Substitute Teacher for {backup_schedule.course.name}'
    html_message = render_to_string('xtrainer/email/backup_student_notification.html', context)
    plain_message = strip_tags(html_message)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        bcc=recipients,  # Use BCC for privacy
    )
    email.attach_alternative(html_message, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending student notification: {e}")
        return False


def send_backup_confirmation_notification(backup_schedule):
    """
    Send confirmation email to backup faculty when they confirm
    
    Args:
        backup_schedule: BackupSchedule instance
    """
    backup_faculty = backup_schedule.backup_faculty
    
    if not backup_faculty.email:
        return False
    
    context = {
        'backup_schedule': backup_schedule,
        'backup_faculty': backup_faculty,
        'original_faculty': backup_schedule.original_faculty,
        'course': backup_schedule.course,
    }
    
    subject = f'Backup Class Confirmed - {backup_schedule.course.name} on {backup_schedule.date}'
    html_message = render_to_string('xtrainer/email/backup_confirmation.html', context)
    plain_message = strip_tags(html_message)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[backup_faculty.email],
    )
    email.attach_alternative(html_message, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending confirmation notification: {e}")
        return False


def send_backup_reminder_to_faculty(backup_schedule):
    """
    Send reminder to backup faculty (day before class)
    
    Args:
        backup_schedule: BackupSchedule instance
    """
    backup_faculty = backup_schedule.backup_faculty
    
    if not backup_faculty.email:
        return False
    
    context = {
        'backup_schedule': backup_schedule,
        'backup_faculty': backup_faculty,
        'original_faculty': backup_schedule.original_faculty,
        'course': backup_schedule.course,
    }
    
    subject = f'Reminder: Backup Class Tomorrow - {backup_schedule.course.name}'
    html_message = render_to_string('xtrainer/email/backup_reminder_faculty.html', context)
    plain_message = strip_tags(html_message)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[backup_faculty.email],
    )
    email.attach_alternative(html_message, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending faculty reminder: {e}")
        return False


def send_backup_reminder_to_students(backup_schedule):
    """
    Send reminder to students (day before class)
    
    Args:
        backup_schedule: BackupSchedule instance
    """
    from xcoursefee.models import StudentEnrollment
    
    enrollments = StudentEnrollment.objects.filter(
        course=backup_schedule.course,
        status='active'
    ).select_related('student')
    
    if not enrollments.exists():
        return False
    
    recipients = []
    for enrollment in enrollments:
        student = enrollment.student
        if student.father_email_id:
            recipients.append(student.father_email_id)
        if student.mother_email_id:
            recipients.append(student.mother_email_id)
    
    recipients = list(set(recipients))
    
    if not recipients:
        return False
    
    context = {
        'backup_schedule': backup_schedule,
        'backup_faculty': backup_schedule.backup_faculty,
        'original_faculty': backup_schedule.original_faculty,
        'course': backup_schedule.course,
    }
    
    subject = f'Reminder: Substitute Teacher Tomorrow - {backup_schedule.course.name}'
    html_message = render_to_string('xtrainer/email/backup_reminder_student.html', context)
    plain_message = strip_tags(html_message)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        bcc=recipients,
    )
    email.attach_alternative(html_message, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending student reminder: {e}")
        return False


def send_all_backup_notifications(backup_schedule):
    """
    Send all initial notifications when backup is created
    
    Args:
        backup_schedule: BackupSchedule instance
    
    Returns:
        dict with success status for each notification type
    """
    results = {
        'backup_faculty': send_backup_assignment_notification(backup_schedule),
        'students': send_backup_student_notification(backup_schedule),
    }
    
    # Update notification flags
    backup_schedule.notification_sent_to_backup = results['backup_faculty']
    backup_schedule.notification_sent_to_students = results['students']
    
    if results['backup_faculty'] or results['students']:
        backup_schedule.notification_date = timezone.now()
    
    backup_schedule.save()
    
    return results

