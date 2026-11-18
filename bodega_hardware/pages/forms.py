from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "phone", "message")
        labels = {"email": "Email Address", "phone": "Phone Number (optional)"}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter your email address"}),
            "phone": forms.TextInput(attrs={"placeholder": "Enter your phone number"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "Your message"}),
        }
