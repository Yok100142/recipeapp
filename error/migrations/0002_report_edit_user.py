# Generated by Django 3.1 on 2021-03-18 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('error', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='edit_user',
            field=models.CharField(default='nichakarn.ra@ku.th', max_length=50),
        ),
    ]