# Generated by Django 4.2.16 on 2024-10-06 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_material'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=255)),
                ('cantidad_total', models.PositiveIntegerField()),
            ],
        ),
    ]
