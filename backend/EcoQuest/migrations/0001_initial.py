# Generated by Django 4.1.7 on 2023-03-28 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('CategoryId', models.BigAutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PointOfInterest',
            fields=[
                ('PointOfInterestId', models.BigAutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100, unique=True)),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EcoQuest.category')),
            ],
        ),
    ]
