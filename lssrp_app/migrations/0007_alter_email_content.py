# Generated by Django 3.2.6 on 2021-08-28 18:59

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('lssrp_app', '0006_alter_email_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='content',
            field=tinymce.models.HTMLField(default=''),
        ),
    ]