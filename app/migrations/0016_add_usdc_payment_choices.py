from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_add_target_to_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='method_type',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('ETH', 'Ethereum'),
                    ('BTC', 'Bitcoin'),
                    ('SOL', 'Solana'),
                    ('USDT_ERC20', 'USDT (ERC20)'),
                    ('USDT_TRC20', 'USDT (TRC20)'),
                    ('USDC_BASE', 'USDC (Base)'),
                    ('USDC_SOL', 'USDC (Solana)'),
                    ('BANK', 'Bank Transfer'),
                    ('CASHAPP', 'Cash App'),
                    ('PAYPAL', 'PayPal'),
                ],
            ),
        ),
    ]
