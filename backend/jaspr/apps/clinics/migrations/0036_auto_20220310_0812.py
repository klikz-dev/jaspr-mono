# Generated by Django 3.2.12 on 2022-03-10 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0035_auto_20220309_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='preferences',
            name='label',
            field=models.CharField(blank=True, help_text='Enter a value in this field to help identify the purpose of this record.', max_length=50, null=True),
        ),
    ]
