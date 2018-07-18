# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

content = {'test':'test'}
# Create your views here.
def home(request):
    """
    Place to veiw/access prior safety checks, see when last was done and diplay
    prominantly when the next one is due. Allow button to start safety check 1
    week prior to new safety check date. Upon button press create new safety check
    instance, populate anchor safety_check for averyanchor in the gym into a table.
    Click on an anchor and go to page for draws on that anchor, you can add a draw,
    or modify an existing draw.
    """

    return render(request, 'SC_home.html', content)

def current_check(request):

    return render(request, 'SC_home.html', content)
    
