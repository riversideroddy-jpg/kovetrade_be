from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0010_remove_capital_trading_days_add_profit_share"),
    ]

    operations = [
        migrations.AlterField(
            model_name="adminwallet",
            name="currency",
            field=models.CharField(
                choices=[
                    ("BTC", "Bitcoin (BTC)"),
                    ("ETH", "Ethereum (ETH)"),
                    ("SOL", "Solana (SOL)"),
                    ("USDT ERC20", "USDT (ERC20)"),
                    ("USDT TRC20", "USDT (TRC20)"),
                    ("USDT SOL", "USDT (Solana)"),
                    ("USDT BEP20", "USDT (BEP20 / BSC)"),
                    ("BNB", "Binance Coin (BNB)"),
                    ("TRX", "Tron (TRX)"),
                    ("USDC", "USDC (BASE)"),
                    ("USDC ERC20", "USDC (ERC20)"),
                    ("USDC SOL", "USDC (Solana)"),
                    ("USDC TRC20", "USDC (TRC20)"),
                    ("XRP", "XRP"),
                    ("LTC", "Litecoin (LTC)"),
                    ("DOGE", "Dogecoin (DOGE)"),
                    ("ADA", "Cardano (ADA)"),
                    ("AVAX", "Avalanche (AVAX)"),
                    ("MATIC", "Polygon (MATIC)"),
                    ("DOT", "Polkadot (DOT)"),
                    ("ATOM", "Cosmos (ATOM)"),
                    ("DAI", "DAI Stablecoin"),
                    ("LINK", "Chainlink (LINK)"),
                    ("TON", "Toncoin (TON)"),
                ],
                max_length=100,
                unique=True,
            ),
        ),
    ]
