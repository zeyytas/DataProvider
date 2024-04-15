# Generated by Django 3.2.25 on 2024-04-15 06:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_reservation_id', models.UUIDField(default=uuid.uuid4)),
                ('night_of_stay', models.DateField()),
                ('status', models.IntegerField(choices=[(1, 'booking'), (2, 'cancellation')])),
                ('event_timestamp', models.DateTimeField(auto_now=True)),
                ('hotel_id', models.CharField(max_length=16)),
            ],
        ),
    ]