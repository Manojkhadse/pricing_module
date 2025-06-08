from django.db import models
from django.contrib.auth.models import User

DAYS = [
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday'),
    ('Sun', 'Sunday'),
]

class PricingConfig(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    valid_days = models.ManyToManyField('DayOfWeek')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DayOfWeek(models.Model):
    day = models.CharField(choices=DAYS, max_length=3, unique=True)

class DistanceBasePrice(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    up_to_kms = models.FloatField()

class DistanceAdditionalPrice(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE)
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    after_kms = models.FloatField()

class TimeMultiplierFactor(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE)
    start_hour = models.FloatField()
    end_hour = models.FloatField()
    multiplier = models.FloatField()

class WaitingCharge(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE)
    charge_per_min = models.DecimalField(max_digits=10, decimal_places=2)
    after_minutes = models.IntegerField()

class ConfigChangeLog(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    change_description = models.TextField()
