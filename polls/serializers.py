
from rest_framework import serializers

from .models import Poll, Option


class OptionSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Option
        fields = ["id", "text", "vote_count"]


class PollReadSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(
        source="creator.username",
        read_only=True,
    )
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = [
            "id",
            "title",
            "description",
            "creator",
            "status",
            "closes_at",
            "options",
            "created_at",
        ]


class PollCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    options = serializers.ListField(
        child=serializers.CharField(max_length=255),
        min_length=2,
    )
    closes_at = serializers.DateTimeField(
        required=False,
        allow_null=True,
    )

    def validate_options(self, options):
        cleaned = [option.strip() for option in options]

        if any(not option for option in cleaned):
            raise serializers.ValidationError(
                "Options cannot be empty."
            )

        if len(set(option.casefold() for option in cleaned)) != len(cleaned):
            raise serializers.ValidationError(
                "Duplicate options are not allowed."
            )

        return cleaned


class PollUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=255,
        required=False,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    closes_at = serializers.DateTimeField(
        required=False,
        allow_null=True,
    )


class VoteSerializer(serializers.Serializer):
    option_id = serializers.IntegerField(min_value=1)
