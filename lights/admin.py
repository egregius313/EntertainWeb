from django.contrib import admin

from .models import Button, ButtonDivider, AccessToken


class ButtonAdmin(admin.ModelAdmin):
    list_display = ('enabled', 'button_name', 'message_string', 'parent_divider')

    list_filter = ['parent_divider', 'enabled']
    search_fields = ['button_name', 'message_string']


class TokenAdmin(admin.ModelAdmin):
    list_display = ('in_use', 'expiry_date', 'token')

    list_filter = ['in_use', 'expiry_date']
    search_fields = ['token']

admin.site.register(Button, ButtonAdmin)
admin.site.register(ButtonDivider)
admin.site.register(AccessToken, TokenAdmin)
