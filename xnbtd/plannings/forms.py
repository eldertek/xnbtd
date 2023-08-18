from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Rest


class RestAdminForm(forms.ModelForm):
    class Meta:
        model = Rest
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RestAdminForm, self).__init__(*args, **kwargs)
        self.initial_status = self.instance.status

    def clean(self):
        cleaned_data = super().clean()

        if 'status' in cleaned_data:
            # Check if status has been changed and the user is not a superuser
            if 'status' in self.changed_data and not self.current_user.is_superuser:
                raise ValidationError(_('Only admin users can change the status.'))

        return cleaned_data
