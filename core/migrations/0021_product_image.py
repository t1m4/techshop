# Generated by Django 3.1.7 on 2021-04-09 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20210408_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='static/core/img/example.jpg', upload_to='static/core/img'),
        ),
    ]
