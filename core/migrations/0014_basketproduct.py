# Generated by Django 3.1.7 on 2021-04-05 08:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20210405_1137'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasketProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='core.product')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='basket', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]