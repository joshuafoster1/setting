# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.urls import resolve
from .views import signup

# Create your tests here.
class SignUpTests(TestCase):
    def test_signup_staus_code(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_signup_url_resolves_sighnup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)
