from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_add_withdrawal_source_to_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='target',
            field=models.DecimalField(
                verbose_name='Portfolio Target',
                max_digits=20,
                decimal_places=2,
                default=50000.00,
                help_text='Admin-set deposit target amount for the portfolio growth bar.',
            ),
        ),
    ]
