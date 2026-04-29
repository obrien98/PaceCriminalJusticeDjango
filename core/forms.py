from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["first_name", "last_name", "email", "subject", "message"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": "First name", "autocomplete": "given-name"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Last name", "autocomplete": "family-name"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "you@pace.edu", "autocomplete": "email"}
            ),
            "subject": forms.TextInput(
                attrs={"placeholder": "What would you like to ask about?"}
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Write your message here.",
                    "rows": 6,
                }
            ),
        }
