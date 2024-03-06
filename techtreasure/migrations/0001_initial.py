# Generated by Django 2.2.28 on 2024-03-06 18:12

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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('views', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Listings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picturefield', models.ImageField(upload_to='')),
                ('suggestedprice', models.DecimalField(decimal_places=2, max_digits=5)),
                ('itemsold', models.BooleanField()),
                ('descriptionfield', models.CharField(max_length=500)),
                ('numofviews', models.IntegerField(unique=True)),
                ('location', models.CharField(max_length=100)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='techtreasure.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('forename', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offerid', models.IntegerField(unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('offerdate', models.DateField()),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='techtreasure.Listings')),
                ('users', models.ManyToManyField(to='techtreasure.Users')),
            ],
        ),
    ]
