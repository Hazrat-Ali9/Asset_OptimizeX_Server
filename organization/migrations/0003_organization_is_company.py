# Generated by Django 4.2.5 on 2023-10-02 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_remove_organization_is_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='is_company',
            field=models.BooleanField(default=False),
        ),
    ]
