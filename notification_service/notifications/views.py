from rest_framework import viewsets

from notifications.serializers import ClientSerializer, ClientCreateSerializer, MailingSerializer, \
    MailingCreateSerializer, MailingDetailSerializer
from notifications.services import get_clients, get_mailing, get_mailing_details


class ClientViewSet(viewsets.ModelViewSet):
    queryset = get_clients()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return ClientCreateSerializer
        return ClientSerializer


class MailingViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return MailingCreateSerializer
        elif self.action == 'retrieve':
            return MailingDetailSerializer
        return MailingSerializer

    def get_queryset(self):
        if self.action == 'retrieve':
            return get_mailing_details(self.kwargs.get('pk'))
        return get_mailing()
