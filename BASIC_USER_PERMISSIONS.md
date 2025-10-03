# Basic User Permissions - Enable All Sidebar Menu Access

This feature allows administrators to easily enable all sidebar menu permissions for basic users (non-super admin users) with a single click.

## What This Feature Does

When enabled, basic users will have access to ALL sidebar menu items including:
- Dashboard
- Students
- Teachers  
- Attendance
- Reports
- Marksheet
- Fee Structure
- Fee Payment
- Daily Expenses
- Settings

## How to Use

### Method 1: Via User Management Interface (Recommended)

1. Login as a super admin or user with user management permissions
2. Go to **User Management** page
3. Find the basic user you want to enable permissions for
4. Click the **"Enable All"** button next to their name
5. Confirm the action in the popup dialog
6. The user will now have access to all sidebar menu items

### Method 2: Via Django Management Command

Run this command in your terminal:

```bash
# Enable all permissions for all basic users
python manage.py enable_basic_permissions

# Enable all permissions for a specific user
python manage.py enable_basic_permissions --username <username>
```

### Method 3: Via Python Script

Run the provided script:

```bash
python enable_basic_permissions.py
```

## Technical Details

### New Permission Fields Added

The following permission fields were added to the `AdminLogin` model:
- `can_view_charts` - Can view charts and graphs
- `can_view_stats` - Can view statistics  
- `can_view_fees` - Can view fees menu
- `can_view_receipts` - Can view receipts menu
- `can_view_expenses` - Can view expenses menu
- `can_view_settings` - Can view settings menu

### Model Methods

- `enable_all_permissions()` - Enables all sidebar menu permissions for the user
- `create_basic_user(username, password, teacher=None)` - Class method to create a basic user with all permissions enabled

### Context Processor

The `user_permissions` context processor has been updated to safely handle the new permission fields with fallback values.

### Sidebar Template

The `base_basic_sidebar.html` template now includes conditional rendering for all menu items based on user permissions.

## Files Modified

1. `schoolmgmt/models.py` - Added new permission fields and helper methods
2. `schoolmgmt/context_processors_user.py` - Updated to handle new permission fields
3. `templates/base_basic_sidebar.html` - Updated sidebar to show all menu items when permissions are enabled
4. `templates/user_management.html` - Added "Enable All" button
5. `schoolmgmt/views_admin.py` - Added enable_all_permissions view
6. `schoolmgmt/urls.py` - Added URL pattern for enable permissions endpoint
7. `schoolmgmt/admin.py` - Updated admin interface to show new permission fields

## Migration

A migration was automatically created to add the new permission fields:
- `0049_adminlogin_can_view_charts_and_more.py`

## Testing

Run the test script to verify functionality:

```bash
python test_permissions.py
```

This will test the `enable_all_permissions()` method and verify all permissions are correctly enabled.

## Notes

- Super admin users already have all permissions by default
- The "Enable All" button only appears for basic users (non-super admin)
- All existing basic users have been automatically updated with all permissions enabled
- This feature is safe to use and does not affect super admin users