# Generated by Django 3.1.7 on 2021-04-05 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20210405_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='core.product'),
        ),
    ]
