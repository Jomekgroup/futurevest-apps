from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django.contrib import messages
from .models import Investor, Investment, ROI, Withdrawal, Testimonial
from .forms import InvestorSignupForm, InvestmentForm, WithdrawalForm

def index(request):
    testimonials = Testimonial.objects.all()[:3]
    return render(request, 'investor/index.html', {'testimonials': testimonials})

def investor_signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        # Get form data directly from request.POST
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        country_with_code = request.POST.get('country')
        
        # Extract clean country name (remove phone code)
        country = country_with_code.split(' (')[0] if country_with_code and ' (' in country_with_code else country_with_code
        
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Basic validation
        if not all([full_name, email, phone_number, country, password1, password2]):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'investor/signup.html')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'investor/signup.html')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'investor/signup.html')
        
        # Split full name into first and last name
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        try:
            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create investor profile
            investor = Investor.objects.create(
                user=user,
                phone_number=phone_number,
                country=country
            )
            
            # Log the user in
            user = authenticate(request, username=email, password=password1)
            if user is not None:
                login(request, user)
                messages.success(request, 'Account created successfully! Welcome to FutureVest.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Authentication failed. Please try logging in.')
                return redirect('investor_login')
                
        except Exception as e:
            messages.error(request, 'An error occurred during registration. Please try again.')
            return render(request, 'investor/signup.html')
    
    return render(request, 'investor/signup.html')

def investor_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return render(request, 'investor/login.html')
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    
    return render(request, 'investor/login.html')

@login_required
def investor_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('index')

@login_required
def dashboard(request):
    try:
        investor = Investor.objects.get(user=request.user)
    except Investor.DoesNotExist:
        messages.error(request, 'Please complete your investor profile.')
        return redirect('investor_signup')
    
    # Get approved investments
    investments = Investment.objects.filter(investor=investor, approved=True)
    
    # Calculate total invested
    total_invested = sum(investment.amount for investment in investments)
    
    # Calculate ROI
    total_roi = Decimal('0.00')
    daily_roi = Decimal('0.00')
    total_withdrawable = Decimal('0.00')
    
    # Update ROI for all investments
    for investment in investments:
        # Calculate days since approval
        if investment.date_approved:
            days_since_approval = (timezone.now() - investment.date_approved).days
            
            # Only count ROI after 30 days
            if days_since_approval >= 30:
                # Calculate ROI (0.3% daily after 30 days)
                days_earning_roi = days_since_approval - 30
                if days_earning_roi > 0:
                    investment_roi = investment.amount * Decimal('0.003') * days_earning_roi
                    total_roi += investment_roi
                    
                    # Add to withdrawable amount
                    total_withdrawable += investment_roi
            
            # Add daily ROI for current day (if past 30 days)
            if days_since_approval >= 30:
                daily_roi += investment.amount * Decimal('0.003')
    
    # Get pending investments
    pending_investments = Investment.objects.filter(investor=investor, approved=False)
    
    context = {
        'investor': investor,
        'investments': investments,
        'pending_investments': pending_investments,
        'total_invested': total_invested,
        'daily_roi': daily_roi,
        'total_roi': total_roi,
        'total_withdrawable': total_withdrawable,
    }
    
    return render(request, 'investor/dashboard.html', context)

@login_required
def invest(request):
    try:
        investor = Investor.objects.get(user=request.user)
    except Investor.DoesNotExist:
        messages.error(request, 'Please complete your investor profile.')
        return redirect('investor_signup')
    
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.investor = investor
            
            # Add transaction hash if provided
            transaction_hash = request.POST.get('transaction_hash', '')
            if transaction_hash:
                investment.transaction_hash = transaction_hash
            
            investment.save()
            messages.success(request, 'Your investment has been submitted for approval. It will start counting once admin confirms receipt of payment.')
            return redirect('dashboard')
    else:
        form = InvestmentForm()
    
    # Crypto information with both local and online QR code options
    crypto_info = {
        'BTC': {
            'address': 'bc1q95jwwr57qlrufgcqhuqvt7efv0020z4c6aydcr',
            'network': 'Bitcoin Mainnet',
            'qr_code': '/static/investor/images/btc_qr.png',
            'online_qr': 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=bitcoin%3Abc1q95jwwr57qlrufgcqhuqvt7efv0020z4c6aydcr'
        },
        'ETH': {
            'address': '0x59a3E73de68E6829C97c40B4812e2d38148BE623',
            'network': 'Ethereum ERC20',
            'qr_code': '/static/investor/images/eth_qr.png',
            'online_qr': 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=0x59a3E73de68E6829C97c40B4812e2d38148BE623'
        },
        'USDT': {
            'address': '0x59a3E73de68E6829C97c40B4812e2d38148BE623',
            'network': 'Ethereum ERC20',
            'qr_code': '/static/investor/images/usdt_qr.png',
            'online_qr': 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=0x59a3E73de68E6829C97c40B4812e2d38148BE623'
        }
    }
    
    return render(request, 'investor/invest.html', {
        'form': form,
        'crypto_info': crypto_info
    })

@login_required
def withdraw(request):
    try:
        investor = Investor.objects.get(user=request.user)
    except Investor.DoesNotExist:
        messages.error(request, 'Please complete your investor profile.')
        return redirect('investor_signup')
    
    # Get approved investments that are at least 30 days old
    eligible_investments = Investment.objects.filter(
        investor=investor, 
        approved=True,
        date_approved__isnull=False
    )
    
    # Calculate available amount to withdraw
    available_amount = Decimal('0.00')
    for investment in eligible_investments:
        if investment.date_approved:
            days_since_approval = (timezone.now() - investment.date_approved).days
            if days_since_approval >= 30:
                days_earning_roi = days_since_approval - 30
                if days_earning_roi > 0:
                    available_amount += investment.amount * Decimal('0.003') * days_earning_roi
    
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.investor = investor
            
            # Check if withdrawal amount is valid
            if withdrawal.amount <= available_amount:
                withdrawal.save()
                messages.success(request, 'Your withdrawal request has been submitted. Admin will process it within 24-48 hours.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Insufficient funds for withdrawal.')
    
    else:
        form = WithdrawalForm()
    
    context = {
        'form': form,
        'available_amount': available_amount,
    }
    
    return render(request, 'investor/withdraw.html', context)

def test_filter(request):
    return render(request, 'investor/test.html')

