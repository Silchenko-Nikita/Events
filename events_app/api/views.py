from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from events_app.api.filters import EventFilter
from events_app.api.serializers import EventSerializer
from events_app.models import Event


class IsAuthenticatedAndOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.organizer == request.user


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedAndOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EventFilter
    search_fields = ['title', 'description', 'location', 'organizer__username']
    ordering_fields = ['date', 'created', 'updated']
    ordering = ['date']

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def invite(self, request, pk=None):
        event = self.get_object()

        if event.organizer != request.user:
            return Response({"error": "Only the event organizer can invite users"}, status=status.HTTP_403_FORBIDDEN)

        if 'invited_user_ids' not in request.data:
            return Response({"error": "'invited_user_ids' is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_ids = request.data.get('invited_user_ids', [])
        if not isinstance(user_ids, list):
            return Response({"error": "invited_user_ids must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        invited = []
        already_invited = []
        already_registered = []
        invalid_ids = []
        not_found = []

        for user_id in user_ids:
            try:
                user_id = int(user_id)
            except (TypeError, ValueError):
                invalid_ids.append(user_id)
                continue

            try:
                user = User.objects.get(id=user_id)

                if user in event.registered_users.all():
                    already_registered.append(user.username)
                elif user in event.invited_users.all():
                    already_invited.append(user.username)
                else:
                    event.invited_users.add(user)
                    invited.append(user.username)

            except User.DoesNotExist:
                not_found.append(user_id)

        response_data = {}
        if invited:
            response_data['invited'] = invited
        if already_invited:
            response_data['already_invited'] = already_invited
        if already_registered:
            response_data['already_registered'] = already_registered
        if invalid_ids:
            response_data['invalid_ids'] = invalid_ids
        if not_found:
            response_data['not_found'] = not_found

        return Response(response_data, status=status.HTTP_200_OK if invited else status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def confirm_registration(self, request, pk=None):
        event = self.get_object()
        user = request.user

        if user in event.registered_users.all():
            return Response({"error": "User already registered for this event"}, status=status.HTTP_400_BAD_REQUEST)

        if user in event.invited_users.all():
            event.invited_users.remove(user)
            event.registered_users.add(user)
            return Response({"message": f"{user.username} registered for the event"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not invited to this event"}, status=status.HTTP_403_FORBIDDEN)
