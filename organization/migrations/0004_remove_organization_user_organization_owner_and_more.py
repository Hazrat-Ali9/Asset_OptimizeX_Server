# Generated by Django 4.2.3 on 2023-10-08 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0003_organization_is_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='user',
        ),
        migrations.AddField(
            model_name='organization',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_organizations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='organization',
            name='organization_logo',
            field=models.ImageField(blank=True, null=True, upload_to='images/company-logo/'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='addMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('Contributor', 'Contributor'), ('Consumer', 'Consumer')], max_length=100)),
                ('is_company', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='member',
            field=models.ManyToManyField(through='organization.addMember', to=settings.AUTH_USER_MODEL),
        ),
    ]
