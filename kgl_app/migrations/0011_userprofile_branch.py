# Generated by Django 5.2 on 2025-04-29 21:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kgl_app', '0010_alter_stock_branch_alter_stock_issued_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='kgl_app.branch'),
        ),
    ]
