# Generated by Django 4.1.3 on 2022-12-05 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=300)),
                ('lname', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=300)),
                ('province', models.CharField(choices=[('province no.1 ', 'Province No. 1'), ('madesh province', 'Madhesh Province'), ('bagmati province', 'Bagmati Province'), ('gandaki province', 'Gandaki Province'), ('lumbini province', 'Lumbini Province'), ('karnali province', 'Karnali Province'), ('mahakali province', 'Mahakali Province')], max_length=100)),
                ('district', models.CharField(max_length=200)),
                ('zipcode', models.IntegerField()),
                ('city', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=300)),
                ('lname', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=300)),
                ('province', models.CharField(choices=[('province no.1 ', 'Province No. 1'), ('madesh province', 'Madhesh Province'), ('bagmati province', 'Bagmati Province'), ('gandaki province', 'Gandaki Province'), ('lumbini province', 'Lumbini Province'), ('karnali province', 'Karnali Province'), ('mahakali province', 'Mahakali Province')], max_length=100)),
                ('district', models.CharField(max_length=200)),
                ('zipcode', models.IntegerField()),
                ('city', models.CharField(max_length=300)),
                ('specialnotes', models.TextField()),
            ],
        ),
    ]
