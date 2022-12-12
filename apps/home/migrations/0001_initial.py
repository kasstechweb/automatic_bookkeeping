# Generated by Django 3.2.6 on 2022-12-11 21:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to='documents/%Y/%m/%d', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
            ],
        ),
    ]
