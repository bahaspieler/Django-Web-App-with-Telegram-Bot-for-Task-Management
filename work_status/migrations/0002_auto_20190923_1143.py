# Generated by Django 2.2.5 on 2019-09-23 05:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('work_status', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lte_validation',
            old_name='Site_or_Cell_name',
            new_name='Assign',
        ),
        migrations.AlterField(
            model_name='lte_integration',
            name='execution_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 9, 23, 5, 43, 18, 169313, tzinfo=utc)),
        ),
    ]
