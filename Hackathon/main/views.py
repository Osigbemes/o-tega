from django.shortcuts import render, redirect
from .forms import UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.contrib import messages


# Create your views here.
def register(response):
	if response.method == "POST":
		form = RegisterForm(response.POST)
		if form.is_valid():
			form.save()
			messages.success(response, f'Your account has been created! You are now able to login')

		return redirect("/login")
	else:
		form = RegisterForm()

	return render(response, "main/register.html", {"form":form})

def home(response):
	return render(response, "main/home.html", {})

@login_required
def profile(request):
	if request.method == "POST":
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context={
		'u_form':u_form,
		'p_form':p_form
	}
	return render(request, 'main/profile.html', context)

