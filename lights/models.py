import datetime
import random

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


def unique_random_num():
    rand_num = random.randrange(1000, 10000)
    try:
        AccessToken.objects.get(pk=rand_num)
    except AccessToken.DoesNotExist:
        return rand_num
    else:
        return unique_random_num()


def now_plus_some():
    return timezone.now() + datetime.timedelta(hours=1)


class ButtonDivider(models.Model):
    divider_name = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.divider_name

    def __eq__(self, other):
        if isinstance(other, ButtonDivider):
            return self.divider_name == other.divider_name
        return NotImplemented


class Button(models.Model):
    button_name = models.CharField(max_length=8, default='')
    related_color = models.CharField(max_length=11, default='000,000,000')
    message_string = models.CharField(max_length=595, default='')  # current max length of color string
    svg_image = models.CharField(max_length=256, default='none')
    parent_divider = models.ForeignKey(ButtonDivider, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.button_name


class AccessToken(models.Model):
    token = models.IntegerField(primary_key=True, validators=[MaxValueValidator(9999), MinValueValidator(1000)], default=unique_random_num)
    expiry_date = models.DateTimeField(default=now_plus_some)
    in_use = models.BooleanField(default=False)
    notes = models.CharField(default='', max_length=512)

    def __str__(self):
        return str(self.token)
