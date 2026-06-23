from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_add_image_to_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='withdrawal_source',
            field=models.CharField(
                max_length=10,
                choices=[('balance', 'Balance'), ('profit', 'Profit')],
                default='balance',
                help_text='Source of withdrawal funds (balance or profit)',
            ),
        ),
    ]
