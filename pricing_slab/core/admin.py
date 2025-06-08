from django.contrib import admin
from .models import (
    PricingConfig,
    DayOfWeek,
    DistanceBasePrice,
    DistanceAdditionalPrice,
    TimeMultiplierFactor,
    WaitingCharge,
    ConfigChangeLog
)

# ----- INLINE CLASSES -----

class DistanceBasePriceInline(admin.TabularInline):
    model = DistanceBasePrice
    extra = 1

class DistanceAdditionalPriceInline(admin.TabularInline):
    model = DistanceAdditionalPrice
    extra = 1

class TimeMultiplierFactorInline(admin.TabularInline):
    model = TimeMultiplierFactor
    extra = 1

class WaitingChargeInline(admin.TabularInline):
    model = WaitingCharge
    extra = 1

# ----- PRICING CONFIG ADMIN -----

@admin.register(PricingConfig)
class PricingConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'created_at']
    list_filter = ['active', 'valid_days']
    search_fields = ['name']
    inlines = [
        DistanceBasePriceInline,
        DistanceAdditionalPriceInline,
        TimeMultiplierFactorInline,
        WaitingChargeInline,
    ]
    filter_horizontal = ('valid_days',)

    def save_model(self, request, obj, form, change):
        if obj.active:
            PricingConfig.objects.exclude(pk=obj.pk).update(active=False)
        super().save_model(request, obj, form, change)
        if change:
            ConfigChangeLog.objects.create(
                config=obj,
                changed_by=request.user,
                change_description="Pricing configuration updated."
            )

# ----- OTHER MODELS (INDIVIDUALLY REGISTERED) -----

@admin.register(DayOfWeek)
class DayOfWeekAdmin(admin.ModelAdmin):
    list_display = ['day']


@admin.register(DistanceBasePrice)
class DistanceBasePriceAdmin(admin.ModelAdmin):
    list_display = ['config', 'base_price', 'up_to_kms']


@admin.register(DistanceAdditionalPrice)
class DistanceAdditionalPriceAdmin(admin.ModelAdmin):
    list_display = ['config', 'price_per_km', 'after_kms']


@admin.register(TimeMultiplierFactor)
class TimeMultiplierFactorAdmin(admin.ModelAdmin):
    list_display = ['config', 'start_hour', 'end_hour', 'multiplier']


@admin.register(WaitingCharge)
class WaitingChargeAdmin(admin.ModelAdmin):
    list_display = ['config', 'charge_per_min', 'after_minutes']


@admin.register(ConfigChangeLog)
class ConfigChangeLogAdmin(admin.ModelAdmin):
    list_display = ['config', 'changed_by', 'timestamp']
    readonly_fields = ['timestamp']
