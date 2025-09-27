from django.core.management.base import BaseCommand
from schoolmgmt.models import IDCardTemplate

class Command(BaseCommand):
    help = 'Save all ID card design templates to database'

    def handle(self, *args, **options):
        templates = [
            {
                'template_id': '1',
                'name': 'Design 1 - Classic Blue',
                'template_type': 'gradient',
                'background_gradient': 'linear-gradient(180deg, #1e3c72 0%, #2a5298 30%, #667eea 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'logo': True},
                    'body': {'photo': True, 'qr_code': True, 'details': ['class', 'roll', 'father', 'dob', 'session', 'mobile']},
                    'footer': {'validity': True}
                }
            },
            {
                'template_id': '2',
                'name': 'Design 2 - Modern Green',
                'template_type': 'gradient',
                'background_gradient': 'linear-gradient(180deg, #134e5e 0%, #71b280 30%, #a8e6cf 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'logo': True},
                    'body': {'photo': True, 'qr_code': True, 'details': ['class', 'roll', 'father', 'dob', 'session', 'mobile']},
                    'footer': {'validity': True}
                }
            },
            {
                'template_id': '3',
                'name': 'Design 3 - Professional Purple',
                'template_type': 'gradient',
                'background_gradient': 'linear-gradient(180deg, #4a148c 0%, #7b1fa2 30%, #ba68c8 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'logo': True},
                    'body': {'photo': True, 'qr_code': True, 'details': ['class', 'roll', 'father', 'dob', 'session', 'mobile']},
                    'footer': {'validity': True}
                }
            },
            {
                'template_id': '4',
                'name': 'Design 4 - Elegant Red',
                'template_type': 'gradient',
                'background_gradient': 'linear-gradient(180deg, #b71c1c 0%, #d32f2f 30%, #f44336 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'logo': True},
                    'body': {'photo': True, 'qr_code': True, 'details': ['class', 'roll', 'father', 'dob', 'session', 'mobile']},
                    'footer': {'validity': True}
                }
            },
            {
                'template_id': '5',
                'name': 'Design 5 - Corporate Gray',
                'template_type': 'gradient',
                'background_gradient': 'linear-gradient(180deg, #263238 0%, #455a64 30%, #78909c 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'logo': True},
                    'body': {'photo': True, 'qr_code': True, 'details': ['class', 'roll', 'father', 'dob', 'session', 'mobile']},
                    'footer': {'validity': True}
                }
            },
            {
                'template_id': '6',
                'name': 'Design 6 - Vibrant Orange',
                'template_type': 'gradient',
                'background_gradient': 'linear-gradient(180deg, #e65100 0%, #ff9800 30%, #ffb74d 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'logo': True},
                    'body': {'photo': True, 'qr_code': True, 'details': ['class', 'roll', 'father', 'dob', 'session', 'mobile']},
                    'footer': {'validity': True}
                }
            },
            {
                'template_id': '7',
                'name': 'Design 7 - Ocean Teal',
                'template_type': 'gradient',
                'background_gradient': 'linear-gradient(180deg, #006064 0%, #00838f 30%, #4dd0e1 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'logo': True},
                    'body': {'photo': True, 'qr_code': True, 'details': ['class', 'roll', 'father', 'dob', 'session', 'mobile']},
                    'footer': {'validity': True}
                }
            },
            {
                'template_id': '8',
                'name': 'Design 8 - Royal Gold',
                'template_type': 'gradient',
                'background_gradient': 'linear-gradient(180deg, #ff6f00 0%, #ff8f00 30%, #ffb300 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'logo': True},
                    'body': {'photo': True, 'qr_code': True, 'details': ['class', 'roll', 'father', 'dob', 'session', 'mobile']},
                    'footer': {'validity': True}
                }
            },
            {
                'template_id': '9',
                'name': 'Design 9 - Dark Navy',
                'template_type': 'gradient',
                'background_gradient': 'linear-gradient(180deg, #0d47a1 0%, #1565c0 30%, #1976d2 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'logo': True},
                    'body': {'photo': True, 'qr_code': True, 'details': ['class', 'roll', 'father', 'dob', 'session', 'mobile']},
                    'footer': {'validity': True}
                }
            },
            {
                'template_id': '10',
                'name': 'Design 10 - Sunset Pink',
                'template_type': 'gradient',
                'background_gradient': 'linear-gradient(180deg, #ad1457 0%, #c2185b 30%, #e91e63 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'logo': True},
                    'body': {'photo': True, 'qr_code': True, 'details': ['class', 'roll', 'father', 'dob', 'session', 'mobile']},
                    'footer': {'validity': True}
                }
            },
            {
                'template_id': 'school1',
                'name': 'School Layout 1 - Academic Classic',
                'template_type': 'school',
                'background_gradient': 'linear-gradient(180deg, #1a237e 0%, #3949ab 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'logo': True, 'style': 'academic'},
                    'body': {'photo': True, 'student_id': True, 'details': ['class', 'roll', 'father', 'dob', 'session']},
                    'footer': {'validity': True, 'style': 'formal'}
                },
                'html_template': 'school1_layout'
            },
            {
                'template_id': 'school2',
                'name': 'School Layout 2 - Modern Campus',
                'template_type': 'school',
                'background_gradient': 'linear-gradient(45deg, #00bcd4 0%, #009688 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'logo': True, 'style': 'modern'},
                    'body': {'photo': True, 'circular_photo': True, 'grid_details': True},
                    'footer': {'validity': True, 'style': 'modern'}
                },
                'html_template': 'school2_layout'
            },
            {
                'template_id': 'school3',
                'name': 'School Layout 3 - Institutional Pro',
                'template_type': 'school',
                'background_gradient': 'linear-gradient(135deg, #37474f 0%, #263238 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'logo': True, 'style': 'institutional'},
                    'body': {'photo': True, 'seal_overlay': True, 'detailed_info': True},
                    'footer': {'validity': True, 'style': 'professional'}
                },
                'html_template': 'school3_layout'
            },
            {
                'template_id': 's4',
                'name': 'Layout 4 - Hexagon Tech',
                'template_type': 'special',
                'background_gradient': 'linear-gradient(60deg, #667eea 0%, #764ba2 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'hexagon_design': True},
                    'body': {'photo': True, 'hexagon_photo': True, 'tech_style': True},
                    'footer': {'validity': True}
                },
                'html_template': 's4_layout'
            },
            {
                'template_id': 's5',
                'name': 'Layout 5 - Diagonal Split',
                'template_type': 'special',
                'background_gradient': 'linear-gradient(45deg, #ff6b6b 0%, #4ecdc4 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'diagonal_overlay': True},
                    'body': {'photo': True, 'rotated_elements': True, 'creative_layout': True},
                    'footer': {'validity': True}
                },
                'html_template': 's5_layout'
            },
            {
                'template_id': 's6',
                'name': 'Layout 6 - Badge Style',
                'template_type': 'special',
                'background_gradient': 'radial-gradient(circle at 30% 20%, #ffd89b 0%, #19547b 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'badge_style': True},
                    'body': {'photo': True, 'circular_photo': True, 'badge_layout': True},
                    'footer': {'validity': True}
                },
                'html_template': 's6_layout'
            },
            {
                'template_id': 's7',
                'name': 'Layout 7 - Mobile Card',
                'template_type': 'special',
                'background_gradient': 'linear-gradient(180deg, #2c3e50 0%, #34495e 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'mobile_style': True},
                    'body': {'photo': True, 'compact_layout': True, 'mobile_optimized': True},
                    'footer': {'validity': True}
                },
                'html_template': 's7_layout'
            },
            {
                'template_id': 's8',
                'name': 'Layout 8 - Spectrum Wave',
                'template_type': 'special',
                'background_gradient': 'linear-gradient(90deg, #ff0080, #ff8c00, #40e0d0, #ee82ee, #98fb98)',
                'layout_structure': {
                    'header': {'school_info': True, 'spectrum_design': True},
                    'body': {'photo': True, 'wave_effects': True, 'colorful_layout': True},
                    'footer': {'validity': True}
                },
                'html_template': 's8_layout'
            },
            {
                'template_id': 's9',
                'name': 'Layout 9 - Fire Gradient',
                'template_type': 'special',
                'background_gradient': 'linear-gradient(135deg, #ff4757 0%, #ff3838 50%, #ff6b6b 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'fire_effects': True},
                    'body': {'photo': True, 'dramatic_shadows': True, 'fire_theme': True},
                    'footer': {'validity': True}
                },
                'html_template': 's9_layout'
            },
            {
                'template_id': 's10',
                'name': 'Layout 10 - Crystal Modern',
                'template_type': 'special',
                'background_gradient': 'linear-gradient(45deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%)',
                'layout_structure': {
                    'header': {'school_info': True, 'crystal_effects': True},
                    'body': {'photo': True, 'glass_morphism': True, 'modern_layout': True},
                    'footer': {'validity': True}
                },
                'html_template': 's10_layout'
            }
        ]

        for template_data in templates:
            template, created = IDCardTemplate.objects.get_or_create(
                template_id=template_data['template_id'],
                defaults=template_data
            )
            if created:
                self.stdout.write(f"Created template: {template.name}")
            else:
                self.stdout.write(f"Template already exists: {template.name}")

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {len(templates)} templates'))