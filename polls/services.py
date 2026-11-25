
from django.db import IntegrityError, transaction
from django.utils import timezone

from .models import Poll, Option, Vote


class PollServiceError(Exception):
    """Base exception for poll business logic errors."""


class PollClosedError(PollServiceError):
    pass


class DuplicateVoteError(PollServiceError):
    pass


class InvalidOptionError(PollServiceError):
    pass


def create_poll(*, creator, title, description="", options, closes_at=None):
    """Create a poll and its options."""
    if not options or len(options) < 2:
        raise PollServiceError("A poll must have at least two options.")

    with transaction.atomic():
        poll = Poll.objects.create(
            creator=creator,
            title=title,
            description=description,
            closes_at=closes_at,
        )

        Option.objects.bulk_create([
            Option(poll=poll, text=option_text)
            for option_text in options
        ])

    return poll


def update_poll(*, poll, title=None, description=None, closes_at=None):
    """Update an existing poll."""
    if poll.status == Poll.Status.CLOSED:
        raise PollClosedError("Closed polls cannot be updated.")

    if title is not None:
        poll.title = title

    if description is not None:
        poll.description = description

    if closes_at is not None:
        poll.closes_at = closes_at

    poll.save()
    return poll


def cast_vote(*, poll_id, option_id, user):
    """Cast one vote per user for an active poll."""
    try:
        with transaction.atomic():
            poll = Poll.objects.select_for_update().get(id=poll_id)

            if poll.status != Poll.Status.ACTIVE:
                raise PollClosedError("This poll is closed.")

            if poll.closes_at and poll.closes_at <= timezone.now():
                raise PollClosedError("The voting deadline has passed.")

            option = Option.objects.filter(
                id=option_id,
                poll=poll,
            ).first()

            if option is None:
                raise InvalidOptionError(
                    "The selected option does not belong to this poll."
                )

            vote = Vote.objects.create(
                poll=poll,
                option=option,
                user=user,
            )

            return vote

    except IntegrityError as exc:
        raise DuplicateVoteError(
            "You have already voted in this poll."
        ) from exc


def close_poll(*, poll):
    """Close an active poll."""
    if poll.status == Poll.Status.CLOSED:
        raise PollClosedError("This poll is already closed.")

    poll.status = Poll.Status.CLOSED
    poll.save(update_fields=["status", "updated_at"])

    return poll
