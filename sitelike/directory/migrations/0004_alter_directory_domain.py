# Generated by Django 4.2.6 on 2023-10-14 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0003_alter_directory_da_alter_directory_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='domain',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
