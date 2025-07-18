from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta
import random
from faker import Faker

from xcoursefee.models import (
    Course, FeeStructure, StudentEnrollment, 
    Discount, Invoice, Payment
)
from xstudent.models import NewStudent
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates dummy course fee data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--courses',
            type=int,
            default=15,
            help='Number of courses to create'
        )
        parser.add_argument(
            '--enrollments',
            type=int,
            default=50,
            help='Number of enrollments to create'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing course fee data'
        )

    def handle(self, *args, **options):
        self.fake = Faker()
        
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing course fee data...'))
            Payment.objects.all().delete()
            Invoice.objects.all().delete()
            StudentEnrollment.objects.all().delete()
            FeeStructure.objects.all().delete()
            Discount.objects.all().delete()
            Course.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        # Create courses
        self.stdout.write('Creating courses...')
        courses = self.create_courses(options['courses'])
        
        # Create fee structures for courses
        self.stdout.write('Creating fee structures...')
        self.create_fee_structures(courses)
        
        # Create discounts
        self.stdout.write('Creating discounts...')
        self.create_discounts(courses)
        
        # Create enrollments
        self.stdout.write('Creating enrollments...')
        enrollments = self.create_enrollments(courses, options['enrollments'])
        
        # Create invoices and payments
        self.stdout.write('Creating invoices and payments...')
        self.create_invoices_and_payments(enrollments)
        
        # Display summary
        self.display_summary()

    def create_courses(self, count):
        """Create diverse courses with realistic Kuwaiti context"""
        
        course_data = [
            # Language Courses
            ('Arabic Language Fundamentals', 'ARA', 'regular', 'Learn Classical Arabic grammar and composition', 6, 'months'),
            ('English Communication', 'ENG', 'regular', 'Improve English speaking and writing skills', 4, 'months'),
            ('French for Beginners', 'FRE', 'regular', 'Introduction to French language and culture', 5, 'months'),
            
            # Islamic Studies
            ('Quran Recitation and Tajweed', 'QUR', 'regular', 'Perfect Quranic recitation with proper Tajweed', 8, 'months'),
            ('Islamic History and Civilization', 'ISH', 'regular', 'Study of Islamic history and contributions', 6, 'months'),
            ('Hadith Studies', 'HAD', 'regular', 'Understanding and memorizing important Hadiths', 4, 'months'),
            
            # Mathematics and Sciences
            ('Advanced Mathematics', 'MAT', 'intensive', 'Advanced mathematical concepts and problem solving', 3, 'months'),
            ('Physics for High School', 'PHY', 'regular', 'Comprehensive physics course for students', 5, 'months'),
            ('Chemistry Laboratory', 'CHE', 'regular', 'Hands-on chemistry experiments and theory', 4, 'months'),
            ('Computer Programming', 'PRG', 'intensive', 'Learn Python and web development basics', 3, 'months'),
            
            # Arts and Culture
            ('Kuwaiti Traditional Arts', 'KTA', 'workshop', 'Learn traditional Kuwaiti handicrafts and arts', 2, 'months'),
            ('Calligraphy Workshop', 'CAL', 'workshop', 'Arabic calligraphy techniques and practice', 6, 'weeks'),
            ('Music Theory and Practice', 'MUS', 'regular', 'Learn music theory and instrument practice', 4, 'months'),
            
            # Life Skills
            ('Business Entrepreneurship', 'BUS', 'intensive', 'Starting and managing a small business', 2, 'months'),
            ('Digital Literacy', 'DIG', 'regular', 'Computer skills and internet safety', 3, 'months'),
            ('Public Speaking', 'SPK', 'workshop', 'Develop confidence in public speaking', 4, 'weeks'),
            
            # Summer Programs
            ('Summer Science Camp', 'SSC', 'summer', 'Fun science experiments for young learners', 4, 'weeks'),
            ('Robotics Workshop', 'ROB', 'summer', 'Build and program simple robots', 3, 'weeks'),
            ('Creative Writing', 'CRW', 'summer', 'Express creativity through writing', 6, 'weeks'),
            
            # Tutorial Programs
            ('Math Tutoring Grade 10', 'MT10', 'tutorial', 'Supplementary math support for Grade 10', 8, 'months'),
            ('English Tutoring Grade 12', 'ET12', 'tutorial', 'University preparation English course', 10, 'months'),
        ]
        
        instructors = [
            'Dr. Ahmed Al-Sabah', 'Prof. Fatima Al-Rashid', 'Mr. Omar Abdullah',
            'Ms. Nadia Hussein', 'Dr. Khalid Al-Mutawa', 'Prof. Aisha Al-Qattan',
            'Mr. Yousef Al-Ahmad', 'Ms. Mariam Al-Kandari', 'Dr. Saad Al-Hajri',
            'Prof. Hind Al-Sabri', 'Mr. Faisal Al-Ajmi', 'Ms. Reem Al-Shammari'
        ]
        
        courses = []
        for i, (name, code_prefix, course_type, description, duration, unit) in enumerate(course_data[:count]):
            # Generate unique course code
            course_code = f"{code_prefix}{101 + i}"
            
            # Random start date (within next 3 months)
            start_date = self.fake.date_between(start_date=date.today(), end_date=date.today() + timedelta(days=90))
            
            # Calculate end date based on duration
            if unit == 'weeks':
                end_date = start_date + timedelta(weeks=duration)
            elif unit == 'months':
                end_date = start_date + timedelta(days=duration * 30)
            else:
                end_date = start_date + timedelta(days=duration)
            
            course = Course.objects.create(
                name=name,
                description=description,
                course_code=course_code,
                course_type=course_type,
                duration=duration,
                duration_unit=unit,
                start_date=start_date,
                end_date=end_date,
                max_students=random.randint(15, 35),
                min_age=random.choice([None, 8, 10, 12, 16]),
                max_age=random.choice([None, 18, 25, 35]),
                status=random.choices(['active', 'inactive', 'coming_soon'], weights=[0.8, 0.1, 0.1])[0],
                instructor_name=random.choice(instructors)
            )
            courses.append(course)
            
        self.stdout.write(self.style.SUCCESS(f'Created {len(courses)} courses'))
        return courses

    def create_fee_structures(self, courses):
        """Create realistic fee structures for courses"""
        
        fee_types = [
            ('tuition', 'monthly'),
            ('registration', 'one_time'),
            ('materials', 'one_time'),
            ('exam', 'one_time'),
            ('activity', 'monthly'),
        ]
        
        # Base fees in KWD
        base_fees = {
            'tuition': {'regular': 45.000, 'intensive': 60.000, 'summer': 35.000, 'workshop': 25.000, 'tutorial': 30.000},
            'registration': 15.000,
            'materials': 20.000,
            'exam': 10.000,
            'activity': 8.000,
        }
        
        fee_count = 0
        for course in courses:
            for fee_type, frequency in fee_types:
                # Not all courses have all fee types
                if random.random() < 0.7:  # 70% chance of having each fee type
                    if fee_type == 'tuition':
                        amount = base_fees['tuition'][course.course_type]
                        # Add some variation
                        amount += random.uniform(-5.000, 10.000)
                    else:
                        amount = base_fees[fee_type]
                        # Add some variation
                        amount += random.uniform(-2.000, 5.000)
                    
                    # Ensure positive amount
                    amount = max(amount, 5.000)
                    
                    FeeStructure.objects.create(
                        course=course,
                        fee_type=fee_type,
                        amount=Decimal(str(round(amount, 3))),
                        payment_frequency=frequency,
                        is_mandatory=fee_type in ['tuition', 'registration'],
                        due_date_offset=random.choice([0, 7, 14, 30]),
                        description=f"{fee_type.title()} fee for {course.name}"
                    )
                    fee_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {fee_count} fee structures'))

    def create_discounts(self, courses):
        """Create some discount offers"""
        
        discount_data = [
            ('Early Bird Discount', 'percentage', 10.000, 'all_fees'),
            ('Sibling Discount', 'percentage', 15.000, 'tuition_only'),
            ('Summer Special', 'fixed_amount', 20.000, 'all_fees'),
            ('Loyalty Discount', 'percentage', 5.000, 'tuition_only'),
            ('New Student Offer', 'fixed_amount', 15.000, 'registration_only'),
        ]
        
        for name, disc_type, value, applicability in discount_data:
            # Random validity period
            valid_from = self.fake.date_between(start_date=date.today() - timedelta(days=30), 
                                         end_date=date.today())
            valid_until = self.fake.date_between(start_date=date.today() + timedelta(days=30), 
                                          end_date=date.today() + timedelta(days=120))
            
            discount = Discount.objects.create(
                name=name,
                description=f"Special {name.lower()} for students",
                discount_type=disc_type,
                value=Decimal(str(value)),
                applicability=applicability,
                valid_from=valid_from,
                valid_until=valid_until,
                max_usage=random.choice([None, 50, 100, 200]),
                current_usage=random.randint(0, 30),
                is_active=random.choice([True, True, True, False]),  # 75% active
            )
            
            # Assign to some courses
            eligible_courses = random.sample(courses, k=random.randint(3, 8))
            discount.eligible_courses.set(eligible_courses)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(discount_data)} discounts'))

    def create_enrollments(self, courses, count):
        """Create student enrollments"""
        
        # Get all active students
        students = list(NewStudent.objects.filter(status='active'))
        if not students:
            self.stdout.write(self.style.ERROR('No active students found. Please create students first.'))
            return []
        
        active_courses = [c for c in courses if c.status == 'active']
        if not active_courses:
            self.stdout.write(self.style.ERROR('No active courses found.'))
            return []
        
        enrollments = []
        enrollment_count = min(count, len(students) * 3)  # Max 3 courses per student
        
        for _ in range(enrollment_count):
            student = random.choice(students)
            course = random.choice(active_courses)
            
            # Check if already enrolled
            if StudentEnrollment.objects.filter(student=student, course=course).exists():
                continue
            
            # Check course capacity
            current_enrollments = course.enrollments.filter(status='active').count()
            if current_enrollments >= course.max_students:
                continue
            
            # Random enrollment date (last 30 days)
            enrollment_date = self.fake.date_between(
                start_date=date.today() - timedelta(days=30),
                end_date=date.today()
            )
            
            enrollment = StudentEnrollment.objects.create(
                student=student,
                course=course,
                enrollment_date=enrollment_date,
                status=random.choices(
                    ['active', 'completed', 'dropped', 'pending'],
                    weights=[0.7, 0.15, 0.1, 0.05]
                )[0],
                enrollment_notes=self.fake.text(max_nb_chars=100) if random.random() < 0.3 else '',
            )
            enrollments.append(enrollment)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(enrollments)} enrollments'))
        return enrollments

    def create_invoices_and_payments(self, enrollments):
        """Create invoices and payments for enrollments"""
        
        # Get or create a staff user
        staff_user, created = User.objects.get_or_create(
            username='fee_admin',
            defaults={
                'first_name': 'Fee',
                'last_name': 'Administrator',
                'email': 'admin@edupulse.com',
                'is_staff': True,
            }
        )
        
        invoice_count = 0
        payment_count = 0
        
        for enrollment in enrollments:
            # Create invoice for most enrollments (90%)
            if random.random() < 0.9:
                # Calculate subtotal from fee structures
                subtotal = enrollment.get_total_fees()
                
                # Random discount (20% chance)
                discount_amount = Decimal('0.000')
                applied_discount = None
                if random.random() < 0.2:
                    discounts = Discount.objects.filter(
                        is_active=True,
                        eligible_courses=enrollment.course
                    )
                    if discounts.exists():
                        applied_discount = random.choice(discounts)
                        if applied_discount.discount_type == 'percentage':
                            discount_amount = subtotal * (applied_discount.value / 100)
                        else:
                            discount_amount = min(applied_discount.value, subtotal)
                
                total_amount = subtotal - discount_amount
                
                # Random issue date (last 45 days)
                issue_date = self.fake.date_between(
                    start_date=enrollment.enrollment_date,
                    end_date=date.today()
                )
                
                # Due date 30 days from issue
                due_date = issue_date + timedelta(days=30)
                
                invoice = Invoice.objects.create(
                    enrollment=enrollment,
                    issue_date=issue_date,
                    due_date=due_date,
                    subtotal=subtotal,
                    discount_amount=discount_amount,
                    total_amount=total_amount,
                    status=random.choices(
                        ['draft', 'sent', 'paid', 'overdue'],
                        weights=[0.1, 0.4, 0.4, 0.1]
                    )[0],
                    applied_discount=applied_discount,
                    notes=self.fake.text(max_nb_chars=100) if random.random() < 0.2 else '',
                )
                invoice_count += 1
                
                # Create payments for paid/sent invoices
                if invoice.status in ['sent', 'paid']:
                    # Number of payments (full payment or installments)
                    num_payments = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
                    
                    if num_payments == 1:
                        # Full payment
                        payment_amount = total_amount
                    else:
                        # Installments
                        payment_amount = total_amount / num_payments
                    
                    payments_made = 0
                    for payment_num in range(num_payments):
                        # Some payments might be pending
                        if random.random() < 0.85:  # 85% completion rate
                            # Payment date after invoice date
                            payment_date = self.fake.date_between(
                                start_date=invoice.issue_date,
                                end_date=min(date.today(), invoice.due_date + timedelta(days=10))
                            )
                            
                            # Last payment might be slightly different due to rounding
                            if payment_num == num_payments - 1:
                                remaining_amount = total_amount - (payment_amount * payments_made)
                                payment_amount = remaining_amount
                            
                            Payment.objects.create(
                                enrollment=enrollment,
                                invoice=invoice,
                                amount=payment_amount,
                                payment_date=payment_date,
                                payment_method=random.choice([
                                    'cash', 'bank_transfer', 'credit_card', 
                                    'debit_card', 'online'
                                ]),
                                reference_number=self.fake.bothify(text='PAY-####-????'),
                                status=random.choices(
                                    ['completed', 'pending', 'failed'],
                                    weights=[0.85, 0.1, 0.05]
                                )[0],
                                processed_by=staff_user,
                                notes=self.fake.text(max_nb_chars=50) if random.random() < 0.15 else '',
                            )
                            payment_count += 1
                            payments_made += 1
                
                # Update invoice status based on payments
                from django.db import models
                total_paid = invoice.payments.filter(status='completed').aggregate(
                    total=models.Sum('amount')
                )['total'] or Decimal('0.000')
                
                if total_paid >= invoice.total_amount:
                    invoice.status = 'paid'
                elif total_paid > 0:
                    invoice.status = 'sent'
                elif invoice.due_date < date.today():
                    invoice.status = 'overdue'
                
                invoice.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {invoice_count} invoices'))
        self.stdout.write(self.style.SUCCESS(f'Created {payment_count} payments'))

    def display_summary(self):
        """Display a summary of created data"""
        from django.db import models
        
        self.stdout.write(self.style.SUCCESS('\n=== COURSE FEE DATA SUMMARY ==='))
        
        # Courses
        courses = Course.objects.all()
        active_courses = courses.filter(status='active')
        self.stdout.write(f'📚 Total Courses: {courses.count()}')
        self.stdout.write(f'   Active: {active_courses.count()}')
        self.stdout.write(f'   By Type: {dict(courses.values_list("course_type").annotate(models.Count("id")))}')
        
        # Enrollments
        enrollments = StudentEnrollment.objects.all()
        active_enrollments = enrollments.filter(status='active')
        self.stdout.write(f'\n👥 Total Enrollments: {enrollments.count()}')
        self.stdout.write(f'   Active: {active_enrollments.count()}')
        
        # Financial Summary
        from django.db import models
        total_invoices = Invoice.objects.count()
        total_revenue = Payment.objects.filter(status='completed').aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.000')
        pending_payments = Payment.objects.filter(status='pending').aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.000')
        
        self.stdout.write(f'\n💰 Financial Overview:')
        self.stdout.write(f'   Total Invoices: {total_invoices}')
        self.stdout.write(f'   Revenue Collected: {total_revenue} KWD')
        self.stdout.write(f'   Pending Payments: {pending_payments} KWD')
        
        # Discounts
        discounts = Discount.objects.all()
        active_discounts = discounts.filter(is_active=True)
        self.stdout.write(f'\n🎁 Discounts: {discounts.count()} total, {active_discounts.count()} active')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Course fee data creation completed!'))
        self.stdout.write('🌐 Access the system at: http://127.0.0.1:8000/coursefee/')
        self.stdout.write('🛠️  Admin interface: http://127.0.0.1:8000/admin/') 