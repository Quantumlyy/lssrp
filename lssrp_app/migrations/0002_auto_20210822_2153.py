# Generated by Django 2.2.24 on 2021-08-22 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lssrp_app", "0001_base_user_mail_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="email",
            name="sent_time",
            field=models.DateField(auto_now_add=True),
        ),
    ]
