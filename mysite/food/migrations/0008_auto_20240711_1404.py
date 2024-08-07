# Generated by Django 3.2 on 2024-07-11 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_remove_tag_rstyle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Device_Management',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('devices', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.device')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.place')),
            ],
        ),
        migrations.AddField(
            model_name='place',
            name='devices',
            field=models.ManyToManyField(through='food.Device_Management', to='food.Device'),
        ),
    ]
