from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Attendance
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Attendance)
def send_absence_notification(sender, instance, created, **kwargs):
    """
    Signal handler to send email notification to parents when student is marked absent.
    Triggers on both creation and update of attendance records.
    """
    # Only send notification if status is 'absent'
    if instance.status == 'absent':
        student = instance.student
        
        # Prepare email recipients (both father and mother)
        recipients = []
        if student.father_email_id:
            recipients.append(student.father_email_id)
        if student.mother_email_id:
            recipients.append(student.mother_email_id)
        
        # Only proceed if there are recipients
        if not recipients:
            logger.warning(f"No parent email addresses found for student: {student.student_name}")
            return
        
        # Prepare email context
        context = {
            'student_name': student.student_name,
            'grade': student.grade,
            'program': student.program,
            'date': instance.date,
            'father_name': student.father_name,
            'mother_name': student.mother_name,
            'notes': instance.notes,
            'recorded_by': instance.recorded_by.get_full_name() if instance.recorded_by else 'School Administration',
        }
        
        # Email subject
        subject = f"Absence Notification - {student.student_name} - {instance.date}"
        
        # Email body (plain text)
        message = f"""
Dear {student.father_name} and {student.mother_name},

This is to inform you that your child, {student.student_name}, was marked absent on {instance.date.strftime('%B %d, %Y')}.

Student Details:
- Name: {student.student_name}
- Grade: {student.grade}
- Program: {student.program}
- Date of Absence: {instance.date.strftime('%B %d, %Y')}
"""
        
        if instance.notes:
            message += f"\nAdditional Notes:\n{instance.notes}\n"
        
        message += """
If this absence was unexpected or if you have any questions, please contact the school administration immediately.

Best regards,
EduPulse School Management
"""
        
        # Try to send HTML email if template exists, otherwise use plain text
        try:
            html_message = render_to_string('xstudent/emails/absence_notification.html', context)
        except:
            html_message = None
        
        # Send email
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Absence notification sent to parents of {student.student_name} for date {instance.date}")
        except Exception as e:
            logger.error(f"Failed to send absence notification for {student.student_name}: {str(e)}")


def send_manual_absence_notification(attendance_id):
    """
    Helper function to manually trigger absence notification for a specific attendance record.
    Can be used for testing or resending notifications.
    """
    try:
        attendance = Attendance.objects.get(id=attendance_id)
        send_absence_notification(sender=Attendance, instance=attendance, created=False)
        return True, "Notification sent successfully"
    except Attendance.DoesNotExist:
        return False, "Attendance record not found"
    except Exception as e:
        return False, f"Error sending notification: {str(e)}"

