# Generated by Django 3.2.8 on 2023-10-03 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
        ('uploadAsset', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadasset',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.library'),
        ),
    ]
