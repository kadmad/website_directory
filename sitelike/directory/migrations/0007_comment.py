from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0006_alter_directory_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('content', models.TextField()),
                ('directory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='directory.directory')),
            ],
            options={
                'ordering': ['-created_at'],
                'app_label': 'directory',
            },
        ),
    ]
