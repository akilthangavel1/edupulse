from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from xstudent.models import NewStudent, Attendance
from xstudent.signals import send_manual_absence_notification
from datetime import date


class Command(BaseCommand):
    help = 'Test the absence notification email system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--student-id',
            type=int,
            help='Student ID to create test absence notification for',
        )
        parser.add_argument(
            '--attendance-id',
            type=int,
            help='Existing attendance ID to resend notification for',
        )

    def handle(self, *args, **options):
        student_id = options.get('student_id')
        attendance_id = options.get('attendance_id')

        # If attendance ID is provided, resend notification
        if attendance_id:
            success, message = send_manual_absence_notification(attendance_id)
            if success:
                self.stdout.write(self.style.SUCCESS(message))
            else:
                self.stdout.write(self.style.ERROR(message))
            return

        # If student ID is provided, create test absence record
        if student_id:
            try:
                student = NewStudent.objects.get(id=student_id, status='active')
            except NewStudent.DoesNotExist:
                raise CommandError(f'Active student with ID {student_id} does not exist')
            
            # Create or update absence record for today
            attendance, created = Attendance.objects.update_or_create(
                student=student,
                date=date.today(),
                defaults={
                    'status': 'absent',
                    'notes': 'Test absence notification - created by management command'
                }
            )
            
            action = 'Created' if created else 'Updated'
            self.stdout.write(
                self.style.SUCCESS(
                    f'{action} absence record for {student.student_name} on {date.today()}'
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Notification emails will be sent to: {student.father_email_id}, {student.mother_email_id}'
                )
            )
            return

        # If no arguments provided, show usage help
        self.stdout.write(self.style.WARNING('Please provide either --student-id or --attendance-id'))
        self.stdout.write('')
        self.stdout.write('Usage examples:')
        self.stdout.write('  python manage.py test_absence_notification --student-id 1')
        self.stdout.write('  python manage.py test_absence_notification --attendance-id 5')
        self.stdout.write('')
        
        # Show available students
        students = NewStudent.objects.filter(status='active')[:5]
        if students:
            self.stdout.write('Available active students (first 5):')
            for student in students:
                self.stdout.write(
                    f'  ID: {student.id} - {student.student_name} '
                    f'(Father: {student.father_email_id}, Mother: {student.mother_email_id})'
                )

