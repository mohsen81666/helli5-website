# Generated by Django 3.0 on 2019-12-12 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('postingApp', '0006_auto_20191212_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postingApp.User'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postingApp.PostStuff'),
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('post', 'author')},
        ),
    ]
