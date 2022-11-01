# Generated by Django 4.1.2 on 2022-11-01 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='status',
            field=models.CharField(choices=[('Not graded', 'Not graded'), ('Graded', 'Graded')], default='Not graded', max_length=10, verbose_name='Status'),
        ),
    ]
