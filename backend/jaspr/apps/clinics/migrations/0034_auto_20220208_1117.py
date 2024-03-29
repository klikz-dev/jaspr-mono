# Generated by Django 2.2.26 on 2022-02-08 19:17

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ('clinics', '0033_auto_20220125_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalpreferences',
            name='consent_language',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.TextField(), default=[
                'Jaspr is not a replacement for your care team nor is it an emergency service. If you need urgent help, please speak to your care team now.',
                'Everything you do on Jaspr will remain confidential. To give you the best experience, some of your information will be stored, in keeping with our privacy practices.',
                'Your care team will have access to your Jaspr data. They may use the information to improve the care you receive. They may add some Jaspr data to your medical record. Your healthcare system will follow its own Notice of Privacy Practices for this information.',
                'Jaspr is an investigational device backed by science and supported by federal research. The Jaspr Health Team wishes to continue to improve it. You do not need to use it. By using this device, you are agreeing to use Jaspr under the supervision of your care team.',
                'If you are under 18 years of age, your care team has followed local laws regarding parent/guardian permission for your use of Jaspr.'],
                                                                          help_text='Custom language shown to the patient on the consent screen. Each text field represents a bulleted consent point',
                                                                          size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='preferences',
            name='consent_language',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.TextField(),
                                                                          default=[
                                                                              'Jaspr is not a replacement for your care team nor is it an emergency service. If you need urgent help, please speak to your care team now.',
                                                                              'Everything you do on Jaspr will remain confidential. To give you the best experience, some of your information will be stored, in keeping with our privacy practices.',
                                                                              'Your care team will have access to your Jaspr data. They may use the information to improve the care you receive. They may add some Jaspr data to your medical record. Your healthcare system will follow its own Notice of Privacy Practices for this information.',
                                                                              'Jaspr is an investigational device backed by science and supported by federal research. The Jaspr Health Team wishes to continue to improve it. You do not need to use it. By using this device, you are agreeing to use Jaspr under the supervision of your care team.',
                                                                              'If you are under 18 years of age, your care team has followed local laws regarding parent/guardian permission for your use of Jaspr.'],
                                                                          help_text='Custom language shown to the patient on the consent screen. Each text field represents a bulleted consent point',
                                                                          size=None),
            preserve_default=False,
        ),
    ]
