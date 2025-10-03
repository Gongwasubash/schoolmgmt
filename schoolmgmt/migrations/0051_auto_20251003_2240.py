from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolmgmt', '0050_adminlogin_can_view_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminlogin',
            name='can_view_attendance',
            field=models.BooleanField(default=True, help_text='Can view student attendance menu', verbose_name='Student Attendance'),
        ),
    ]