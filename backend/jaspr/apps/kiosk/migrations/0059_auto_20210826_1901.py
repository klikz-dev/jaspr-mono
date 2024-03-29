# Generated by Django 2.2.24 on 2021-08-27 00:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jaspr.apps.common.fields.encrypted_json_field
import model_utils.fields
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kiosk', '0058_assessmentlocks_acknowledged'),
    ]

    operations = [
        migrations.CreateModel(
            name='Outro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('active', 'Active'), ('archived', 'Archived')], default='active', max_length=100, no_check_for_status=True)),
                ('answers', jaspr.apps.common.fields.encrypted_json_field.EncryptedJSONField(blank=True, null=True)),
                ('patient_session', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kiosk.PatientSession', verbose_name='Patient Session')),
            ],
            options={
                'verbose_name': 'Outro Question Answers',
                'verbose_name_plural': 'Outro Question Answers',
            },
        ),
        migrations.CreateModel(
            name='HistoricalOutro',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('choice1', 'choice1'), ('choice2', 'choice2')], default='choice1', max_length=100, no_check_for_status=True)),
                ('answers', jaspr.apps.common.fields.encrypted_json_field.EncryptedJSONField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('patient_session', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='kiosk.PatientSession', verbose_name='Patient Session')),
            ],
            options={
                'verbose_name': 'historical Outro Question Answers',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
