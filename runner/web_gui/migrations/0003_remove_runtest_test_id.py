# Generated by Django 2.0.9 on 2019-01-25 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_gui', '0002_remove_runtest_run_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='runtest',
            name='test_id',
        ),
    ]
