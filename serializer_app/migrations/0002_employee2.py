# Generated by Django 4.0.4 on 2022-04-19 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serializer_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee2',
            fields=[
                ('username', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=10)),
                ('department', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=30, unique=True)),
            ],
        ),
    ]