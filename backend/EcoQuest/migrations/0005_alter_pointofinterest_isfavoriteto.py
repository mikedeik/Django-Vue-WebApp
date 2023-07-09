# Generated by Django 4.1.5 on 2023-07-09 19:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EcoQuest', '0004_pointofinterest_isfavoriteto_delete_favoritepois'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointofinterest',
            name='IsFavoriteTo',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]