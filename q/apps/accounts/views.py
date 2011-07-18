from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import (authenticate,
                                login as auth_login,
                                logout as auth_logout)
from django.contrib.auth.forms import PasswordChangeForm

from accounts import forms, models
from ebooks.models import CheckOut, Ownership

def view_user_list(request, template_name="accounts/users_list.html"):
    ctx = {}

    users = User.objects.all()

    ctx.update({'users': users})
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
def view_user(request, template_name="accounts/dashboard.html",  *args, **kwargs):
    ctx = {}

    can_edit = False
    username = kwargs.get('username').lower()
    view_user = get_object_or_404(User,username=username)
    
    if username == request.user.username:
        can_edit = True
        
    current_checkouts = CheckOut.objects.filter(user=view_user).filter(check_in_time=None)
    checkout_history = CheckOut.objects.filter(user=view_user).order_by('-create_time')[:10]
    books_owned = Ownership.objects.filter(user=view_user)

    ctx.update({'view_user': view_user,
                'can_edit':can_edit,
                'current_checkouts':current_checkouts,
                'checkout_history':checkout_history,
                'books_owned': books_owned,
                })
    return render_to_response(template_name, RequestContext(request, ctx))

def login(request, template_name="accounts/login.html"):
    ctx = {}
    messages = []
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            try:
                given_username = form.cleaned_data['username']
                given_password = form.cleaned_data['password']
                user = User.objects.get(username=given_username)
                user = authenticate(username=user.username,
                                    password=given_password)

                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        if request.GET.has_key('next'):
                            return HttpResponseRedirect(request.GET['next'])
                        return HttpResponseRedirect(reverse('index'))
                    else:
                        messages.append("Your account is currently deactivated.")
                else:
                    messages.append("Invalid account.")

            except User.DoesNotExist:
                pass
    else:
        form = forms.LoginForm()

    ctx.update({'form':form, 'messages':messages})
    return render_to_response(template_name, RequestContext(request, ctx))


def edit_profile(request, template_name="accounts/edit_profile.html",*args, **kwargs):
    ctx ={}
    
    username = kwargs.get('username').lower()
    
    if username != request.user.username:
        return HttpResponseRedirect(reverse("view_user", kwargs={'username': username}))
        
    user = get_object_or_404(User, username=username)
    
    
    #create profile if needed
    try:
        profile = user.get_profile()
    except:
        profile = models.UserProfile(user=user)
        profile.save()
        
    profile_form = forms.EditProfileForm(initial={'first_name': user.first_name,
                                      'last_name': user.last_name,
                                      'username': user.username,
                                      'email':user.email,
                                      'kindle_email':profile.kindle_email,
                                      })

    password_form = PasswordChangeForm(user)

    if request.method == 'POST':
        if "profile" in request.POST['submit'].lower():
            profile_form = forms.EditProfileForm(request.POST)
            if profile_form.is_valid():
                user.first_name = profile_form.cleaned_data['first_name']
                user.last_name = profile_form.cleaned_data['last_name']
                user.email = profile_form.cleaned_data['email']
                #user.username = profile_form.cleaned_data['username']
                profile.kindle_email = profile_form.cleaned_data['kindle_email']

                user.save()
                profile.save()

                messages.success(request, "Profile saved!")
        elif "password" in request.POST['submit'].lower():
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                if not user.check_password(request.POST['old_password']):
                    messages.error(request, "Wrong password. Password not changed.")
                elif request.POST['new_password1'] != request.POST['new_password2']:
                    messages.error(request, "Passwords do not match. Password not changed.")
                else:
                    user.set_password(request.POST['new_password1'])
                    user.save()
                    messages.success(request,"Password changed!")

    ctx.update({'profile_form':profile_form, 'view_user':user, 'password_form':password_form})
    return render_to_response(template_name, RequestContext(request, ctx))

def logout(request):

    auth_logout(request)

    return HttpResponseRedirect(reverse('login'))
