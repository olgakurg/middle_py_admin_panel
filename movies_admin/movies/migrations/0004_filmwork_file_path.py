# Generated by Django 4.2.5 on 2023-09-11 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_filmwork_options_alter_genre_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmwork',
            name='file_path',
            field=models.TextField(null=True, verbose_name='file_path'),
        ),
    ]
