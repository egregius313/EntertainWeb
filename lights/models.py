from django.db import models


class ButtonDivider(models.Model):
    divider_name = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.divider_name

    def __eq__(self, other):
        if isinstance(other, ButtonDivider):
            return self.divider_name == other.divider_name
        return NotImplemented


class Button(models.Model):
    button_name = models.CharField(max_length=20, default='')
    related_color = models.CharField(max_length=11, default='000,000,000')
    message_string = models.CharField(max_length=595, default='')  # current max length of color string
    parent_divider = models.ForeignKey(ButtonDivider, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.button_name
