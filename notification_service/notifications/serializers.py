from rest_framework import serializers

from notifications.models import Client, Mailing, Message


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('phone_number', 'tag', 'timezone')


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ('id', 'start_time', 'end_time', 'sent_count', 'total_count')


class MailingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ('start_time', 'end_time', 'text', 'filter_params')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'client', 'send_time', 'status')


class MailingDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Mailing
        fields = ('id', 'start_time', 'end_time', 'text', 'filter_params', 'sent_count', 'total_count', 'messages')