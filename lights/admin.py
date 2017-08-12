from django.contrib import admin

from .models import Button, ButtonDivider


class ButtonAdmin(admin.ModelAdmin):
    list_display = ('enabled', 'button_name', 'message_string', 'parent_divider')

    list_filter = ['parent_divider', 'enabled']
    search_fields = ['button_name', 'message_string']

admin.site.register(Button, ButtonAdmin)
admin.site.register(ButtonDivider)
