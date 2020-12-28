from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserRegisterForm, ProfileForm, UserUpdateForm

from contest.models import UserContest, Contest
from django.db import models
from django.contrib import messages
from django.utils import timezone

def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            p_form = p_form.save(commit=False)
            p_form.user = user
            p_form.save()
            #username = u_form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now log in')
            return redirect('login')
    else:
        u_form = UserRegisterForm()
        p_form = ProfileForm()
    return render(request,'users/register.html',{'u_form':u_form,'p_form':p_form})



@login_required
def mycontests(request):
    user = request.user.pk

    context = {

        'user_contests': [UC for UC in UserContest.objects.filter(user=user).order_by('-time_added') if not UC.contest.is_expired and UC.enter_available],
        'entered': [UC for UC in UserContest.objects.filter(user=user).order_by('-last_entered') if not UC.contest.is_expired and not UC.enter_available],
        'expired': [UC for UC in UserContest.objects.filter(user=user).order_by('-contest__end_date') if UC.contest.is_expired],

    }
    if request.method == 'POST':
        user = request.POST.get('user')
        if user != 'None':
            user_object = User.objects.get(pk=user)
            usercontest = request.POST.get('usercontest')
            user_contest_object = UserContest.objects.get(pk=usercontest)
            if user_contest_object.enter_available:
                user_contest_object.entries += 1
                user_contest_object.last_entered = timezone.now()
                user_contest_object.save()
                messages.success(request, 'Entered!')
                context['user_contests'] = [UC for UC in UserContest.objects.filter(user=user) if not UC.contest.is_expired and UC.enter_available]
                context['entered'] = [UC for UC in UserContest.objects.filter(user=user) if not UC.contest.is_expired and not UC.enter_available]
                return redirect('mycontests')
            else:
                messages.info(request, 'Already entered')


        else:
            return redirect('login')

    return render(request,'users/mycontests.html',context)

@login_required
def profile(request):
    user_profile = Profile.objects.get(user__id=request.user.id)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileForm(request.POST,instance=user_profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=user_profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)