# Generated by Django 5.0.6 on 2024-07-06 03:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquarius', '0004_post_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='comment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='aquarius.comment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(default=''),
        ),
    ]
