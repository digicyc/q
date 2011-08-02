from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.views import password_change
from django.contrib.auth import (authenticate,
                                login as auth_login,
                                logout as auth_logout)
from django.contrib.auth.forms import PasswordChangeForm

from q.common import reverse_lazy

from accounts import forms, models
from ebooks.models import CheckOut, Ownership

from activity_stream.models import create_activity_item

@user_passes_test(lambda u: u.is_staff, reverse_lazy('admin_required'))
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

@login_required
def edit_password(request, template_name="accounts/edit_password.html",  *args, **kwargs):
    ctx = {}
    
    user = request.user
    username = user.username
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            if not user.check_password(request.POST['old_password']):
                messages.error(request, "Wrong password. Password not changed.")
            elif request.POST['new_password1'] != request.POST['new_password2']:
                messages.error(request, "Passwords do not match. Password not changed.")
            else:
                user.set_password(request.POST['new_password1'])
                user.save()
                messages.success(request,"Password changed!")
    else:
        form = PasswordChangeForm(user)

    print form
    ctx.update({'form':form})
    return render_to_response(template_name, RequestContext(request, ctx))

def edit_profile(request, template_name="accounts/edit_profile.html",*args, **kwargs):
    ctx ={}
    
    
    user = request.user
    
    username = user.username
    
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
                
        # SHOULD REMOVE THIS LOGIC.      
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
    
#INVITATION STUFF
@login_required
def manage_invitations(request, template_name="accounts/manage_invites.html",  *args, **kwargs):
	ctx = {}
	invitation = ""
	
	# get the user.
	user = request.user
	profile = user.get_profile()
	
	# get remaining invites.
	remaining_invitations = profile.available_invites
	
	# form setup
	form = forms.InvitationKeyForm()
	
	# get all users for invite distribution
	users = User.objects.all()
	invite_distribution_form = forms.InvitationDistributionForm(users=users)
	
	if request.method == "POST":
		if 'distribute' in request.POST['submit'].lower():
			invite_distribution_form = forms.InvitationDistributionForm(request.POST, users=users)
			if invite_distribution_form.is_valid():
				distribute_to = User.objects.get(id=invite_distribution_form.cleaned_data["to_who"])
				distribute_to_profile = distribute_to.get_profile()
				
				distribute_to_profile.available_invites += invite_distribution_form.cleaned_data["number_of_invites"]
				distribute_to_profile.save()
	
		else:
			form = forms.InvitationKeyForm(request.POST)
			if remaining_invitations > 0 and form.is_valid():
				# create & deliver invitation.
				invitation = models.InvitationKey.objects.create_invitation(request.user)
				invitation.send_to(form.cleaned_data["email"])
				
				#remove invite by 1
				profile.available_invites = remaining_invitations - 1
				profile.save()

	
	# get sent invitations
	invitations = models.InvitationKey.objects.filter(from_user=user)
	
	ctx.update({'form':form, 'invite_distribution_form': invite_distribution_form, 
				'users':users, 'invitation':invitation, 'invitations':invitations})
	return render_to_response(template_name, RequestContext(request, ctx))


def signup(request, template_name="accounts/signup.html",  *args, **kwargs):
	ctx = {}
	
	#IS SITE IN INVITE MODE?
	if not settings.INVITE_MODE:
		return HttpResponseRedirect(reverse('index'))
	
	invitation_key = request.session.get('invitation_key')
	invitation_key = get_object_or_404(models.InvitationKey, key=invitation_key)
		
		
		
	if not invitation_key.is_usable():
		return HttpResponseRedirect(reverse('index'))
	else:
		if request.method == "POST":
			form = forms.RegistrationForm(request.POST)
			if form.is_valid():
				
				user = User()
				profile = models.UserProfile()
				
				split_name = form.cleaned_data['name'].split(" ")
			
				if len(split_name) == 2:
					user.first_name = split_name[0]
					user.last_name = split_name[1]
				else:
					user.first_name = form.cleaned_data['name']
					user.last_name = ""
					
				user.username = form.cleaned_data['username']
				user.email = form.cleaned_data['email']
				user.set_password(form.cleaned_data['password'])
				 
				user.save()
				
				#setup profile.
				profile.user = user
				profile.kindle_email = form.cleaned_data['kindle_email']
				profile.save()
				
				#if in invite mode. mark invite used.
				if getattr(settings, 'INVITE_MODE', True):				
					# disable invite.
					invitation_key.mark_used(user)
					
					from_user = invitation_key.from_user
					from_user_profile = from_user.get_profile()
					from_user_profile.available_invites = from_user_profile.available_invites - 1
					from_user_profile.save()
					
					del request.session['invitation_key']
					
					create_activity_item('invited', request.user, invitation_key)
				
				#redirect
				return HttpResponseRedirect(reverse('login'))
		else:
			form = forms.RegistrationForm()
		
		ctx.update({'form':form})
	
	
	
	#push out to page
	return render_to_response(template_name, RequestContext(request, ctx))

def invited(request, template_name="accounts/invited.html",  *args, **kwargs):
	ctx = {}
	if getattr(settings, 'INVITE_MODE', True):	
		#get invite key and check if valid.
		invitation_key =  kwargs.get('invitation_key')
		is_key_valid = models.InvitationKey.objects.is_key_valid(invitation_key)
	
		#set session cookie to allow registering
		request.session['invitation_key'] = invitation_key
	
		#boot if not valid.
		if not is_key_valid:
			return HttpResponseRedirect(reverse('index'))
		return render_to_response(template_name, RequestContext(request, ctx))
	return HttpResponseRedirect(reverse('index'))

