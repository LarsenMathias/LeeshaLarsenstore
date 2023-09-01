from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class UserprofileModelform(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['name','email','address','city','state','pincode']
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1', 'password2','email']  # You can adjust this

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create UserProfile related to the user
            UserProfile.objects.create(
                user=user,
                email=self.cleaned_data['email'],
                name=self.cleaned_data['name'],
                # ... other fields
            )
        return user
