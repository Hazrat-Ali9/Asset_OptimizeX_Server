# Generated by Django 4.2.6 on 2023-11-02 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0012_feedbackmodel_feedback_approve'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackmodel',
            name='rating',
        ),
    ]