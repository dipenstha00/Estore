# Generated by Django 4.1.3 on 2022-12-16 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_order_orderitem_remove_shippingaddress_s_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='username',
            field=models.CharField(default='', max_length=300),
        ),
    ]
