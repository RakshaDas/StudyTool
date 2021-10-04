from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, EditAccountForm, ChangePasswordForm


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registered  successfully!. Login now')
            return redirect('login')
        else:
            messages.error(request, 'Something went wrong!! Please try again')

    else:
        form = RegisterForm()

    context = {
        'title': 'Register',
        'form': form,
    }
    return render(request, 'accounts/register.html', context=context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            email = loginForm.cleaned_data['email']
            password = loginForm.cleaned_data['password']
            user = authenticate(
                request, username=email.split('@')[0], password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request, 'Logged in  successfully!.')
                return redirect('index')
            else:
                messages.error(
                    request, "Account not found!.")
        else:
            messages.error(request, 'Something went wrong!! Please try again')

    else:
        loginForm = LoginForm()

    context = {
        'title': 'Login',
        'loginForm': loginForm,
    }
    return render(request, 'accounts/login.html', context=context)


@login_required
def logoutUser(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("index")


@login_required
def userProfile(request):
    if request.method == 'POST':
        form = EditAccountForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Something went wrong!! Please try again')

    else:
        user = User.objects.get(id=request.user.id)
        formData = {
            'firstName': user.first_name,
            'lastName': user.last_name,
            'email': user.email,
        }
        form = EditAccountForm(initial=formData, user=request.user)

    context = {
        'title': 'Profile',
        'form': form,
    }
    return render(request, 'accounts/profile.html', context=context)


@login_required
def changePassword(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Password changed successfully. Login back.')
            return redirect('index')
        else:
            messages.error(request, 'Something went wrong!! Please try again')

    else:
        form = ChangePasswordForm(user=request.user)

    context = {
        'title': 'Change Password',
        'form': form,
    }
    return render(request, 'accounts/changePass.html', context=context)


@login_required
def deleteAccount(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        messages.success(request, "Account deleted successfully")
        return redirect("index")
    except User.DoesNotExist:
        messages.error(request, "Account not found!")
        return redirect("profile")
    except Exception as e:
        messages.error(request, "Something went wrong!! Please try again")
        return redirect("profile")
