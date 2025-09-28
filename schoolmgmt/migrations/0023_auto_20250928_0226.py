from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolmgmt', '0022_schooldetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('address', models.TextField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='school_logos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='IDCardTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_id', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('template_type', models.CharField(choices=[('student', 'Student'), ('staff', 'Staff')], max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('template_data', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]