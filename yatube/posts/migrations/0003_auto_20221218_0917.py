# Generated by Django 2.2.19 on 2022-12-18 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': [-1]},
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='posts', to='posts.Group'),
        ),
    ]
