# Generated by Django 2.0.9 on 2019-01-25 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_gui', '0003_remove_runtest_test_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='runtest',
            name='result',
        ),
    ]