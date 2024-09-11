# Generated by Django 4.2.16 on 2024-09-10 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_transaction_actual_return_date_transaction_penalty'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='book',
            name='total_quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='rental_debt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='fees_charged',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='penalty',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5, null=True),
        ),
    ]
