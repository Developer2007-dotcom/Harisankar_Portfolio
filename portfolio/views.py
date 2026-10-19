import logging

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .email_service import send_enquiry_email
from .forms import EnquiryForm, SERVICE_CHOICES

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "portfolio/home.html")


def about(request):
    return render(request, "portfolio/about.html")


def work(request):
    return render(request, "portfolio/work.html")


def skills(request):
    return render(request, "portfolio/skills.html")


def health_check(request):
    return HttpResponse("ok", content_type="text/plain")


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("portfolio:sitemap"))
    return HttpResponse(
        f"User-agent: *\nAllow: /\nSitemap: {sitemap_url}\n",
        content_type="text/plain",
    )


def sitemap_xml(request):
    from xml.sax.saxutils import escape

    page_paths = ("", "about/", "work/", "skills/", "contact/")
    entries = "".join(
        f"<url><loc>{escape(request.build_absolute_uri('/' + path))}</loc></url>"
        for path in page_paths
    )
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>'
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")


def contact(request):
    form = EnquiryForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        # Silently accept honeypot submissions without sending email.
        if data["website"]:
            return redirect(reverse("portfolio:contact") + "?sent=1")
        service_labels = dict(SERVICE_CHOICES)
        enquiry = {
            "name": data["name"],
            "email": data["email"],
            "phone": data["phone"] or "Not provided",
            "service_label": service_labels[data["service"]],
            "message": data["message"],
        }
        try:
            send_enquiry_email(enquiry)
        except Exception:
            logger.exception("Unable to send portfolio enquiry with Resend")
            messages.error(request, "Your enquiry could not be sent right now. Please email Harisankar directly.")
        else:
            messages.success(request, "Thanks — your enquiry has been sent. I’ll get back to you soon.")
            return redirect("portfolio:contact")
    return render(request, "portfolio/contact.html", {"form": form})
