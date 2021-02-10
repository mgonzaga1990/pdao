# Generated by Django 3.1.5 on 2021-02-09 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='civil_status',
            field=models.IntegerField(choices=[(0, 'Single'), (1, 'Married'), (2, 'Separated'), (3, 'Live In'), (4, 'Widow')], null=True),
        ),
    ]
