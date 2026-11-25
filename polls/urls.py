
from django.urls import path

from .views import (
    PollListCreateView,
    PollDetailView,
    VoteView,
    PollResultsView,
    ClosePollView,
)

urlpatterns = [
    path("polls/", PollListCreateView.as_view(), name="poll-list-create"),
    path("polls/<int:poll_id>/", PollDetailView.as_view(), name="poll-detail"),
    path("polls/<int:poll_id>/vote/", VoteView.as_view(), name="poll-vote"),
    path("polls/<int:poll_id>/results/", PollResultsView.as_view(), name="poll-results"),
    path("polls/<int:poll_id>/close/", ClosePollView.as_view(), name="poll-close"),
]
