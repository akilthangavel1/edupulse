"""
Management command to send backup class reminders
Run this daily (preferably in the evening) to send next-day reminders
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from xtrainer.models import BackupSchedule
from xtrainer.email_notifications import (
    send_backup_reminder_to_faculty,
    send_backup_reminder_to_students
)


class Command(BaseCommand):
    help = 'Send backup class reminders to faculty and students for tomorrow\'s classes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending emails',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        tomorrow = date.today() + timedelta(days=1)
        
        # Get all backup schedules for tomorrow
        schedules = BackupSchedule.objects.filter(
            date=tomorrow,
            status__in=['scheduled', 'confirmed']
        ).select_related('backup_faculty', 'original_faculty', 'course')
        
        if not schedules.exists():
            self.stdout.write(
                self.style.WARNING(f'No backup schedules found for {tomorrow}')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(f'Found {schedules.count()} backup schedule(s) for {tomorrow}')
        )
        
        faculty_sent = 0
        student_sent = 0
        faculty_failed = 0
        student_failed = 0
        
        for schedule in schedules:
            schedule_info = f'{schedule.schedule_id} - {schedule.course.name} ({schedule.start_time}-{schedule.end_time})'
            
            if dry_run:
                self.stdout.write(f'  [DRY RUN] Would send reminders for: {schedule_info}')
                self.stdout.write(f'    → Backup Faculty: {schedule.backup_faculty.email}')
                self.stdout.write(f'    → Students: via course enrollments')
            else:
                # Send to backup faculty
                if send_backup_reminder_to_faculty(schedule):
                    faculty_sent += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Faculty reminder sent: {schedule_info}')
                    )
                else:
                    faculty_failed += 1
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Faculty reminder failed: {schedule_info}')
                    )
                
                # Send to students
                if send_backup_reminder_to_students(schedule):
                    student_sent += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Student reminder sent: {schedule_info}')
                    )
                else:
                    student_failed += 1
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠ Student reminder failed (no emails?): {schedule_info}')
                    )
        
        # Summary
        if dry_run:
            self.stdout.write(
                self.style.WARNING('\n[DRY RUN] No emails were actually sent.')
            )
        else:
            self.stdout.write(self.style.SUCCESS('\n=== Summary ==='))
            self.stdout.write(f'Faculty reminders sent: {faculty_sent}')
            self.stdout.write(f'Faculty reminders failed: {faculty_failed}')
            self.stdout.write(f'Student reminders sent: {student_sent}')
            self.stdout.write(f'Student reminders failed: {student_failed}')
            self.stdout.write(
                self.style.SUCCESS(f'\nTotal schedules processed: {schedules.count()}')
            )

