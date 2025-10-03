#!/usr/bin/env python
"""
Test script to verify the enable_all_permissions functionality
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import AdminLogin

def test_enable_all_permissions():
    """Test the enable_all_permissions method"""
    
    # Get a basic user (non-super admin)
    basic_user = AdminLogin.objects.filter(is_super_admin=False, is_active=True).first()
    
    if not basic_user:
        print("No basic users found to test")
        return
    
    print(f"Testing with user: {basic_user.username}")
    
    # Check permissions before
    print("\nPermissions BEFORE enabling all:")
    print(f"  can_view_dashboard: {basic_user.can_view_dashboard}")
    print(f"  can_view_students: {basic_user.can_view_students}")
    print(f"  can_view_teachers: {basic_user.can_view_teachers}")
    print(f"  can_view_reports: {basic_user.can_view_reports}")
    print(f"  can_view_marksheet: {basic_user.can_view_marksheet}")
    print(f"  can_view_fee_structure: {basic_user.can_view_fee_structure}")
    print(f"  can_view_fee_receipt: {basic_user.can_view_fee_receipt}")
    print(f"  can_view_daily_expenses: {basic_user.can_view_daily_expenses}")
    print(f"  can_view_school_settings: {basic_user.can_view_school_settings}")
    print(f"  can_view_website_settings: {basic_user.can_view_website_settings}")
    print(f"  can_view_user_management: {basic_user.can_view_user_management}")
    print(f"  can_view_charts: {getattr(basic_user, 'can_view_charts', 'N/A')}")
    print(f"  can_view_stats: {getattr(basic_user, 'can_view_stats', 'N/A')}")
    print(f"  can_view_fees: {getattr(basic_user, 'can_view_fees', 'N/A')}")
    print(f"  can_view_receipts: {getattr(basic_user, 'can_view_receipts', 'N/A')}")
    print(f"  can_view_expenses: {getattr(basic_user, 'can_view_expenses', 'N/A')}")
    print(f"  can_view_settings: {getattr(basic_user, 'can_view_settings', 'N/A')}")
    
    # Enable all permissions
    print("\nEnabling all permissions...")
    basic_user.enable_all_permissions()
    
    # Refresh from database
    basic_user.refresh_from_db()
    
    # Check permissions after
    print("\nPermissions AFTER enabling all:")
    print(f"  can_view_dashboard: {basic_user.can_view_dashboard}")
    print(f"  can_view_students: {basic_user.can_view_students}")
    print(f"  can_view_teachers: {basic_user.can_view_teachers}")
    print(f"  can_view_reports: {basic_user.can_view_reports}")
    print(f"  can_view_marksheet: {basic_user.can_view_marksheet}")
    print(f"  can_view_fee_structure: {basic_user.can_view_fee_structure}")
    print(f"  can_view_fee_receipt: {basic_user.can_view_fee_receipt}")
    print(f"  can_view_daily_expenses: {basic_user.can_view_daily_expenses}")
    print(f"  can_view_school_settings: {basic_user.can_view_school_settings}")
    print(f"  can_view_website_settings: {basic_user.can_view_website_settings}")
    print(f"  can_view_user_management: {basic_user.can_view_user_management}")
    print(f"  can_view_charts: {basic_user.can_view_charts}")
    print(f"  can_view_stats: {basic_user.can_view_stats}")
    print(f"  can_view_fees: {basic_user.can_view_fees}")
    print(f"  can_view_receipts: {basic_user.can_view_receipts}")
    print(f"  can_view_expenses: {basic_user.can_view_expenses}")
    print(f"  can_view_settings: {basic_user.can_view_settings}")
    
    # Verify all permissions are True
    all_permissions_enabled = all([
        basic_user.can_view_dashboard,
        basic_user.can_view_students,
        basic_user.can_view_teachers,
        basic_user.can_view_reports,
        basic_user.can_view_marksheet,
        basic_user.can_view_fee_structure,
        basic_user.can_view_fee_receipt,
        basic_user.can_view_daily_expenses,
        basic_user.can_view_school_settings,
        basic_user.can_view_website_settings,
        basic_user.can_view_user_management,
        basic_user.can_view_charts,
        basic_user.can_view_stats,
        basic_user.can_view_fees,
        basic_user.can_view_receipts,
        basic_user.can_view_expenses,
        basic_user.can_view_settings,
    ])
    
    if all_permissions_enabled:
        print("\n[SUCCESS] All permissions are now enabled!")
    else:
        print("\n[ERROR] Some permissions are still disabled!")
    
    return all_permissions_enabled

if __name__ == "__main__":
    test_enable_all_permissions()