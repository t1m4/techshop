# Generated by Django 3.1.7 on 2021-04-05 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20210405_1042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basket',
            name='total_price',
        ),
    ]
