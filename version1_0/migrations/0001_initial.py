# Generated by Django 2.0.5 on 2019-05-15 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beverage',
            fields=[
                ('BeverageId', models.TextField(default='', max_length=3, primary_key=True, serialize=False)),
                ('name', models.TextField(default='')),
                ('info', models.TextField(null=True)),
                ('imagePath', models.TextField(null=True)),
                ('hasCool', models.BooleanField(default=True)),
                ('hasHot', models.BooleanField(default=False)),
                ('remark', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BeverageSize',
            fields=[
                ('Number', models.TextField(default='', max_length=3, primary_key=True, serialize=False)),
                ('size', models.TextField(default='M', max_length=2)),
                ('price', models.IntegerField(default=0)),
                ('calories', models.IntegerField(default=0)),
                ('BeverageId', models.ForeignKey(default='XXX', on_delete=django.db.models.deletion.CASCADE, to='version1_0.Beverage')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('CategoryId', models.TextField(default='', max_length=2, primary_key=True, serialize=False)),
                ('name', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('ShopId', models.TextField(default='', max_length=1, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('info', models.TextField(null=True)),
                ('logoPath', models.TextField(null=True)),
                ('imagePath', models.TextField(null=True)),
                ('remark', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('StudentId', models.TextField(default='B00000000', max_length=9, primary_key=True, serialize=False)),
                ('name', models.TextField(default='')),
                ('info', models.TextField()),
                ('photoPath', models.TextField(null=True)),
                ('job', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='beverage',
            name='Category',
            field=models.ForeignKey(default='CX', on_delete=django.db.models.deletion.SET_DEFAULT, to='version1_0.Category'),
        ),
        migrations.AddField(
            model_name='beverage',
            name='Shop',
            field=models.ForeignKey(default='X', on_delete=django.db.models.deletion.CASCADE, to='version1_0.Shop'),
        ),
    ]