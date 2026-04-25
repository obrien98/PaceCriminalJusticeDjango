from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Your name", "autocomplete": "name"}
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
