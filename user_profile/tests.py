from django.test import TestCase,Client
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from user_profile.models import UserProfile


class Test_user_profile_views(TestCase):
    def setUp(self):
        self.data = {
                     'username':'admin',
                     'email':'admin@gmail.com',
                     'password':'admin123456',
                    }
        self.user = User.objects.create_user(**self.data)
        self.profile = UserProfile.objects.get(user=self.user)
        self.client = Client()
        self.profile_detail_url = reverse_lazy(
            'profile',args=(self.profile.id,)
        )
        self.update_profile_url = reverse_lazy(
            'update-profile',args=(self.profile.id,)
        )
        
    def test_profile_detail_if_redirect_for_unauth_user(self):
        resp = self.client.get(self.profile_detail_url)
        #test if unauth user is redirected 
        self.assertEqual(resp.status_code,302)
    def test_profile_detail_if_ok_for_auth_user(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.profile_detail_url)
        self.assertEqual(resp.status_code,200)
        # test if right template used
        self.assertTemplateUsed(resp,'user_profile/userprofile_detail.html')
        self.assertContains(resp,self.profile)
    def test_update_profile_for_unauth_user(self):
        resp = self.client.get(self.update_profile_url)
        #check if unauthorized user is redirected
        self.assertEqual(resp.status_code,302)
    def test_update_profile_for_auth_and_owner_of_profile(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.update_profile_url)
        #test if profile owner pass the redirect and forbidden 
        self.assertEqual(resp.status_code,200)
    def test_update_profile_for_auth_but_not_owner_of_profile(self):
        tuser = User.objects.create_user(
            username='test',email='test@gmail.com',
            password='test123456'
        )
        self.client.force_login(tuser)
        resp = self.client.get(self.update_profile_url)
        #test if non owner of profile get forbidden response in update profile page
        self.assertEqual(resp.status_code,403)
        del tuser
    def test_update_profile_by_updating_profile_model_by_post_request(self):
        self.client.force_login(self.user)
        data = {"name":"Hailse"}
        resp = self.client.post(path=self.update_profile_url,data=data)
        profile = UserProfile.objects.get(user=self.user)
        #test if profile is updated by right data
        self.assertEqual(profile.name,data['name'])
        #test if redirect after update 
        self.assertEqual(resp.status_code,302)
    def tearDown(self):
        del self.user
        del self.profile
        del self.client
        
class Test_user_profile_models(TestCase):
    def setUp(self):
        self.data = {
                     'username':'admin',
                     'email':'admin@gmail.com',
                     'password':'admin123456',
                }
        self.user = User.objects.create_user(self.data)
    def test_signal_create_userprofile_when_user_created(self):
        exist = UserProfile.objects.filter(user=self.user).exists()
        self.assertTrue(exist)
    def test_str_method_of_userprofile_model(self):
        profile = UserProfile.objects.get(user=self.user)
        #test if profile have str method that return profile name
        self.assertEqual(str(profile),profile.name)
    def tearDown(self):
        del self.user