from django.contrib import admin

# Register your models here.
from .models import EmailVerificationEvent,Email

admin.site.register(Email)
admin.site.register(EmailVerificationEvent)

# @admin.register(EmailVerificationEvent)
# class EmailVerificationEventAdmin(admin.ModelAdmin):
#     list_display = (
#         'parent', 
#         'email', 
#         'attempts', 
#         'last_attempt_at', 
#         'expired', 
#         'expired_at', 
#         'timestamp'
#     ) 