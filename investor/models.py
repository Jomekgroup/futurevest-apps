from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import datetime
from django.utils import timezone

class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Investment(models.Model):
    CRYPTO_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('ETH', 'Ethereum'),
        ('USDT', 'Tether'),
    ]
    
    CRYPTO_ADDRESSES = {
        'BTC': 'bc1q95jwwr57qlrufgcqhuqvt7efv0020z4c6aydcr',
        'ETH': '0x59a3E73de68E6829C97c40B4812e2d38148BE623',
        'USDT': '0x59a3E73de68E6829C97c40B4812e2d38148BE623',
    }
    
    CRYPTO_NETWORKS = {
        'BTC': 'Bitcoin Mainnet',
        'ETH': 'Ethereum ERC20',
        'USDT': 'Ethereum ERC20',
    }
    
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('10.00'))])
    date_invested = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    crypto_type = models.CharField(max_length=10, choices=CRYPTO_CHOICES)
    transaction_hash = models.CharField(max_length=100, blank=True)
    
    @property
    def crypto_address(self):
        return self.CRYPTO_ADDRESSES.get(self.crypto_type, '')
    
    @property
    def crypto_network(self):
        return self.CRYPTO_NETWORKS.get(self.crypto_type, '')
    
    @property
    def days_since_investment(self):
        if self.approved and self.date_approved:
            return (timezone.now() - self.date_approved).days
        return 0
    
    @property
    def total_roi(self):
        if self.approved and self.date_approved:
            days_since_approval = (timezone.now() - self.date_approved).days
            if days_since_approval >= 30:
                days_earning_roi = days_since_approval - 30
                if days_earning_roi > 0:
                    return self.amount * Decimal('0.003') * days_earning_roi
        return Decimal('0.00')
    
    def __str__(self):
        return f"{self.investor.user.username} -  - {self.crypto_type}"

class ROI(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    date_earned = models.DateTimeField(auto_now_add=True)
    withdrawn = models.BooleanField(default=False)
    
    def __str__(self):
        return f"ROI:  for Investment #{self.investment.id}"

class Withdrawal(models.Model):
    CRYPTO_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('ETH', 'Ethereum'),
        ('USDT', 'Tether'),
    ]
    
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    crypto_type = models.CharField(max_length=10, choices=CRYPTO_CHOICES)
    wallet_address = models.CharField(max_length=100)
    requested_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Withdrawal:  by {self.investor.user.username}"

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Testimonial by {self.name}"
