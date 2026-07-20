from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib import messages
# Create your views here.

@login_required
def dashboard(request):
    return render(
        request,
        'accounts/dashboard.html',
        {
            'section':'dashboard'
        }
    )


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit = False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            messages.success(request, "Registered Successfully")
            return render(
                request,'accounts/register_done.html',{
                    'new_user' : new_user
                }
            )
        
    else:
        user_form = UserRegistrationForm()

    return render(
        request,
        'accounts/register.html',{
            'user_form' : user_form
        }
    )