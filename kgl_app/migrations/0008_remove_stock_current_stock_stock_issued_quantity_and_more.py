# Generated by Django 5.2 on 2025-04-28 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kgl_app', '0007_sales_selling_price_alter_sales_is_sold_on_cash'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='current_stock',
        ),
        migrations.AddField(
            model_name='stock',
            name='issued_quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='received_quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='credit',
            name='NIN',
            field=models.CharField(unique=True),
        ),
        migrations.AlterField(
            model_name='credit',
            name='contact',
            field=models.IntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='credit',
            name='location',
            field=models.CharField(default=35, max_length=25),
        ),
        migrations.AlterField(
            model_name='sales',
            name='is_sold_on_cash',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sales',
            name='selling_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
