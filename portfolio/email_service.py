import resend
from django.conf import settings
from django.template.loader import render_to_string


def send_enquiry_email(enquiry):
    """Send a validated contact enquiry through Resend's Python SDK."""
    if not settings.RESEND_API_KEY:
        raise RuntimeError("RESEND_API_KEY is not configured")

    resend.api_key = settings.RESEND_API_KEY
    context = {**enquiry, "recipient": settings.CONTACT_TO_EMAIL}
    params = {
        "from": settings.RESEND_FROM_EMAIL,
        "to": [settings.CONTACT_TO_EMAIL],
        "reply_to": [enquiry["email"]],
        "subject": f"Portfolio enquiry: {enquiry['service_label']}",
        "text": render_to_string("portfolio/emails/enquiry.txt", context),
        "html": render_to_string("portfolio/emails/enquiry.html", context),
    }
    return resend.Emails.send(params)
