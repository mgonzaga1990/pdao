# Generated by Django 3.1.5 on 2021-02-08 22:40

from django.db import migrations, models
import evaluation.models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0002_auto_20210209_0338'),
    ]

    operations = [
        migrations.CreateModel(
            name='DohForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to=evaluation.models.doh_form_file)),
            ],
        ),
    ]