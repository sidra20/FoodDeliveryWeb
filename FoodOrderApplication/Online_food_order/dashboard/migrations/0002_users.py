# Generated by Django 4.1.3 on 2022-11-13 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.roles')),
            ],
        ),
    ]
