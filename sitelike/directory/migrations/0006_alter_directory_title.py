# Generated by Django 4.2.6 on 2023-10-14 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0005_alter_directory_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='title',
            field=models.TextField(default=''),
        ),
    ]
