from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Contest, UserContest
from django.contrib import messages

def home(request):
    if request.user.is_authenticated:
        user = request.user.pk
        user_contests = [UC.contest for UC in UserContest.objects.filter(user=user)]
        context = {
        'posts': [C for C in Contest.objects.all().order_by('-date_posted') if not C.is_expired and C not in user_contests]
        }
    else:
        context = {
            'posts': [C for C in Contest.objects.all().order_by('-date_posted') if not C.is_expired]
        }


    if request.method == 'POST':
        user = request.POST.get('user')
        if user != 'None':
            user_object = User.objects.get(pk=user)
            contest = request.POST.get('contest')
            contest_object = Contest.objects.get(pk=contest)
            usercontest = UserContest(user=user_object,contest=contest_object)
            if not UserContest.objects.filter(user=user).filter(contest=contest):
                usercontest.save()
                messages.success(request, 'Contest added to your profile!')
                return redirect('contest-home')
            else:
                messages.info(request, 'Contest is already in your profile')
                return redirect('contest-home')
        else:
            return redirect('login')

    return render(request,'contest/home.html',context)

def about(request):
    return render(request,'contest/about.html',{'title': 'About'})
