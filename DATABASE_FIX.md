# Database Fix Instructions

## Problem
The application is showing an error: `no such table: schoolmgmt_heroslider`

This happens because the database migrations haven't been run on the production server.

## Quick Fix

### Option 1: Run the fix script
```bash
python fix_database.py
```

### Option 2: Manual steps
```bash
# Step 1: Create migrations
python manage.py makemigrations

# Step 2: Apply migrations
python manage.py migrate
```

### Option 3: For deployment platforms (like Render)
Make sure your build script includes:
```bash
python manage.py makemigrations
python manage.py migrate
```

## What was fixed

1. **Updated views.py**: Added proper error handling for missing database tables
2. **Updated build.sh**: Added `makemigrations` step to ensure all migrations are created
3. **Created fix scripts**: Added `fix_database.py` and `build_deploy.py` for easy fixing

## For Production Deployment

If you're deploying to a platform like Render, Heroku, or similar:

1. Make sure your build command includes both `makemigrations` and `migrate`
2. The updated `build.sh` file should handle this automatically
3. If the issue persists, run the migrations manually after deployment

## Verification

After running the fix, your application should load without the database table errors.

## Files Modified

- `schoolmgmt/views.py` - Added error handling for missing tables
- `build.sh` - Added makemigrations step
- `fix_database.py` - New script to fix database issues
- `build_deploy.py` - New comprehensive build script