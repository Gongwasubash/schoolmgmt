import re

# Read the views.py file
with open('e:\\schoolmgmt\\schoolmgmt\\views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the first dashboard function and add pending enquiries calculation
pattern = r"(def dashboard\(request\):\s*\"\"\"Original dashboard view[^}]+?yearly_collection = FeePayment\.objects\.filter\(payment_date__year=today\.year\)\.aggregate\(total=Sum\('payment_amount'\)\)\['total'\] or 0\s*)(# Get class-wise data)"

replacement = r"\1\n    # Get pending enquiries count\n    pending_enquiries = ContactEnquiry.objects.count() + StudentRegistration.objects.filter(status='pending').count()\n    \n    \2"

# Replace only the first occurrence
content = re.sub(pattern, replacement, content, count=1)

# Also add pending_enquiries to the context in the first dashboard function
pattern2 = r"(def dashboard\(request\):[^}]+?'yearly_collection': yearly_collection,\s*)'class_data': class_data,"

replacement2 = r"\1'pending_enquiries': pending_enquiries,\n        'class_data': class_data,"

content = re.sub(pattern2, replacement2, content, count=1)

# Write back to file
with open('e:\\schoolmgmt\\schoolmgmt\\views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Dashboard function updated successfully!")