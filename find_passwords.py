import os
import django
import hashlib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import AdminLogin

users = AdminLogin.objects.filter(is_super_admin=True)
passwords = ['admin123', 'saMA@123', 'password123', 'admin', '123456', 'superadmin', 'password', '12345']

for user in users:
    print(f'Testing {user.username}:')
    for pwd in passwords:
        hash_val = hashlib.md5(pwd.encode()).hexdigest()
        if user.password == hash_val:
            print(f'  FOUND: {pwd}')
            break
    else:
        print(f'  Password not found in common list')
    print()