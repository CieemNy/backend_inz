# Generated by Django 4.1.2 on 2022-11-25 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_team_completion_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.team'),
        ),
    ]