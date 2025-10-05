# Generated migration for adding school field to CalendarEvent

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolmgmt', '0054_calendarevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendarevent',
            name='school',
            field=models.ForeignKey(blank=True, help_text='School for this event', null=True, on_delete=django.db.models.deletion.CASCADE, to='schoolmgmt.schooldetail'),
        ),
    ]