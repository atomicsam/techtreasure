# Generated by Django 4.2.11 on 2024-03-21 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techtreasure', '0004_alter_category_id_alter_listing_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='picture_field',
            field=models.ImageField(blank=True, default="listings/default_image.jpg'", null=True, upload_to='listings'),
        ),
    ]