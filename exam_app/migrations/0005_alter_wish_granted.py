# Generated by Django 3.2 on 2021-04-29 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0004_wish_granted_for'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish',
            name='granted',
            field=models.CharField(max_length=255),
        ),
    ]