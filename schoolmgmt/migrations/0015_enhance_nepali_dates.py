# Generated migration for enhanced Nepali date functionality

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolmgmt', '0014_exam_exam_date_nepali_student_admission_date_nepali_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='admission_date_nepali_short',
            field=models.CharField(blank=True, help_text='Short Nepali date (YYYY/MM/DD)', max_length=20),
        ),
        migrations.AddField(
            model_name='student',
            name='session_nepali',
            field=models.CharField(blank=True, help_text='Nepali session (e.g., 2082-83)', max_length=15),
        ),
        migrations.AddField(
            model_name='exam',
            name='exam_date_nepali_short',
            field=models.CharField(blank=True, help_text='Short Nepali date (YYYY/MM/DD)', max_length=20),
        ),
        migrations.AddField(
            model_name='exam',
            name='session_nepali',
            field=models.CharField(blank=True, help_text='Nepali session (e.g., 2082-83)', max_length=15),
        ),
        migrations.AddField(
            model_name='feepayment',
            name='payment_date_nepali',
            field=models.CharField(blank=True, help_text='Nepali payment date', max_length=50),
        ),
        migrations.AddField(
            model_name='feepayment',
            name='payment_date_nepali_short',
            field=models.CharField(blank=True, help_text='Short Nepali payment date', max_length=20),
        ),
        migrations.AddField(
            model_name='session',
            name='name_nepali',
            field=models.CharField(blank=True, help_text='Nepali session name (e.g., 2082-83)', max_length=25),
        ),
        migrations.AddField(
            model_name='session',
            name='start_date_nepali',
            field=models.CharField(blank=True, help_text='Nepali start date', max_length=50),
        ),
        migrations.AddField(
            model_name='session',
            name='end_date_nepali',
            field=models.CharField(blank=True, help_text='Nepali end date', max_length=50),
        ),
    ]