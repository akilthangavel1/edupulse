from django.core.management.base import BaseCommand
from django.db import transaction
from xmark.models import GradeScale, AssessmentType, Subject
from xcoursefee.models import Course


class Command(BaseCommand):
    help = 'Create sample data for marks system'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample marks data...'))

        try:
            with transaction.atomic():
                # Create Grade Scales
                grade_scales = [
                    {'grade': 'A+', 'min_percentage': 95, 'max_percentage': 100, 'grade_points': 4.00, 'description': 'Excellent'},
                    {'grade': 'A', 'min_percentage': 90, 'max_percentage': 94.99, 'grade_points': 3.70, 'description': 'Very Good'},
                    {'grade': 'B+', 'min_percentage': 85, 'max_percentage': 89.99, 'grade_points': 3.30, 'description': 'Good'},
                    {'grade': 'B', 'min_percentage': 80, 'max_percentage': 84.99, 'grade_points': 3.00, 'description': 'Above Average'},
                    {'grade': 'C+', 'min_percentage': 75, 'max_percentage': 79.99, 'grade_points': 2.70, 'description': 'Average'},
                    {'grade': 'C', 'min_percentage': 70, 'max_percentage': 74.99, 'grade_points': 2.30, 'description': 'Below Average'},
                    {'grade': 'D+', 'min_percentage': 65, 'max_percentage': 69.99, 'grade_points': 2.00, 'description': 'Poor'},
                    {'grade': 'D', 'min_percentage': 60, 'max_percentage': 64.99, 'grade_points': 1.70, 'description': 'Very Poor'},
                    {'grade': 'F', 'min_percentage': 0, 'max_percentage': 59.99, 'grade_points': 0.00, 'description': 'Fail'},
                ]

                for scale_data in grade_scales:
                    grade_scale, created = GradeScale.objects.get_or_create(
                        grade=scale_data['grade'],
                        defaults=scale_data
                    )
                    if created:
                        self.stdout.write(f'Created grade scale: {grade_scale.grade}')

                # Create Assessment Types
                assessment_types = [
                    {'name': 'Quiz 1', 'category': 'quiz', 'weight_percentage': 10.00, 'description': 'First quiz'},
                    {'name': 'Quiz 2', 'category': 'quiz', 'weight_percentage': 10.00, 'description': 'Second quiz'},
                    {'name': 'Midterm Exam', 'category': 'midterm', 'weight_percentage': 30.00, 'description': 'Midterm examination'},
                    {'name': 'Final Exam', 'category': 'final', 'weight_percentage': 40.00, 'description': 'Final examination'},
                    {'name': 'Assignment', 'category': 'assignment', 'weight_percentage': 10.00, 'description': 'Course assignment'},
                    {'name': 'Project', 'category': 'project', 'weight_percentage': 15.00, 'description': 'Course project'},
                    {'name': 'Lab Work', 'category': 'lab', 'weight_percentage': 15.00, 'description': 'Laboratory work'},
                    {'name': 'Participation', 'category': 'participation', 'weight_percentage': 5.00, 'description': 'Class participation'},
                ]

                for assessment_data in assessment_types:
                    assessment_type, created = AssessmentType.objects.get_or_create(
                        name=assessment_data['name'],
                        defaults=assessment_data
                    )
                    if created:
                        self.stdout.write(f'Created assessment type: {assessment_type.name}')

                # Create sample subjects for existing courses
                courses = Course.objects.filter(status='active')[:3]  # Get first 3 active courses
                
                if courses:
                    sample_subjects = [
                        {'name': 'Mathematics', 'code': 'MATH101', 'credit_hours': 3, 'instructor': 'Dr. Ahmed Hassan'},
                        {'name': 'English Language', 'code': 'ENG102', 'credit_hours': 3, 'instructor': 'Prof. Sarah Wilson'},
                        {'name': 'Science', 'code': 'SCI103', 'credit_hours': 4, 'instructor': 'Dr. Mohamed Ali'},
                        {'name': 'Computer Programming', 'code': 'CS104', 'credit_hours': 4, 'instructor': 'Mr. John Smith'},
                        {'name': 'Physics', 'code': 'PHY105', 'credit_hours': 3, 'instructor': 'Dr. Fatima Al-Zahra'},
                    ]

                    for i, subject_data in enumerate(sample_subjects):
                        if i < len(courses):
                            course = courses[i % len(courses)]
                            subject_data['course'] = course
                            subject_data['description'] = f'{subject_data["name"]} course for {course.name}'
                            
                            subject, created = Subject.objects.get_or_create(
                                code=subject_data['code'],
                                defaults=subject_data
                            )
                            if created:
                                self.stdout.write(f'Created subject: {subject.code} - {subject.name}')

                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully created sample marks data!\n'
                        f'- Grade scales: {GradeScale.objects.count()}\n'
                        f'- Assessment types: {AssessmentType.objects.count()}\n'
                        f'- Subjects: {Subject.objects.count()}'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating sample data: {str(e)}')
            ) 