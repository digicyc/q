from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import (authenticate,
                                login as auth_login,
                                logout as auth_logout)

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
        profile = models.UserProfile(kindle_email='', user=user)
        profile.save()
    
    profile = user.get_profile()
    
    if request.method == 'POST':
        form = forms.EditProfileForm(request.POST)
        if form.is_valid():
            if user.first_name != form.cleaned_data['first_name']:
                user.first_name = form.cleaned_data['first_name']
            
            if user.last_name != form.cleaned_data['last_name']:    
                user.last_name = form.cleaned_data['last_name']
            
            if user.email != form.cleaned_data['email']:     
                user.email = form.cleaned_data['email']
            
            if user.username != form.cleaned_data['username']:    
                user.username = form.cleaned_data['username']
            
            if profile.kindle_email != form.cleaned_data['kindle_email']:    
                profile.kindle_email = form.cleaned_data['kindle_email']
                
            user.save()
            profile.save()
            
            return HttpResponseRedirect(reverse("edit_profile", kwargs={'username': user.username}))

    else:
        form = forms.EditProfileForm(initial={'first_name': user.first_name, 
                                              'last_name': user.last_name,
                                              'username': user.username, 
                                              'email':user.email,
                                              'kindle_email':profile.kindle_email,
                                              })
            
    ctx.update({'form':form, 'view_user':user})
    return render_to_response(template_name, RequestContext(request, ctx))

def logout(request):

    auth_logout(request)

    return HttpResponseRedirect(reverse('login'))
