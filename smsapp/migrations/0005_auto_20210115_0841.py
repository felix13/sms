# Generated by Django 2.2.13 on 2021-01-15 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0004_deliveryreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsinbox',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='smslog',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
