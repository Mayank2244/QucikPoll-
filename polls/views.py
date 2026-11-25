
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import selectors, services
from .models import Poll
from .permissions import IsPollCreatorOrAdmin, IsParticipant
from .serializers import (
    PollReadSerializer,
    PollCreateSerializer,
    PollUpdateSerializer,
    VoteSerializer,
)


class PollListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsPollCreatorOrAdmin()]
        return [IsAuthenticated()]

    def get(self, request):
        polls = selectors.get_polls()
        data = PollReadSerializer(polls, many=True).data
        return Response(data)

    def post(self, request):
        serializer = PollCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        poll = services.create_poll(
            creator=request.user,
            **serializer.validated_data,
        )

        return Response(
            PollReadSerializer(poll).data,
            status=status.HTTP_201_CREATED,
        )


class PollDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, poll_id):
        poll = selectors.get_poll_by_id(poll_id)

        if poll is None:
            return None

        self.check_object_permissions(self.request, poll)
        return poll

    def get(self, request, poll_id):
        poll = self.get_object(poll_id)

        if poll is None:
            return Response(
                {"detail": "Poll not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(PollReadSerializer(poll).data)

    def patch(self, request, poll_id):
        poll = self.get_object(poll_id)

        if poll is None:
            return Response(
                {"detail": "Poll not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        self.check_object_permissions(request, poll)

        serializer = PollUpdateSerializer(
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        try:
            poll = services.update_poll(
                poll=poll,
                **serializer.validated_data,
            )
        except services.PollServiceError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(PollReadSerializer(poll).data)

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsPollCreatorOrAdmin()]
        return [IsAuthenticated()]


class VoteView(APIView):
    permission_classes = [IsAuthenticated, IsParticipant]

    def post(self, request, poll_id):
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            vote = services.cast_vote(
                poll_id=poll_id,
                option_id=serializer.validated_data["option_id"],
                user=request.user,
            )
        except Poll.DoesNotExist:
            return Response(
                {"detail": "Poll not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except services.DuplicateVoteError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_409_CONFLICT,
            )
        except services.PollServiceError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Vote submitted successfully.",
                "vote_id": vote.id,
            },
            status=status.HTTP_201_CREATED,
        )


class PollResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, poll_id):
        poll = selectors.get_poll_by_id(poll_id)

        if poll is None:
            return Response(
                {"detail": "Poll not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        options = selectors.get_poll_results(poll_id)
        total_votes = sum(option.vote_count for option in options)

        results = [
            {
                "option_id": option.id,
                "option": option.text,
                "votes": option.vote_count,
                "percentage": round(
                    option.vote_count * 100 / total_votes, 2
                ) if total_votes else 0,
            }
            for option in options
        ]

        return Response({
            "poll": poll.title,
            "total_votes": total_votes,
            "results": results,
        })


class ClosePollView(APIView):
    permission_classes = [IsAuthenticated, IsPollCreatorOrAdmin]

    def post(self, request, poll_id):
        poll = selectors.get_poll_by_id(poll_id)

        if poll is None:
            return Response(
                {"detail": "Poll not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        self.check_object_permissions(request, poll)

        try:
            poll = services.close_poll(poll=poll)
        except services.PollServiceError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            "message": "Poll closed successfully.",
            "poll": PollReadSerializer(poll).data,
        })
