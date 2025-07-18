from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from xstudent.models import NewStudent, Attendance
import random
from datetime import date, datetime, timedelta, time


class Command(BaseCommand):
    help = 'Create dummy attendance data for testing the attendance system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=14,
            help='Number of past days to create attendance for (default: 14)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing attendance records before creating new ones'
        )

    def handle(self, *args, **options):
        if options['clear']:
            Attendance.objects.all().delete()
            self.stdout.write(
                self.style.WARNING('Cleared all existing attendance records.')
            )

        days = options['days']
        
        # Get all active students
        students = list(NewStudent.objects.filter(status='active'))
        
        if not students:
            self.stdout.write(
                self.style.ERROR('No active students found! Please create students first.')
            )
            return
        
        # Get or create a default user for recording attendance
        try:
            user = User.objects.get(username='admin')
        except User.DoesNotExist:
            # Create a default admin user if it doesn't exist
            user = User.objects.create_user(
                username='admin',
                email='admin@edupulse.com',
                password='admin123',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(
                self.style.SUCCESS('Created default admin user (username: admin, password: admin123)')
            )

        # Define attendance probabilities (realistic distribution)
        attendance_weights = [
            ('present', 70),  # 70% present
            ('absent', 15),   # 15% absent
            ('late', 10),     # 10% late
            ('excused', 5),   # 5% excused
        ]
        
        # Prepare choices for random selection
        status_choices = []
        for status, weight in attendance_weights:
            status_choices.extend([status] * weight)

        created_records = []
        start_date = date.today() - timedelta(days=days)
        
        for day_offset in range(days + 1):  # Include today
            current_date = start_date + timedelta(days=day_offset)
            
            # Skip weekends (Friday and Saturday in Kuwait)
            if current_date.weekday() in [4, 5]:  # Friday=4, Saturday=5
                continue
            
            self.stdout.write(f"Creating attendance for {current_date}...")
            
            for student in students:
                # Check if attendance already exists for this student and date
                if Attendance.objects.filter(student=student, date=current_date).exists():
                    continue
                
                # Randomly determine attendance status
                status = random.choice(status_choices)
                
                # Generate realistic times
                time_in = None
                time_out = None
                notes = ""
                
                if status == 'present':
                    # Normal arrival time: 7:30 AM - 8:30 AM
                    hour = random.randint(7, 8)
                    minute = random.randint(0, 59) if hour == 7 else random.randint(0, 30)
                    time_in = time(hour, minute)
                    
                    # Departure time: 2:00 PM - 3:30 PM
                    departure_hour = random.randint(14, 15)
                    departure_minute = random.randint(0, 59) if departure_hour == 14 else random.randint(0, 30)
                    time_out = time(departure_hour, departure_minute)
                
                elif status == 'late':
                    # Late arrival: 8:31 AM - 10:00 AM
                    hour = random.randint(8, 9)
                    minute = random.randint(31, 59) if hour == 8 else random.randint(0, 59)
                    time_in = time(hour, minute)
                    
                    # Normal departure
                    departure_hour = random.randint(14, 15)
                    departure_minute = random.randint(0, 59) if departure_hour == 14 else random.randint(0, 30)
                    time_out = time(departure_hour, departure_minute)
                    
                    late_reasons = [
                        "Traffic delay", "Medical appointment", "Family matter",
                        "Transportation issue", "Overslept"
                    ]
                    notes = f"Reason: {random.choice(late_reasons)}"
                
                elif status == 'absent':
                    absent_reasons = [
                        "Sick leave", "Family emergency", "Medical appointment",
                        "Travel", "Personal matter", "Weather conditions"
                    ]
                    notes = f"Reason: {random.choice(absent_reasons)}"
                
                elif status == 'excused':
                    excused_reasons = [
                        "Medical appointment with certificate", "Family bereavement",
                        "Official school event", "Medical procedure", "Court appearance"
                    ]
                    notes = f"Excused - {random.choice(excused_reasons)}"

                try:
                    attendance = Attendance.objects.create(
                        student=student,
                        date=current_date,
                        status=status,
                        time_in=time_in,
                        time_out=time_out,
                        notes=notes,
                        recorded_by=user
                    )
                    created_records.append(attendance)
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creating attendance for {student.student_name} on {current_date}: {str(e)}')
                    )
                    continue

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(created_records)} attendance records!')
        )
        
        # Display summary statistics
        self.stdout.write("\n" + "="*60)
        self.stdout.write("ATTENDANCE SUMMARY:")
        self.stdout.write("="*60)
        
        # Count by status
        status_counts = {}
        daily_counts = {}
        student_attendance = {}
        
        for record in created_records:
            status_counts[record.status] = status_counts.get(record.status, 0) + 1
            daily_counts[record.date] = daily_counts.get(record.date, 0) + 1
            
            if record.student.student_name not in student_attendance:
                student_attendance[record.student.student_name] = {'present': 0, 'absent': 0, 'late': 0, 'excused': 0}
            student_attendance[record.student.student_name][record.status] += 1

        self.stdout.write(f"Total Records Created: {len(created_records)}")
        self.stdout.write(f"Date Range: {start_date} to {date.today()}")
        self.stdout.write(f"Students: {len(students)}")
        
        self.stdout.write("\nStatus Distribution:")
        for status, count in status_counts.items():
            percentage = (count / len(created_records)) * 100
            self.stdout.write(f"  {status.title()}: {count} ({percentage:.1f}%)")
        
        self.stdout.write(f"\nDaily Attendance Counts:")
        for attendance_date in sorted(daily_counts.keys()):
            count = daily_counts[attendance_date]
            self.stdout.write(f"  {attendance_date}: {count} records")
        
        # Show top attending students
        self.stdout.write(f"\nTop 5 Students by Attendance:")
        sorted_students = sorted(
            student_attendance.items(),
            key=lambda x: x[1]['present'],
            reverse=True
        )
        
        for i, (student_name, stats) in enumerate(sorted_students[:5]):
            total_days = sum(stats.values())
            present_percentage = (stats['present'] / total_days) * 100 if total_days > 0 else 0
            self.stdout.write(f"  {i+1}. {student_name}: {stats['present']}/{total_days} days ({present_percentage:.1f}%)")
        
        # Show concerning attendance (below 70%)
        concerning_students = []
        for student_name, stats in student_attendance.items():
            total_days = sum(stats.values())
            if total_days > 0:
                present_percentage = (stats['present'] / total_days) * 100
                if present_percentage < 70:
                    concerning_students.append((student_name, present_percentage, stats))
        
        if concerning_students:
            self.stdout.write(f"\n⚠️  Students with Concerning Attendance (< 70%):")
            for student_name, percentage, stats in concerning_students:
                total_days = sum(stats.values())
                self.stdout.write(f"  • {student_name}: {percentage:.1f}% ({stats['present']}/{total_days} days)")
        
        self.stdout.write("\n" + "="*60)
        self.stdout.write("✅ Dummy attendance data creation completed!")
        self.stdout.write("You can now view the attendance dashboard and reports.")
        self.stdout.write("="*60) 