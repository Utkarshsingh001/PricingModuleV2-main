# Generated by Django 4.2.4 on 2023-08-08 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_pricing_module_usermodifiedby_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricing_module',
            name='created_at',
            field=models.CharField(max_length=50),
        ),
    ]
