# Generated by Django 4.2 on 2023-04-07 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0005_alter_inbound_price_inbound'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inbound',
            name='price_inbound',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=19),
        ),
    ]
