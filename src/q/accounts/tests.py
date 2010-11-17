from datetime import datetime 
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from django.contrib.auth.models import User

from q.accounts import models

class AccountsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # create user.
        user = User.objects.create_user('zholmquist', 'zholmquist@gmail.com', 'kinderhook')
        user.save()
        
        try:
            profile = view_user.get_profile()
        except:
            profile = models.UserProfile(kindle_email='', user=user)
            profile.save()
    
    def test_edit_profile(self):  
        #login 
        self.client.login(username='zholmquist', password='kinderhook')   
        
        #hit /users/zholmquist/edit
        response = self.client.get(reverse("edit_profile", kwargs={'username': 'zholmquist'}))
        self.assertEqual(response.status_code, 200)
        
    def test_edit_profile(self):
        response = self.client.post(reverse("edit_profile", kwargs={'username': 'zholmquist'}), 
                            {'first_name': 'Zachary', 'last_name': "Mehquist", 'email':'zach@bleh.com',
                                'username':'zach', 'kindle_email':'zach@neutroninteractive.com'})
        
        #get new username.                    
        user = User.objects.get(username='zach')
        profile = user.get_profile()
        
        #check if update worked.
        self.assertEqual(user.first_name, 'Zachary')
        self.assertEqual(user.last_name, 'Mehquist')
        self.assertEqual(user.email, 'zach@bleh.com')
        self.assertEqual(user.username, 'zach')
        self.assertEqual(profile.kindle_email, 'zach@neutroninteractive.com')