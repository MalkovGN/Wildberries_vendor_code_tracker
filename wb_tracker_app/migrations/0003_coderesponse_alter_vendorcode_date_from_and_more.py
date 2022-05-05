# Generated by Django 4.0.4 on 2022-05-05 16:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wb_tracker_app', '0002_productcard_remove_vendorcode_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.SmallIntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='vendorcode',
            name='date_from',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(regex='^\\d{4}\\-(0?[1-9]|1[012])\\-(0?[1-9]|[12][0-9]|3[01])$')]),
        ),
        migrations.AlterField(
            model_name='vendorcode',
            name='date_to',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(regex='^\\d{4}\\-(0?[1-9]|1[012])\\-(0?[1-9]|[12][0-9]|3[01])$')]),
        ),
    ]