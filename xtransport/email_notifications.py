"""
Email notification utilities for Transport Fee Management
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_transport_fee_notification(transport_fee, action='created'):
    """
    Send email notification to parents when a transport fee is created or updated
    
    Args:
        transport_fee: TransportFee instance
        action: 'created' or 'updated'
    """
    student = transport_fee.student
    
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
        'fee': transport_fee,
        'action': action,
        'father_name': student.father_name,
        'mother_name': student.mother_name,
    }
    
    # Subject line
    action_text = 'Recorded' if action == 'created' else 'Updated'
    subject = f'Transport Fee {action_text} - {student.student_name}'
    
    # Render HTML email
    html_message = render_to_string('xtransport/email/fee_notification.html', context)
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
        print(f"Error sending transport fee notification: {e}")
        return False


def send_bulk_fee_notifications(transport_fees):
    """
    Send notifications for multiple transport fees
    
    Args:
        transport_fees: QuerySet or list of TransportFee instances
    """
    success_count = 0
    fail_count = 0
    
    for fee in transport_fees:
        if send_transport_fee_notification(fee, action='created'):
            success_count += 1
        else:
            fail_count += 1
    
    return {
        'success': success_count,
        'failed': fail_count,
        'total': success_count + fail_count
    }


def send_fee_reminder(student, outstanding_amount=None):
    """
    Send a reminder email for transport fee payment
    
    Args:
        student: NewStudent instance
        outstanding_amount: Optional decimal amount
    """
    recipients = []
    if student.father_email_id:
        recipients.append(student.father_email_id)
    if student.mother_email_id:
        recipients.append(student.mother_email_id)
    
    if not recipients:
        return False
    
    context = {
        'student': student,
        'outstanding_amount': outstanding_amount,
        'father_name': student.father_name,
        'mother_name': student.mother_name,
    }
    
    subject = f'Transport Fee Reminder - {student.student_name}'
    html_message = render_to_string('xtransport/email/fee_reminder.html', context)
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
        print(f"Error sending fee reminder: {e}")
        return False

