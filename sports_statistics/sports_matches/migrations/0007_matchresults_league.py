# Generated by Django 3.1.5 on 2021-02-08 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports_matches', '0006_matchresults_type_sport'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchresults',
            name='league',
            field=models.CharField(max_length=150, null=True),
        ),
    ]