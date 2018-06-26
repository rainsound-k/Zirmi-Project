# Generated by Django 2.0.5 on 2018-06-26 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_auto_20180621_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='items.ItemComment'),
        ),
    ]
