# Generated by Django 4.2.1 on 2023-07-04 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_contacto'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='Stock',
            field=models.IntegerField(null=True),
        ),
    ]
