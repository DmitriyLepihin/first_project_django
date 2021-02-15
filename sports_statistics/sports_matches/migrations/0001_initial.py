# Generated by Django 3.1.5 on 2021-02-08 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MatchResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_one', models.CharField(max_length=350)),
                ('team_two', models.CharField(max_length=350)),
                ('score_one', models.IntegerField()),
                ('score_two', models.IntegerField()),
                ('date_match', models.DateField()),
                ('match_details', models.CharField(max_length=800)),
            ],
        ),
    ]
