# Generated by Django 4.1.3 on 2022-11-24 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_rename_customer_name_reviews_name_reviews_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='labels',
            field=models.CharField(choices=[('HOT', 'hot'), ('NEW', 'new'), ('SALE', 'sale')], max_length=100),
        ),
    ]