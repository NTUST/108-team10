# Generated by Django 2.2.1 on 2019-05-28 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('version1_0', '0003_auto_20190528_1551'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beverage',
            old_name='hasCool',
            new_name='hasCold',
        ),
    ]
