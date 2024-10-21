# Generated by Django 4.2.16 on 2024-09-15 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('cooking_time', models.FloatField(help_text='minutes')),
                ('ingredients', models.CharField(help_text='Ingredients must be separated by commas.', max_length=400)),
            ],
        ),
    ]
