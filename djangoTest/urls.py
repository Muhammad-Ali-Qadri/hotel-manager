"""djangoTest URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

import polls.views

admin.autodiscover()

urlpatterns = [
    url('^admin/', admin.site.urls, name="Admin"),
    url('^index/', polls.views.index, "index"),
    url('^facilities/', polls.views.facilities, name="facilities"),
    url('^restaurant/', polls.views.restaurant, name="restaurant"),
    url('^review/', polls.views.review, name="review"),
    url('^login/', polls.views.my_login, name="login"),
    url('^signup/', polls.views.signup, name="signup"),
    url('^profile/', polls.views.profile, name="profile"),
    url('^logout/', polls.views.my_logout, name="logout"),
    url('^booking/', polls.views.booking, name="booking"),
    url('^check/', polls.views.check, name="check"),
    url('', polls.views.index, name="index"),
]
