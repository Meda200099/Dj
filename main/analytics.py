from django.db.models import Avg, Count, Sum
from django.db.models.functions import ExtractHour, ExtractWeekDay

from .club_data import ZONE_FILTERS
from .models import Appointment, CatalogSession, TariffPageView


def format_duration(seconds):
    seconds = int(seconds or 0)
    if seconds < 60:
        return f"{seconds} сек"
    minutes, secs = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes} мин {secs} сек" if secs else f"{minutes} мин"
    hours, mins = divmod(minutes, 60)
    return f"{hours} ч {mins} мин"


ZONE_LABELS = {f["key"]: f["label"] for f in ZONE_FILTERS}

WEEKDAY_LABELS = {
    1: "Вс",
    2: "Пн",
    3: "Вт",
    4: "Ср",
    5: "Чт",
    6: "Пт",
    7: "Сб",
}


def _add_bar_pct(items, value_key):
    max_val = max((item[value_key] for item in items), default=0)
    for item in items:
        item["bar_pct"] = round(item[value_key] / max_val * 100) if max_val else 0
    return items


def get_analytics_context():
    active_bookings = Appointment.objects.filter(
        status__in=[Appointment.STATUS_PENDING, Appointment.STATUS_CONFIRMED]
    )

    popular_tariffs = _add_bar_pct(list(
        active_bookings.values("tariff")
        .annotate(bookings=Count("id"))
        .order_by("-bookings", "tariff")[:8]
    ), "bookings")

    popular_seats = _add_bar_pct(list(
        active_bookings.values("seat")
        .annotate(bookings=Count("id"))
        .order_by("-bookings", "seat")[:10]
    ), "bookings")

    tariff_views = _add_bar_pct(list(
        TariffPageView.objects.values("tariff")
        .annotate(views=Count("id"))
        .order_by("-views", "tariff")[:8]
    ), "views")

    buyer_catalog_time = []
    for row in (
        CatalogSession.objects.filter(user__isnull=False)
        .values("user_id", "user__username", "user__first_name")
        .annotate(total_seconds=Sum("duration_seconds"), visits=Count("id"))
        .order_by("-total_seconds")[:15]
    ):
        buyer_catalog_time.append({
            **row,
            "duration_display": format_duration(row["total_seconds"]),
            "avg_display": format_duration(
                (row["total_seconds"] or 0) // max(row["visits"], 1)
            ),
        })

    zone_stats = []
    zone_rows = list(
        CatalogSession.objects.values("zone")
        .annotate(views=Count("id"), total_seconds=Sum("duration_seconds"))
        .order_by("-views")
    )
    _add_bar_pct(zone_rows, "views")
    for row in zone_rows:
        zone_key = row["zone"] or "all"
        zone_stats.append({
            "zone": zone_key,
            "label": ZONE_LABELS.get(zone_key, "Все зоны"),
            "views": row["views"],
            "bar_pct": row["bar_pct"],
            "total_seconds": row["total_seconds"] or 0,
            "duration_display": format_duration(row["total_seconds"]),
        })

    peak_hours = []
    peak_hour_rows = list(
        active_bookings.annotate(hour=ExtractHour("appointment_time"))
        .values("hour")
        .annotate(bookings=Count("id"))
        .order_by("-bookings")[:6]
    )
    _add_bar_pct(peak_hour_rows, "bookings")
    for row in peak_hour_rows:
        peak_hours.append({
            "hour": row["hour"],
            "label": f"{row['hour']:02d}:00",
            "bookings": row["bookings"],
            "bar_pct": row["bar_pct"],
        })

    peak_days = []
    peak_day_rows = list(
        active_bookings.annotate(weekday=ExtractWeekDay("appointment_date"))
        .values("weekday")
        .annotate(bookings=Count("id"))
        .order_by("-bookings")
    )
    _add_bar_pct(peak_day_rows, "bookings")
    for row in peak_day_rows:
        peak_days.append({
            "weekday": row["weekday"],
            "label": WEEKDAY_LABELS.get(row["weekday"], "?"),
            "bookings": row["bookings"],
            "bar_pct": row["bar_pct"],
        })

    catalog_agg = CatalogSession.objects.aggregate(
        sessions=Count("id"),
        avg_seconds=Avg("duration_seconds"),
        total_seconds=Sum("duration_seconds"),
    )
    active_appointments = active_bookings.count()
    catalog_sessions = catalog_agg["sessions"] or 0
    conversion_pct = round(
        active_appointments / catalog_sessions * 100, 1
    ) if catalog_sessions else 0

    recent_sessions = []
    for session in CatalogSession.objects.select_related("user").order_by("-started_at")[:20]:
        recent_sessions.append({
            "started_at": session.started_at,
            "user": session.user,
            "zone": session.zone or "all",
            "duration_display": format_duration(session.duration_seconds),
        })

    return {
        "popular_tariffs": popular_tariffs,
        "popular_seats": popular_seats,
        "tariff_views": tariff_views,
        "buyer_catalog_time": buyer_catalog_time,
        "zone_stats": zone_stats,
        "peak_hours": peak_hours,
        "peak_days": peak_days,
        "catalog_sessions": catalog_sessions,
        "avg_catalog_time": format_duration(catalog_agg["avg_seconds"]),
        "total_catalog_time": format_duration(catalog_agg["total_seconds"]),
        "conversion_pct": conversion_pct,
        "recent_sessions": recent_sessions,
    }
