# Generated by Django 2.2.13 on 2021-03-11 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0030_auto_20210221_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='assessment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kiosk.Assessment', verbose_name='Assessment'),
        ),
    ]
