# Generated by Django 3.2 on 2021-04-27 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('heading', models.TextField()),
                ('description', models.TextField()),
                ('deadline', models.TextField()),
            ],
        ),
    ]