"""
Read-only audit of a user's financial state.
Usage: python manage.py audit_user charlessamyren@gmail.com
"""
from django.core.management.base import BaseCommand
from django.db.models import Sum
from decimal import Decimal
from app.models import CustomUser, Transaction, UserCopyTraderHistory


class Command(BaseCommand):
    help = 'Audit a user financial state'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        email = options['email']
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {email} not found'))
            return

        self.stdout.write(self.style.SUCCESS(f'\n=== USER: {user.email} ==='))
        self.stdout.write(f'  Current balance : ${user.balance}')
        self.stdout.write(f'  Current profit  : ${user.profit}')
        self.stdout.write('')

        # ── Deposits ──────────────────────────────────────────────────────────
        deposits = Transaction.objects.filter(
            user=user, transaction_type='deposit'
        ).order_by('created_at')

        self.stdout.write(self.style.WARNING('--- DEPOSITS ---'))
        total_approved = Decimal('0')
        for d in deposits:
            mark = 'OK' if d.status == 'completed' else '--'
            self.stdout.write(
                f'  [{mark}] ${d.amount:>10}  status={d.status:<10}  '
                f'ref={d.reference}  date={d.created_at.strftime("%Y-%m-%d")}'
            )
            if d.status == 'completed':
                total_approved += d.amount
        self.stdout.write(f'  TOTAL APPROVED DEPOSITS: ${total_approved}')
        self.stdout.write('')

        # ── Withdrawals ───────────────────────────────────────────────────────
        withdrawals = Transaction.objects.filter(
            user=user, transaction_type='withdrawal'
        ).order_by('created_at')

        self.stdout.write(self.style.WARNING('--- WITHDRAWALS ---'))
        total_withdrawn = Decimal('0')
        for w in withdrawals:
            mark = 'OK' if w.status == 'completed' else '--'
            self.stdout.write(
                f'  [{mark}] ${w.amount:>10}  status={w.status:<10}  '
                f'ref={w.reference}  date={w.created_at.strftime("%Y-%m-%d")}'
            )
            if w.status == 'completed':
                total_withdrawn += w.amount
        self.stdout.write(f'  TOTAL COMPLETED WITHDRAWALS: ${total_withdrawn}')
        self.stdout.write('')

        # ── Direct trades ─────────────────────────────────────────────────────
        direct_trades = UserCopyTraderHistory.objects.filter(
            user=user, trader__isnull=True
        ).order_by('opened_at')

        self.stdout.write(self.style.WARNING('--- DIRECT TRADES ---'))
        total_trade_profit = Decimal('0')
        for t in direct_trades:
            inv = t.investment_amount or Decimal('0')
            pl_dollar = (inv * t.profit_loss_percent / 100) if inv else Decimal('0')
            total_trade_profit += pl_dollar
            self.stdout.write(
                f'  id={t.id:<6} market={t.market:<10} pl%={t.profit_loss_percent:>7}  '
                f'inv=${inv:>10}  pl$={pl_dollar:>10.2f}  '
                f'status={t.status:<6}  date={t.opened_at.strftime("%Y-%m-%d")}'
            )
        self.stdout.write(f'  TOTAL DIRECT TRADE P/L: ${total_trade_profit:.2f}')
        self.stdout.write('')

        # ── Summary ───────────────────────────────────────────────────────────
        expected_balance = total_approved - total_withdrawn
        self.stdout.write(self.style.SUCCESS('--- EXPECTED vs ACTUAL ---'))
        self.stdout.write(f'  Expected balance (deposits - withdrawals) : ${expected_balance:.2f}')
        self.stdout.write(f'  Actual balance                            : ${user.balance}')
        self.stdout.write(f'  Balance discrepancy                       : ${user.balance - expected_balance:.2f}')
        self.stdout.write('')
        self.stdout.write(f'  Expected profit (sum of direct trade P/L) : ${total_trade_profit:.2f}')
        self.stdout.write(f'  Actual profit                             : ${user.profit}')
        self.stdout.write(f'  Profit discrepancy                        : ${user.profit - total_trade_profit:.2f}')
        self.stdout.write('')
