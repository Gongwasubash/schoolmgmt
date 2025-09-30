from django.core.management.base import BaseCommand
from schoolmgmt.models import Blog, HeroSlider

class Command(BaseCommand):
    help = 'Create sample blog and hero slider data'

    def handle(self, *args, **options):
        # Create sample blogs
        blogs_data = [
            {
                'heading': 'Welcome to New Academic Year 2024-25',
                'description': 'We are excited to welcome all students and parents to the new academic year. This year brings new opportunities, challenges, and exciting learning experiences for all our students.'
            },
            {
                'heading': 'Annual Sports Day Celebration',
                'description': 'Our annual sports day was a grand success with students participating in various athletic events. The day was filled with enthusiasm, team spirit, and healthy competition.'
            },
            {
                'heading': 'Science Fair 2024 Results',
                'description': 'Students showcased their innovative projects at the annual science fair. The creativity and scientific thinking displayed by our students was truly remarkable.'
            }
        ]

        for blog_data in blogs_data:
            blog, created = Blog.objects.get_or_create(
                heading=blog_data['heading'],
                defaults={'description': blog_data['description']}
            )
            if created:
                self.stdout.write(f'Created blog: {blog.heading}')
            else:
                self.stdout.write(f'Blog already exists: {blog.heading}')

        # Create sample hero slider entries
        hero_data = [
            {'title': 'Excellence in Education', 'order': 1},
            {'title': 'Building Future Leaders', 'order': 2},
            {'title': 'Nurturing Young Minds', 'order': 3}
        ]

        for hero_item in hero_data:
            slider, created = HeroSlider.objects.get_or_create(
                title=hero_item['title'],
                defaults={'order': hero_item['order']}
            )
            if created:
                self.stdout.write(f'Created hero slider: {slider.title}')
            else:
                self.stdout.write(f'Hero slider already exists: {slider.title}')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))