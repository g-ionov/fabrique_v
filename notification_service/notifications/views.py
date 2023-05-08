from rest_framework import viewsets


from notifications.serializers import ClientSerializer, ClientCreateSerializer, MailingSerializer, \
    MailingCreateSerializer
from notifications.services import get_clients, get_mailing


class ClientViewSet(viewsets.ModelViewSet):
    queryset = get_clients()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return ClientCreateSerializer
        return ClientSerializer


class MailingViewSet(viewsets.ModelViewSet):
    queryset = get_mailing()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return MailingCreateSerializer
        return MailingSerializer
