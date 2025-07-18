from django.core.management.base import BaseCommand
from django.utils import timezone
from xstudent.models import NewStudent
import random
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Create dummy student data for testing the attendance system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=25,
            help='Number of students to create (default: 25)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing students before creating new ones'
        )

    def handle(self, *args, **options):
        if options['clear']:
            NewStudent.objects.all().delete()
            self.stdout.write(
                self.style.WARNING('Cleared all existing students.')
            )

        count = options['count']
        
        # Sample data lists
        first_names_male = [
            'Ahmed', 'Mohammed', 'Ali', 'Omar', 'Khalid', 'Saad', 'Faisal', 'Abdullah', 
            'Yousef', 'Salem', 'Mansour', 'Fahad', 'Nawaf', 'Rakan', 'Turki', 'Majed'
        ]
        
        first_names_female = [
            'Fatima', 'Aisha', 'Sara', 'Noor', 'Maryam', 'Zahra', 'Hala', 'Noura', 
            'Reem', 'Lina', 'Huda', 'Rana', 'Dana', 'Lara', 'Maya', 'Zeinab'
        ]
        
        last_names = [
            'Al-Ahmad', 'Al-Mohammed', 'Al-Ali', 'Al-Omar', 'Al-Khalid', 'Al-Saad',
            'Al-Faisal', 'Al-Abdullah', 'Al-Yousef', 'Al-Salem', 'Al-Mansour',
            'Al-Fahad', 'Al-Nawaf', 'Al-Rakan', 'Al-Turki', 'Al-Majed', 'Al-Hassan',
            'Al-Hussein', 'Al-Rashid', 'Al-Sabah', 'Al-Thani', 'Al-Maktoum'
        ]
        
        schools = [
            'Kuwait International School', 'Al-Bayan Bilingual School', 
            'Kuwait English School', 'American School of Kuwait',
            'New English School', 'Universal American School',
            'Kuwait National English School', 'Al-Rowad School'
        ]
        
        grades = ['Grade 6', 'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12']
        
        programs = [
            'Mathematics Excellence', 'Science Advanced', 'English Literature',
            'Arabic Studies', 'Computer Science', 'Arts & Creativity',
            'Sports & Athletics', 'Leadership Development'
        ]
        
        areas = [
            'Hawalli', 'Salmiya', 'Kuwait City', 'Jabriya', 'Mishref', 
            'Bayan', 'Salwa', 'Mahboula', 'Fintas', 'Mangaf'
        ]
        
        cities = ['Kuwait City', 'Hawalli', 'Farwaniya', 'Mubarak Al-Kabeer', 'Ahmadi', 'Jahra']
        
        occupations = [
            'Engineer', 'Doctor', 'Teacher', 'Business Manager', 'Government Employee',
            'Lawyer', 'Accountant', 'Sales Manager', 'IT Specialist', 'Nurse'
        ]
        
        companies = [
            'Kuwait Oil Company', 'NBK', 'Gulf Bank', 'KFH', 'Zain Kuwait',
            'Ooredoo Kuwait', 'Ministry of Education', 'Ministry of Health',
            'KIPCO', 'Agility', 'KGL', 'Warba Bank'
        ]

        created_students = []
        
        for i in range(count):
            # Randomly choose gender
            gender = random.choice(['M', 'F'])
            
            # Select appropriate first name based on gender
            if gender == 'M':
                first_name = random.choice(first_names_male)
            else:
                first_name = random.choice(first_names_female)
            
            last_name = random.choice(last_names)
            student_name = f"{first_name} {last_name}"
            
            # Generate birth date (age between 11-18)
            age = random.randint(11, 18)
            birth_date = date.today() - timedelta(days=age * 365 + random.randint(0, 365))
            
            # Generate email
            email = f"{first_name.lower()}.{last_name.lower().replace('-', '').replace('al', '')}@student.edu.kw"
            
            # Select random school, grade, program
            school = random.choice(schools)
            grade = random.choice(grades)
            program = random.choice(programs)
            
            # Father details
            father_name = f"{random.choice(first_names_male)} {last_name}"
            father_occupation = random.choice(occupations)
            father_company = random.choice(companies)
            father_mobile = f"+965{random.randint(50000000, 99999999)}"
            father_email = f"{father_name.split()[0].lower()}.{last_name.lower().replace('-', '').replace('al', '')}@email.com"
            
            # Mother details
            mother_first = random.choice(first_names_female)
            mother_name = f"{mother_first} {random.choice(last_names)}"
            mother_occupation = random.choice(occupations)
            mother_company = random.choice(companies)
            mother_mobile = f"+965{random.randint(50000000, 99999999)}"
            mother_email = f"{mother_first.lower()}.mother@email.com"
            
            # Address details
            area = random.choice(areas)
            city = random.choice(cities)
            
            # Mobile number selection
            mobile_choice = random.choice(['Father', 'Mother'])
            mobile_no = father_mobile if mobile_choice == 'Father' else mother_mobile
            
            try:
                student = NewStudent.objects.create(
                    status='active',
                    student_name=student_name,
                    gender=gender,
                    school_name=school,
                    grade=grade,
                    program=program,
                    date_of_birth=birth_date,
                    email_id=email,
                    
                    # Father details
                    father_name=father_name,
                    father_occupation=father_occupation,
                    father_company_name=father_company,
                    father_mobile_no=father_mobile,
                    father_email_id=father_email,
                    
                    # Mother details
                    mother_name=mother_name,
                    mother_occupation=mother_occupation,
                    mother_company_name=mother_company,
                    mother_mobile_no=mother_mobile,
                    mother_email_id=mother_email,
                    
                    # Address
                    address_line_1=f"Block {random.randint(1, 20)}, Street {random.randint(1, 50)}",
                    address_line_2=f"Building {random.randint(1, 100)}, Apt {random.randint(1, 20)}",
                    area=area,
                    country="Kuwait",
                    state_emirates_province="Kuwait",
                    city=city,
                    postal_code=f"{random.randint(10000, 99999)}",
                    telephone=f"+965{random.randint(20000000, 29999999)}",
                    
                    # Mobile selection
                    select_mobile_number=mobile_choice,
                    mobile_no=mobile_no,
                )
                
                created_students.append(student)
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating student {student_name}: {str(e)}')
                )
                continue
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(created_students)} students!')
        )
        
        # Display summary
        self.stdout.write("\n" + "="*50)
        self.stdout.write("SUMMARY OF CREATED STUDENTS:")
        self.stdout.write("="*50)
        
        for student in created_students[:10]:  # Show first 10
            self.stdout.write(f"• {student.student_name} - {student.grade} - {student.program}")
        
        if len(created_students) > 10:
            self.stdout.write(f"... and {len(created_students) - 10} more students")
        
        # Show statistics
        grades_count = {}
        programs_count = {}
        gender_count = {'M': 0, 'F': 0}
        
        for student in created_students:
            grades_count[student.grade] = grades_count.get(student.grade, 0) + 1
            programs_count[student.program] = programs_count.get(student.program, 0) + 1
            gender_count[student.gender] += 1
        
        self.stdout.write("\nSTATISTICS:")
        self.stdout.write("-" * 20)
        self.stdout.write(f"Total Students: {len(created_students)}")
        self.stdout.write(f"Male: {gender_count['M']}, Female: {gender_count['F']}")
        
        self.stdout.write("\nGrades Distribution:")
        for grade, count in sorted(grades_count.items()):
            self.stdout.write(f"  {grade}: {count} students")
        
        self.stdout.write("\nPrograms Distribution:")
        for program, count in sorted(programs_count.items()):
            self.stdout.write(f"  {program}: {count} students")
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write("✅ Dummy data creation completed!")
        self.stdout.write("You can now test the attendance system with realistic data.")
        self.stdout.write("="*50) 