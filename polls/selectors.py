
from django.db.models import Count, Prefetch, Q
from django.utils import timezone

from .models import Poll, Option


def get_polls():
    """Return all polls with their options and vote counts."""
    return (
        Poll.objects
        .select_related("creator")
        .prefetch_related(
            Prefetch(
                "options",
                queryset=Option.objects.annotate(
                    vote_count=Count("votes")
                ),
            )
        )
    )


def get_poll_by_id(poll_id):
    """Return a single poll with its related data."""
    return (
        get_polls()
        .filter(id=poll_id)
        .first()
    )


def get_active_polls():
    """Return polls that are active and have not expired."""
    now = timezone.now()

    return get_polls().filter(
        Q(closes_at__isnull=True) | Q(closes_at__gt=now),
        status=Poll.Status.ACTIVE,
    )

def get_poll_results(poll_id):
    """Return poll options with their vote counts."""
    return (
        Option.objects
        .filter(poll_id=poll_id)
        .annotate(vote_count=Count("votes"))
        .order_by("id")
    )
