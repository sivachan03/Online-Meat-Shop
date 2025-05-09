# Generated by Django 4.2.7 on 2025-03-06 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='product',
            new_name='shop_produc_id_f21274_idx',
            old_fields=('id', 'slug'),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Discounted price (optional)', max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default=False, help_text='Featured products appear on homepage'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='shop_produc_name_a2070e_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['created'], name='shop_produc_created_661b12_idx'),
        ),
    ]
