# Generated by Django 3.0 on 2019-12-15 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('postingApp', '0016_auto_20191215_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postingApp.PostStuff'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postingApp.PostStuff'),
        ),
    ]
