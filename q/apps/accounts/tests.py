from datetime import datetime 
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from django.contrib.auth.models import User

from accounts import models

class AccountsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # create user.
        user = User.objects.create_user('zholmquist', 'zholmquist@gmail.com', 'kinderhook')
        user.save()
        
        user2 = User.objects.create_user('com4', 'pinkponies@gmail.com', 'kinderhook')
        user2.save()
    
    def test_edit_profile(self):  
        #login 
        self.client.login(username='zholmquist', password='kinderhook')   
        
        #hit /users/zholmquist/edit
        response = self.client.get(reverse("edit_profile", kwargs={'username': 'zholmquist'}))
        self.assertEqual(response.status_code, 200)
        
    def test_can_only_edit_personal_account(self):
        #login as zholmquist
        self.client.login(username='zholmquist', password='kinderhook')  
        
        #get to jasons edit_profile ( should redirect )
        response = self.client.get( reverse("edit_profile", kwargs={'username': 'com4'}) )
        self.assertRedirects(response, reverse("view_user", kwargs={'username': 'com4'}))
        
        #get my own edit_profile ( should load )
        response = self.client.get( reverse("edit_profile", kwargs={'username': 'zholmquist'}) )
        self.assertEqual(response.status_code, 200)
        
    def test_edit_profile(self):
        self.client.login(username='zholmquist', password='kinderhook')  
    
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
        
        