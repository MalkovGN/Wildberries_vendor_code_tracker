# Generated by Django 4.0.4 on 2022-05-05 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wb_tracker_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_code', models.IntegerField()),
                ('product_name', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('sale_price', models.FloatField()),
                ('brand', models.CharField(max_length=100)),
                ('supplier', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='vendorcode',
            name='price',
        ),
        migrations.AlterField(
            model_name='vendorcode',
            name='vendor_code',
            field=models.IntegerField(),
        ),
    ]
