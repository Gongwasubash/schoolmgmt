from django.core.management.base import BaseCommand
from schoolmgmt.models import Blog
from django.core.files.base import ContentFile
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate 10 blog posts with images'

    def handle(self, *args, **options):
        blog_data = [
            {
                'heading': 'Annual Sports Day Celebration',
                'description': 'Our school celebrated its annual sports day with great enthusiasm. Students participated in various athletic events including track and field, basketball, and football competitions. The event showcased the athletic talents of our students and promoted healthy competition and sportsmanship among all participants.',

            },
            {
                'heading': 'Science Exhibition 2024',
                'description': 'Students from grades 6-12 presented innovative science projects at our annual science exhibition. The event featured experiments in physics, chemistry, biology, and environmental science. Parents and guests were amazed by the creativity and scientific thinking demonstrated by our young scientists.',

            },
            {
                'heading': 'Cultural Festival Highlights',
                'description': 'Our multicultural festival brought together students from diverse backgrounds to celebrate unity in diversity. The event featured traditional dances, music performances, art exhibitions, and food stalls representing various cultures. It was a wonderful display of our school community spirit.',

            },
            {
                'heading': 'New Library Wing Opening',
                'description': 'We are excited to announce the opening of our new library wing, featuring modern facilities, digital resources, and comfortable reading spaces. The library now houses over 10,000 books, e-learning stations, and quiet study areas for students to enhance their learning experience.',

            },
            {
                'heading': 'Student Achievement Awards',
                'description': 'We proudly celebrate our students who have excelled in academics, sports, and extracurricular activities this semester. The award ceremony recognized outstanding achievements in various fields and motivated other students to strive for excellence in their chosen areas.',

            },
            {
                'heading': 'Environmental Awareness Campaign',
                'description': 'Our school launched a comprehensive environmental awareness campaign focusing on sustainability and eco-friendly practices. Students participated in tree planting, waste reduction initiatives, and educational workshops about climate change and environmental conservation.',

            },
            {
                'heading': 'Technology Integration Program',
                'description': 'We have successfully implemented new technology integration programs across all grade levels. Students now have access to tablets, interactive whiteboards, and coding classes that prepare them for the digital future while enhancing their learning experience.',

            },
            {
                'heading': 'Parent-Teacher Conference Success',
                'description': 'Our recent parent-teacher conference saw excellent participation from families. Teachers shared student progress reports, discussed individual learning plans, and collaborated with parents to support each child academic and personal development journey.',

            },
            {
                'heading': 'Art Competition Winners',
                'description': 'Congratulations to all participants in our inter-school art competition. Our students showcased exceptional creativity in painting, sculpture, and digital art categories. The winning artworks are now displayed in our school gallery for everyone to admire.',

            },
            {
                'heading': 'Community Service Initiative',
                'description': 'Our students actively participated in community service projects, including visiting elderly care homes, organizing charity drives, and helping local environmental cleanup efforts. These initiatives teach valuable lessons about social responsibility and community engagement.',

            }
        ]

        for i, blog in enumerate(blog_data, 1):
            try:
                # Check if existing images are available
                existing_images = ['Nepal_SOTW5-13-16leadfinal_1000x.webp', 'Ruby_Winter2022_800x.webp', 'thumb.jpg']
                image_to_use = existing_images[(i-1) % len(existing_images)]
                
                # Create blog post
                blog_post = Blog.objects.create(
                    heading=blog['heading'],
                    description=blog['description']
                )
                
                # Copy existing image from blog_images folder
                source_path = os.path.join(settings.MEDIA_ROOT, 'blog_images', image_to_use)
                if os.path.exists(source_path):
                    with open(source_path, 'rb') as f:
                        blog_post.photo.save(
                            f'blog_post_{i}_{image_to_use}',
                            ContentFile(f.read()),
                            save=True
                        )
                
                self.stdout.write(f'Created blog post: {blog["heading"]}')
                
            except Exception as e:
                self.stdout.write(f'Error creating blog {i}: {str(e)}')

        self.stdout.write(self.style.SUCCESS('Successfully populated 10 blog posts'))