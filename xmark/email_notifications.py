"""
Email notification utilities for Marks Management
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_marks_published_notification(student_mark):
    """
    Send email to parents when marks are published
    
    Args:
        student_mark: StudentMark instance
    """
    student = student_mark.student
    
    # Prepare recipient list
    recipients = []
    if student.father_email_id:
        recipients.append(student.father_email_id)
    if student.mother_email_id:
        recipients.append(student.mother_email_id)
    
    # If no email addresses, return
    if not recipients:
        return False
    
    # Prepare email context
    context = {
        'student': student,
        'mark': student_mark,
        'subject': student_mark.subject,
        'assessment_type': student_mark.assessment_type,
        'father_name': student.father_name,
        'mother_name': student.mother_name,
    }
    
    # Subject line
    subject = f'Exam Marks Published - {student.student_name} - {student_mark.subject.name}'
    
    # Render HTML email
    html_message = render_to_string('xmark/email/marks_notification.html', context)
    plain_message = strip_tags(html_message)
    
    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients,
    )
    email.attach_alternative(html_message, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error sending marks notification: {e}")
        return False


def send_bulk_marks_notification(student_marks):
    """
    Send notifications for multiple marks (bulk entry)
    
    Args:
        student_marks: QuerySet or list of StudentMark instances
    
    Returns:
        dict with success/failed counts
    """
    success_count = 0
    fail_count = 0
    
    for mark in student_marks:
        if send_marks_published_notification(mark):
            success_count += 1
        else:
            fail_count += 1
    
    return {
        'success': success_count,
        'failed': fail_count,
        'total': success_count + fail_count
    }


def send_marks_updated_notification(student_mark):
    """
    Send email to parents when marks are updated/revised
    
    Args:
        student_mark: StudentMark instance
    """
    student = student_mark.student
    
    recipients = []
    if student.father_email_id:
        recipients.append(student.father_email_id)
    if student.mother_email_id:
        recipients.append(student.mother_email_id)
    
    if not recipients:
        return False
    
    context = {
        'student': student,
        'mark': student_mark,
        'subject': student_mark.subject,
        'assessment_type': student_mark.assessment_type,
        'father_name': student.father_name,
        'mother_name': student.mother_name,
        'is_update': True,
    }
    
    subject = f'Marks Updated - {student.student_name} - {student_mark.subject.name}'
    html_message = render_to_string('xmark/email/marks_notification.html', context)
    plain_message = strip_tags(html_message)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients,
    )
    email.attach_alternative(html_message, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending marks update notification: {e}")
        return False


def send_report_card_notification(student, report_period=None):
    """
    Send report card notification to parents
    
    Args:
        student: NewStudent instance
        report_period: Optional string describing the period
    """
    recipients = []
    if student.father_email_id:
        recipients.append(student.father_email_id)
    if student.mother_email_id:
        recipients.append(student.mother_email_id)
    
    if not recipients:
        return False
    
    # Get all published marks for student
    marks = student.marks.filter(status='published', is_active=True).select_related(
        'subject', 'assessment_type'
    ).order_by('subject__name', 'assessment_type__name')
    
    if not marks.exists():
        return False
    
    context = {
        'student': student,
        'marks': marks,
        'report_period': report_period,
        'father_name': student.father_name,
        'mother_name': student.mother_name,
    }
    
    subject = f'Report Card - {student.student_name}'
    if report_period:
        subject += f' - {report_period}'
    
    html_message = render_to_string('xmark/email/report_card.html', context)
    plain_message = strip_tags(html_message)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients,
    )
    email.attach_alternative(html_message, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending report card: {e}")
        return False

