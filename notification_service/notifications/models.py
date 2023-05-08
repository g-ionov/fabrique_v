from django.db import models

from base.validators import phone_number_validation, filter_validator


class Client(models.Model):
    """ Client model """
    phone_number = models.CharField(max_length=11, unique=True, validators=[phone_number_validation])
    operator_code = models.CharField(max_length=3)
    tag = models.CharField(max_length=50, null=True, blank=True)
    timezone = models.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_phone_number = self.phone_number

    def save(self, *args, **kwargs):
        if self.phone_number != self.__original_phone_number or not self.operator_code:
            self.operator_code = self.phone_number[1:4]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.phone_number}'


class Mailing(models.Model):
    """ Mailing model """
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    text = models.TextField()
    filter_params = models.JSONField(default=dict, validators=[filter_validator])
    sent_count = models.IntegerField(default=0)
    total_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.text[:20]}'


class Message(models.Model):
    """ Message model """
    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='messages')
    send_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.client} {self.mailing} {self.status}'

    class Meta:
        unique_together = ('client', 'mailing')
