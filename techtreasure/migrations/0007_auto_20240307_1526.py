# Generated by Django 2.2.28 on 2024-03-07 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('techtreasure', '0006_auto_20240307_1507'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='categories',
            new_name='category',
        ),
    ]