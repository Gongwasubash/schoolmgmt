from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('schoolmgmt', '0008_exam_subject_marksheet'),
    ]

    operations = [
        migrations.AddField(
            model_name='marksheet',
            name='session',
            field=models.CharField(default='2024-25', max_length=10),
        ),
    ]