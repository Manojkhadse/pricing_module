from decimal import Decimal
from django.http import JsonResponse
from .models import PricingConfig

def calculate_price(request):
    try:
        distance = Decimal(request.GET.get('distance', '0'))
        time = Decimal(request.GET.get('time', '0'))
        waiting = Decimal(request.GET.get('waiting', '0'))
        day = request.GET.get('day')
    except:
        return JsonResponse({"error": "Invalid input"}, status=400)

    config = PricingConfig.objects.filter(active=True, valid_days__day=day).first()
    if not config:
        return JsonResponse({"error": "No active config for this day."}, status=400)

    dbp = config.distancebaseprice_set.first()
    dap = config.distanceadditionalprice_set.first()
    wc = config.waitingcharge_set.first()

    additional_distance = max(Decimal('0'), distance - Decimal(dbp.up_to_kms))
    distance_price = dbp.base_price + (additional_distance * dap.price_per_km)

    multiplier = Decimal('1.0')
    for tmf in config.timemultiplierfactor_set.all():
        if tmf.start_hour < float(time) <= tmf.end_hour:
            multiplier = Decimal(str(tmf.multiplier))
            break

    time_price = time * multiplier

    waiting_price = Decimal('0')
    if waiting > wc.after_minutes:
        waiting_price = (waiting - Decimal(wc.after_minutes)) * wc.charge_per_min

    total_price = distance_price + time_price + waiting_price

    return JsonResponse({"total_price": round(total_price, 2)})
