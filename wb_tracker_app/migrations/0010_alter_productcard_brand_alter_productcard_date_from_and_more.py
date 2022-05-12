# Generated by Django 4.0.4 on 2022-05-12 11:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wb_tracker_app', '0009_alter_productcard_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcard',
            name='brand',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='productcard',
            name='date_from',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(regex='^\\d{4}\\-(0?[1-9]|1[012])\\-(0?[1-9]|[12][0-9]|3[01])$')]),
        ),
        migrations.AlterField(
            model_name='productcard',
            name='date_to',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(regex='^\\d{4}\\-(0?[1-9]|1[012])\\-(0?[1-9]|[12][0-9]|3[01])$')]),
        ),
        migrations.AlterField(
            model_name='productcard',
            name='price',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='productcard',
            name='sale_price',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='productcard',
            name='supplier',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='productcard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]