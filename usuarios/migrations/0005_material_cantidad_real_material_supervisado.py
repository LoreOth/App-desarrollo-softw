# Generated by Django 4.2.16 on 2024-10-06 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_delete_materialstock'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='cantidad_real',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='material',
            name='supervisado',
            field=models.BooleanField(default=False),
        ),
    ]
