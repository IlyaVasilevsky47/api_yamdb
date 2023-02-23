from django.shortcuts import render
from .models import ReviewUser
# from django.urls import reverse_lazy
# from django.views.generic.edit import CreateView

# from .forms import CustomUserCreationForm

def profile(request):
    users = ReviewUser.objects.all()
    return render(request, 'users/profile.html', {'users': users})

# class SignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'