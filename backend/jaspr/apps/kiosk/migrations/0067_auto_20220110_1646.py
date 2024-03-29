# Generated by Django 2.2.26 on 2022-01-11 00:46

from django.db import migrations, models
import django.utils.timezone

# Bump version

class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0066_auto_20220110_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientmeasurements',
            name='encounter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kiosk.Encounter',
                                    verbose_name='Encounter'),
        ),
        migrations.RemoveField(
            model_name='patientmeasurements',
            name='patient_session',
        ),
        migrations.AlterField(
            model_name='providercomment',
            name='encounter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kiosk.Encounter',
                                    verbose_name='Encounter'),
        ),
        migrations.RemoveField(
            model_name='providercomment',
            name='patient_session',
        ),
        migrations.RemoveField(
            model_name='historicalpatientcopingstrategy',
            name='patient_session',
        ),
        migrations.RemoveField(
            model_name='patientcopingstrategy',
            name='patient_session',
        ),
        migrations.AddConstraint(
            model_name='patientcopingstrategy',
            constraint=models.UniqueConstraint(fields=('title', 'encounter'),
                                               name='patientcopingstrategy_title_and_patient_encounter_unique_together'),
        ),

        migrations.RemoveField(
            model_name='action',
            name='patient_session',
        ),

        migrations.AlterField(
            model_name='historicalamendment',
            name='encounter',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                    to='kiosk.Encounter'),
        ),
        migrations.RemoveField(
            model_name='amendment',
            name='patient_session',
        ),
        migrations.RemoveField(
            model_name='historicalamendment',
            name='patient_session',
        ),
        migrations.AlterField(
            model_name='assignmentlocks',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    to='kiosk.AssignedActivity'),
        ),
        migrations.RemoveField(
            model_name='assignmentlocks',
            name='patient_session',
        ),
        migrations.RemoveField(
            model_name='crisisstabilityplan',
            name='patient_session',
        ),
        migrations.RemoveField(
            model_name='historicalcrisisstabilityplan',
            name='patient_session',
        ),
        migrations.RemoveField(
            model_name='patientsession',
            name='encounter',
        ),
        migrations.RemoveField(
            model_name='customonboardingquestions',
            name='patient_session',
        ),
        migrations.RemoveField(
            model_name='historicalcustomonboardingquestions',
            name='patient_session',
        ),
        migrations.RemoveField(
            model_name='historicaloutro',
            name='patient_session',
        ),
        migrations.RemoveField(
            model_name='historicalsrat',
            name='patient_session',
        ),
        migrations.RemoveField(
            model_name='outro',
            name='patient_session',
        ),
        migrations.RemoveField(
            model_name='srat',
            name='patient_session',
        ),
        migrations.DeleteModel(
            name='HistoricalPatientSession',
        ),
        migrations.DeleteModel(
            name='PatientSession',
        ),
    ]
