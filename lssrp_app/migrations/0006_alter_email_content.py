# Generated by Django 3.2.6 on 2021-08-28 17:24

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("lssrp_app", "0005_alter_email_sent_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="email",
            name="content",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]
