# Generated by Django 2.2.5 on 2019-09-26 12:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_status', '0012_auto_20190926_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lte_integration',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 9, 26, 12, 35, 8, 181460)),
        ),
        migrations.AlterField(
            model_name='lte_integration',
            name='time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 26, 12, 35, 8, 181460)),
        ),
        migrations.AlterField(
            model_name='lte_validation',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 9, 26, 12, 35, 8, 181460)),
        ),
    ]
