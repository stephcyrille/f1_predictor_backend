# Generated by Django 4.2.11 on 2024-03-16 01:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('constructors', '0003_alter_constructor_constructor_avg_point'),
        ('drivers', '0002_driver_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='constructorId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='constructors.constructor'),
        ),
    ]
