# Generated by Django 3.1 on 2021-01-08 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pantip_id', models.CharField(max_length=50)),
                ('report_data', models.CharField(max_length=255)),
            ],
        ),
    ]
