# Generated by Django 4.0.4 on 2022-05-09 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wb_tracker_app', '0005_alter_productcard_brand_alter_productcard_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcard',
            name='vendor_code',
            field=models.CharField(max_length=15),
        ),
    ]
