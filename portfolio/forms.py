from django import forms


SERVICE_CHOICES = [
    ("web_app", "Web app development"),
    ("frontend", "Front-end development"),
    ("full_stack", "Full-stack development"),
    ("website", "Website design and development"),
    ("seo", "SEO"),
    ("video_production", "Video production"),
    ("video_editing", "Video editing and post-production"),
    ("ui_ux", "UI / UX design and development"),
    ("data_analysis", "Data analysis"),
    ("graphic_design", "Graphic design"),
    ("photo_editing", "Photo editing"),
    ("wedding_video", "Wedding video editing"),
    ("other", "Other / general enquiry"),
]


class EnquiryForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"autocomplete": "name", "placeholder": "Name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "you@example.com"}))
    phone = forms.CharField(required=False, max_length=30, widget=forms.TelInput(attrs={"autocomplete": "tel", "placeholder": "+91"}))
    service = forms.ChoiceField(choices=[("", "Select a service"), *SERVICE_CHOICES])
    message = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={"rows": 5, "placeholder": "What are you working on? A few details are a great start."}))

    # Honeypot field: normal visitors never see or fill it.
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}))
