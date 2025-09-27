from django.core.management.base import BaseCommand
from schoolmgmt.models import Student
import random

class Command(BaseCommand):
    help = 'Populate blank fields in Student model with random Nepali format text'

    def handle(self, *args, **options):
        # Nepali names and data
        nepali_first_names = [
            'राम', 'श्याम', 'गीता', 'सीता', 'हरि', 'कृष्ण', 'राधा', 'लक्ष्मी', 'सरस्वती', 'दुर्गा',
            'विष्णु', 'शिव', 'ब्रह्मा', 'इन्द्र', 'सुर्य', 'चन्द्र', 'अर्जुन', 'भीम', 'युधिष्ठिर', 'नकुल',
            'सहदेव', 'द्रौपदी', 'कुन्ती', 'गान्धारी', 'उर्मिला', 'मन्दोदरी', 'अहिल्या', 'तारा', 'सुमित्रा', 'कैकेयी'
        ]
        
        nepali_last_names = [
            'शर्मा', 'अधिकारी', 'पौडेल', 'गुरुङ', 'तामाङ', 'राई', 'लिम्बु', 'मगर', 'थापा', 'खत्री',
            'बस्नेत', 'पन्त', 'जोशी', 'उपाध्याय', 'आचार्य', 'भट्टराई', 'रेग्मी', 'काफ्ले', 'सुब्बा', 'दाहाल'
        ]
        
        nepali_places = [
            'काठमाडौं', 'पोखरा', 'भक्तपुर', 'ललितपुर', 'बिराटनगर', 'धरान', 'हेटौडा', 'भरतपुर', 'बुटवल', 'नेपालगञ्ज',
            'जनकपुर', 'वीरगञ्ज', 'त्रिभुवन', 'गोरखा', 'लमजुङ', 'तनहुँ', 'स्याङ्जा', 'पर्वत', 'बाग्लुङ', 'म्याग्दी'
        ]
        
        nepali_occupations = [
            'किसान', 'शिक्षक', 'डाक्टर', 'इन्जिनियर', 'व्यापारी', 'कर्मचारी', 'मजदुर', 'चालक', 'नर्स', 'वकिल',
            'पुलिस', 'सेना', 'बैंकर', 'लेखक', 'कलाकार', 'संगीतकार', 'खेलाडी', 'पत्रकार', 'राजनीतिज्ञ', 'समाजसेवी'
        ]
        
        nepali_qualifications = [
            'एसएलसी', 'प्लस टु', 'स्नातक', 'स्नातकोत्तर', 'एमफिल', 'पिएचडी', 'डिप्लोमा', 'सर्टिफिकेट', 'व्यावसायिक', 'प्राविधिक'
        ]
        
        religions = ['Hindu', 'Buddhist', 'Christian', 'Muslim', 'Other']
        
        students = Student.objects.all()
        updated_count = 0
        
        for student in students:
            updated = False
            
            # Fill blank name
            if not student.name or student.name.strip() == '':
                first_name = random.choice(nepali_first_names)
                last_name = random.choice(nepali_last_names)
                student.name = f"{first_name} {last_name}"
                updated = True
            
            # Fill blank father name
            if not student.father_name or student.father_name.strip() == '':
                first_name = random.choice(nepali_first_names)
                last_name = random.choice(nepali_last_names)
                student.father_name = f"{first_name} {last_name}"
                updated = True
            
            # Fill blank mother name
            if not student.mother_name or student.mother_name.strip() == '':
                first_name = random.choice(nepali_first_names)
                last_name = random.choice(nepali_last_names)
                student.mother_name = f"{first_name} {last_name}"
                updated = True
            
            # Fill blank address1
            if not student.address1 or student.address1.strip() == '':
                place = random.choice(nepali_places)
                ward = random.randint(1, 15)
                student.address1 = f"{place}-{ward}"
                updated = True
            
            # Fill blank city
            if not student.city or student.city.strip() == '':
                student.city = random.choice(nepali_places)
                updated = True
            
            # Fill blank religion
            if not student.religion or student.religion.strip() == '':
                student.religion = random.choice(religions)
                updated = True
            
            # Fill blank father occupation
            if not student.father_occupation or student.father_occupation.strip() == '':
                student.father_occupation = random.choice(nepali_occupations)
                updated = True
            
            # Fill blank mother occupation
            if not student.mother_occupation or student.mother_occupation.strip() == '':
                student.mother_occupation = random.choice(nepali_occupations)
                updated = True
            
            # Fill blank father qualification
            if not student.father_qualification or student.father_qualification.strip() == '':
                student.father_qualification = random.choice(nepali_qualifications)
                updated = True
            
            # Fill blank mother qualification
            if not student.mother_qualification or student.mother_qualification.strip() == '':
                student.mother_qualification = random.choice(nepali_qualifications)
                updated = True
            
            # Fill blank father citizen
            if not student.father_citizen or student.father_citizen.strip() == '':
                district_code = random.randint(10, 77)
                year = random.randint(40, 80)
                number = random.randint(100000, 999999)
                student.father_citizen = f"{district_code}-{year}-{number}"
                updated = True
            
            # Fill blank mother citizen
            if not student.mother_citizen or student.mother_citizen.strip() == '':
                district_code = random.randint(10, 77)
                year = random.randint(40, 80)
                number = random.randint(100000, 999999)
                student.mother_citizen = f"{district_code}-{year}-{number}"
                updated = True
            
            # Fill blank transport
            if not student.transport or student.transport.strip() == '':
                transport_options = [
                    '00_No Transport Service | 0 Rs.',
                    '01_School Bus Route A | 1500 Rs.',
                    '02_School Bus Route B | 1200 Rs.',
                    '03_Private Vehicle | 0 Rs.',
                    '04_Walking | 0 Rs.'
                ]
                student.transport = random.choice(transport_options)
                updated = True
            
            # Fill blank last school
            if not student.last_school or student.last_school.strip() == '':
                school_names = [
                    'श्री सरस्वती माध्यमिक विद्यालय',
                    'जनता माध्यमिक विद्यालय',
                    'त्रिभुवन माध्यमिक विद्यालय',
                    'शान्ति निकेतन विद्यालय',
                    'ज्ञान ज्योति विद्यालय'
                ]
                student.last_school = random.choice(school_names)
                updated = True
            
            if updated:
                student.save()
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} students with Nepali format data'
            )
        )