# Generated by Django 2.0 on 2018-01-12 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0003_gift_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='bought',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gift',
            name='wrapped',
            field=models.BooleanField(default=False),
        ),
    ]
