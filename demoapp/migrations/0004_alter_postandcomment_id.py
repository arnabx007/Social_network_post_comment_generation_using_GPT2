# Generated by Django 3.2.7 on 2021-09-24 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0003_alter_postandcomment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postandcomment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
