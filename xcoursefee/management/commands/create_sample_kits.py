from django.core.management.base import BaseCommand
from decimal import Decimal
from xcoursefee.models import Kit, Course, CourseKit, StudentEnrollment, KitFee
from xstudent.models import NewStudent


class Command(BaseCommand):
    help = 'Create sample kit data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing kit data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing kit data...')
            KitFee.objects.all().delete()
            CourseKit.objects.all().delete()
            Kit.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared existing kit data'))

        # Create sample kits
        kits_data = [
            {
                'name': 'Basic Programming Kit',
                'kit_code': 'PROG001',
                'description': 'Essential materials for programming courses including notebook, pens, and USB drive.',
                'price': Decimal('25.500'),
                'stock_quantity': 50,
                'minimum_stock': 10,
                'contents': 'Notebook, 2 pens, USB drive (8GB), Course materials',
                'supplier': 'TechSupply Kuwait',
                'supplier_contact': '+965 2234 5678',
                'status': 'available',
                'is_mandatory': True,
            },
            {
                'name': 'Electronics Lab Kit',
                'kit_code': 'ELEC001',
                'description': 'Complete electronics kit with breadboard, resistors, and basic components.',
                'price': Decimal('75.000'),
                'stock_quantity': 30,
                'minimum_stock': 5,
                'contents': 'Breadboard, Resistors set, LEDs, Jumper wires, Multimeter',
                'supplier': 'Electronics Store Kuwait',
                'supplier_contact': '+965 2345 6789',
                'status': 'available',
                'is_mandatory': True,
            },
            {
                'name': 'Art & Design Kit',
                'kit_code': 'ART001',
                'description': 'Creative supplies for art and design courses.',
                'price': Decimal('45.250'),
                'stock_quantity': 25,
                'minimum_stock': 8,
                'contents': 'Sketchbook, Pencils set, Markers, Ruler, Eraser',
                'supplier': 'Creative Supplies KW',
                'supplier_contact': '+965 2456 7890',
                'status': 'available',
                'is_mandatory': False,
            },
            {
                'name': 'Science Lab Kit',
                'kit_code': 'SCI001',
                'description': 'Basic laboratory equipment for science experiments.',
                'price': Decimal('65.750'),
                'stock_quantity': 8,  # Low stock to test alerts
                'minimum_stock': 10,
                'contents': 'Test tubes, Beakers, Safety goggles, Lab coat, pH strips',
                'supplier': 'Scientific Equipment Ltd',
                'supplier_contact': '+965 2567 8901',
                'status': 'available',
                'is_mandatory': True,
            },
            {
                'name': 'Business Studies Kit',
                'kit_code': 'BUS001',
                'description': 'Materials for business and management courses.',
                'price': Decimal('30.000'),
                'stock_quantity': 0,  # Out of stock
                'minimum_stock': 15,
                'contents': 'Calculator, Notebook, Business case studies, Presentation materials',
                'supplier': 'Business Supplies Co',
                'supplier_contact': '+965 2678 9012',
                'status': 'out_of_stock',
                'is_mandatory': False,
            },
        ]

        created_kits = []
        for kit_data in kits_data:
            kit, created = Kit.objects.get_or_create(
                kit_code=kit_data['kit_code'],
                defaults=kit_data
            )
            if created:
                created_kits.append(kit)
                self.stdout.write(f'Created kit: {kit.name}')
            else:
                self.stdout.write(f'Kit already exists: {kit.name}')

        self.stdout.write(self.style.SUCCESS(f'Created {len(created_kits)} new kits'))

        # Link kits to courses if courses exist
        courses = Course.objects.filter(status='active')
        if courses.exists():
            self.stdout.write('Linking kits to courses...')
            
            # Get some kits
            prog_kit = Kit.objects.filter(kit_code='PROG001').first()
            elec_kit = Kit.objects.filter(kit_code='ELEC001').first()
            art_kit = Kit.objects.filter(kit_code='ART001').first()
            sci_kit = Kit.objects.filter(kit_code='SCI001').first()
            
            course_kit_links = 0
            for course in courses[:3]:  # Link to first 3 courses
                # Link programming kit to all courses
                if prog_kit:
                    course_kit, created = CourseKit.objects.get_or_create(
                        course=course,
                        kit=prog_kit,
                        defaults={
                            'is_required': True,
                            'notes': 'Basic kit required for all students'
                        }
                    )
                    if created:
                        course_kit_links += 1
                
                # Link specific kits based on course name
                if 'programming' in course.name.lower() or 'computer' in course.name.lower():
                    if elec_kit:
                        course_kit, created = CourseKit.objects.get_or_create(
                            course=course,
                            kit=elec_kit,
                            defaults={'is_required': True}
                        )
                        if created:
                            course_kit_links += 1
                
                elif 'art' in course.name.lower() or 'design' in course.name.lower():
                    if art_kit:
                        course_kit, created = CourseKit.objects.get_or_create(
                            course=course,
                            kit=art_kit,
                            defaults={'is_required': True}
                        )
                        if created:
                            course_kit_links += 1
                
                elif 'science' in course.name.lower() or 'lab' in course.name.lower():
                    if sci_kit:
                        course_kit, created = CourseKit.objects.get_or_create(
                            course=course,
                            kit=sci_kit,
                            defaults={'is_required': True}
                        )
                        if created:
                            course_kit_links += 1
            
            self.stdout.write(self.style.SUCCESS(f'Created {course_kit_links} course-kit links'))

            # Create sample kit fees for existing enrollments
            enrollments = StudentEnrollment.objects.filter(status='active')[:5]
            kit_fees_created = 0
            
            for enrollment in enrollments:
                course_kits = enrollment.course.course_kits.all()
                for course_kit in course_kits:
                    kit_fee, created = KitFee.objects.get_or_create(
                        enrollment=enrollment,
                        course_kit=course_kit,
                        defaults={
                            'amount': course_kit.kit.price,
                            'payment_status': 'pending',
                            'delivery_status': 'pending',
                        }
                    )
                    if created:
                        kit_fees_created += 1
            
            self.stdout.write(self.style.SUCCESS(f'Created {kit_fees_created} sample kit fee entries'))
        
        else:
            self.stdout.write(self.style.WARNING('No active courses found. Create courses first to link kits.'))

        self.stdout.write(
            self.style.SUCCESS(
                '\nSample kit data created successfully!\n'
                'You can now:\n'
                '- View kits at /coursefee/kits/\n'
                '- Manage course-kit links at /coursefee/course-kits/\n'
                '- Process kit fees at /coursefee/kit-fees/\n'
                '- Access admin panel for detailed management'
            )
        ) 