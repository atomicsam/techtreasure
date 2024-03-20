# Generated by Django 2.2 on 2024-03-20 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Merchandise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('describe', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('file_image', models.ImageField(upload_to='')),
                ('user_id', models.CharField(max_length=30, null=True)),
                ('user_name', models.CharField(max_length=30, null=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Merchandise',
            },
        ),
        migrations.CreateModel(
            name='HistoryRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user_id', models.CharField(max_length=30, null=True)),
                ('user_name', models.CharField(max_length=30, null=True)),
                ('purchase_user_id', models.CharField(max_length=30, null=True)),
                ('purchase_user_name', models.CharField(max_length=30, null=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('merchandise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Merchandise')),
            ],
            options={
                'verbose_name_plural': 'HistoryRecord',
            },
        ),
    ]
