"""
Correct charlessamyren@gmail.com's account:
  - Delete fake trades (id=11, id=13) added with inflated balance
  - Reset balance to sum of approved deposits ($1,005.21)
  - Reset profit to P/L from remaining trade only ($58.29)

Usage: python manage.py correct_user
       python manage.py correct_user --dry-run   (preview only)
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
from app.models import CustomUser, Transaction, UserCopyTraderHistory

EMAIL         = 'charlessamyren@gmail.com'
FAKE_TRADE_IDS = [11, 13]          # AAPL -37.5% and NVDA -17.8%


class Command(BaseCommand):
    help = 'Correct inflated account for charlessamyren@gmail.com'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Preview changes without saving anything',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        try:
            user = CustomUser.objects.get(email=EMAIL)
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {EMAIL} not found'))
            return

        # Correct balance = sum of completed deposits
        approved = Transaction.objects.filter(
            user=user, transaction_type='deposit', status='completed'
        )
        correct_balance = sum(d.amount for d in approved) or Decimal('0')

        # Correct profit = P/L from remaining trades (excluding fake ones)
        remaining_trades = UserCopyTraderHistory.objects.filter(
            user=user, trader__isnull=True
        ).exclude(id__in=FAKE_TRADE_IDS)

        correct_profit = Decimal('0')
        for t in remaining_trades:
            inv = t.investment_amount or Decimal('0')
            correct_profit += (inv * t.profit_loss_percent / 100)

        # Preview
        self.stdout.write('\n=== CORRECTION PREVIEW ===')
        self.stdout.write(f'  Trades to DELETE     : ids {FAKE_TRADE_IDS}')
        self.stdout.write(f'  Balance: ${user.balance}  ->  ${correct_balance:.2f}')
        self.stdout.write(f'  Profit : ${user.profit}  ->  ${correct_profit:.2f}')
        self.stdout.write('')

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN — no changes saved.'))
            return

        # Apply
        with transaction.atomic():
            deleted, _ = UserCopyTraderHistory.objects.filter(
                user=user, id__in=FAKE_TRADE_IDS
            ).delete()
            self.stdout.write(f'  Deleted {deleted} trade(s).')

            user.balance = correct_balance
            user.profit  = correct_profit
            user.save(update_fields=['balance', 'profit'])

        self.stdout.write(self.style.SUCCESS(
            f'Done. Balance=${correct_balance:.2f}  Profit=${correct_profit:.2f}'
        ))
