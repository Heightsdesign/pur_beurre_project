# Generated by Django 3.2.4 on 2021-09-28 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitutes', '0003_auto_20210928_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='nutriments',
            field=models.ManyToManyField(blank=True, related_name='nutriments', to='substitutes.Nutriments'),
        ),
    ]
