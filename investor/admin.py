from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from decimal import Decimal
from .models import Investor, Investment, ROI, Withdrawal, Testimonial

@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'country', 'created_at']
    list_filter = ['country', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'phone_number']

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['investor', 'amount', 'crypto_type', 'date_invested', 'approved', 'date_approved', 'approval_actions']
    list_filter = ['approved', 'crypto_type', 'date_invested']
    search_fields = ['investor__user__first_name', 'investor__user__last_name', 'investor__user__email', 'transaction_hash']
    actions = ['approve_investments', 'reject_investments']
    readonly_fields = ['date_invested', 'date_approved']
    
    # Make actions more prominent by changing the button text
    class Media:
        js = ('investor/js/admin_custom.js',)
    
    def approval_actions(self, obj):
        if obj.approved:
            return '? Approved'
        else:
            return '? Pending Approval'
    approval_actions.short_description = 'Status'

    def approve_investments(self, request, queryset):
        for investment in queryset:
            if not investment.approved:
                investment.approved = True
                investment.date_approved = timezone.now()
                investment.save()
                
                # Create initial ROI record
                ROI.objects.create(
                    investment=investment,
                    amount=Decimal('0.00')
                )
        
        self.message_user(request, f"{queryset.count()} investments approved successfully. ROI calculation will start from now.")
    approve_investments.short_description = "? APPROVE SELECTED INVESTMENTS"

    def reject_investments(self, request, queryset):
        updated = queryset.update(approved=False, date_approved=None)
        self.message_user(request, f"{updated} investments rejected.")
    reject_investments.short_description = "? REJECT SELECTED INVESTMENTS"

    # Add custom view for pending approvals
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['show_action_buttons'] = True
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ['investor', 'amount', 'crypto_type', 'wallet_address', 'requested_at', 'processed', 'processed_at', 'processing_actions']
    list_filter = ['processed', 'crypto_type', 'requested_at']
    search_fields = ['investor__user__first_name', 'investor__user__last_name', 'wallet_address']
    actions = ['process_withdrawals', 'cancel_withdrawals']
    readonly_fields = ['requested_at', 'processed_at']
    
    class Media:
        js = ('investor/js/admin_custom.js',)
    
    def processing_actions(self, obj):
        if obj.processed:
            return '? Processed'
        else:
            return '? Pending Processing'
    processing_actions.short_description = 'Status'

    def process_withdrawals(self, request, queryset):
        for withdrawal in queryset:
            if not withdrawal.processed:
                withdrawal.processed = True
                withdrawal.processed_at = timezone.now()
                withdrawal.save()
        
        self.message_user(request, f"{queryset.count()} withdrawals processed successfully.")
    process_withdrawals.short_description = "? PROCESS SELECTED WITHDRAWALS"

    def cancel_withdrawals(self, request, queryset):
        updated = queryset.update(processed=False, processed_at=None)
        self.message_user(request, f"{updated} withdrawals cancelled.")
    cancel_withdrawals.short_description = "? CANCEL SELECTED WITHDRAWALS"

    # Add custom view for pending processing
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['show_action_buttons'] = True
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(ROI)
class ROIAdmin(admin.ModelAdmin):
    list_display = ['investment', 'amount', 'date_earned', 'withdrawn']
    list_filter = ['withdrawn', 'date_earned']
    search_fields = ['investment__investor__user__first_name', 'investment__investor__user__last_name']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'created_at']
    list_filter = ['country', 'created_at']
    search_fields = ['name', 'country', 'content']
