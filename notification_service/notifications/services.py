from django.db.models import QuerySet

from notifications.models import Client, Mailing



def get_clients() -> QuerySet:
    """Get all clients from database"""
    return Client.objects.all()


def get_mailing() -> QuerySet:
    """Get all mailing from database"""
    return Mailing.objects.all()


def get_mailing_details(mailing_id: int) -> Mailing:
    """Get mailing detail information with sent messages"""
    return Mailing.objects.prefetch_related('messages').filter(id=mailing_id)