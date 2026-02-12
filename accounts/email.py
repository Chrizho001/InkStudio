from djoser import email
from django.conf import settings

class ActivationEmail(email.ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        context["activation_url"] = f"{settings.FRONTEND_URL}/activate/{context['uid']}/{context['token']}"
        return context
