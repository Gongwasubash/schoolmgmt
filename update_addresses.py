import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import Student

nepali_places = [
    "Kathmandu", "Pokhara", "Lalitpur", "Bhaktapur", "Biratnagar", "Birgunj", 
    "Dharan", "Bharatpur", "Janakpur", "Butwal", "Hetauda", "Dhangadhi",
    "Itahari", "Nepalgunj", "Gorkha", "Chitwan", "Banke", "Kailali",
    "Jhapa", "Morang", "Sunsari", "Sarlahi", "Mahottari", "Dhanusa"
]

nepali_addresses = [
    "Thamel", "Patan Durbar Square", "Basantapur", "New Road", "Asan Tole",
    "Lakeside", "Sarangkot", "Phewa Lake", "Bindabasini", "Mahendrapul",
    "Jawalakhel", "Pulchowk", "Mangal Bazaar", "Godawari", "Chapagaun",
    "Durbar Square", "Pottery Square", "Taumadhi Square", "Dattatreya Square",
    "Traffic Chowk", "Rani Pokhari", "Ratna Park", "Sundhara", "Kalanki"
]

students = Student.objects.all()
for student in students:
    if not student.address1 or student.address1 == 'N/A':
        student.address1 = random.choice(nepali_addresses)
    if not student.city or student.city == 'N/A':
        student.city = random.choice(nepali_places)
    student.save()

print(f"Updated addresses for {students.count()} students")