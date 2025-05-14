from rest_framework import serializers

from accounts.api.serializers import UserSerializer
from events_app.models import Event


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source='organizer.username')
    invited_users = UserSerializer(many=True, read_only=True)
    registered_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'date', 'location',
                  'organizer', 'invited_users', 'registered_users',
                  'created', 'updated')
        read_only_fields = ('id', 'organizer', 'invited_users',
                            'registered_users', 'created', 'updated')
