import pytz
from datetime import datetime

from celery import shared_task
from django.db import transaction
from django.db.models import Q, Count

import config
from base.services import send_message_to_external_server


@shared_task
def send_mailing(mailing_id):
    from notifications.models import Mailing, Client

    current_time = datetime.now().astimezone(pytz.timezone(config.settings.TIME_ZONE))

    mailing = Mailing.objects.get(id=mailing_id)

    if mailing.start_time <= current_time <= mailing.end_time:
        tag = mailing.filter_params.get('tag')
        operator_code = mailing.filter_params.get('operator_code')
        filter_args = Q()

        if tag:
            filter_args &= Q(tag__in=tag)
        if operator_code:
            filter_args &= Q(operator_code__in=operator_code)

        clients = Client.objects.filter(filter_args)

        for client in clients:
            send_message.delay(client.id, mailing_id)

    elif current_time < mailing.start_time:
        send_mailing.apply_async((mailing_id,), eta=mailing.start_time)


@shared_task
def send_message(client_id, mailing_id):
    from notifications.models import Message, Client, Mailing

    client = Client.objects.get(id=client_id)
    mailing = Mailing.objects.get(id=mailing_id)
    message = Message.objects.create(client=client, mailing=mailing)

    response = send_message_to_external_server(message.pk, client.phone_number, mailing.text,
                                               'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTQ4Mjg3ODMsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9TcGl0X2l0In0.T4jW4KFGhnTIzFa_mFJbINp6dBwFcoF5Qj3Dn-Avtc0')
    if response.status_code == 200:
        message.status = 'sent'
        message.save()
    else:
        message.status = 'failed'
        message.save()
        send_message.apply_async((client_id, mailing_id), countdown=180)
    set_mailing_statistics.delay(mailing_id)

@shared_task
def set_mailing_statistics(mailing_id):
    from notifications.models import Mailing
    with transaction.atomic():
        mailing = Mailing.objects.prefetch_related('messages',).filter(id=mailing_id).\
            annotate(sent_messages=Count('messages', filter=Q(messages__status='sent')), total=Count('messages'))[0]
        mailing.sent_count = mailing.sent_messages
        mailing.total_count = mailing.total
        mailing.save()