# Generated by Django 4.0.3 on 2022-04-08 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_order_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='user_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]