from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from core.forms import LoginForm

urlpatterns = [
    url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name="login"),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(next_page='/'), name="logout"),
    url('^accounts/', include('django.contrib.auth.urls')),
    #url(r'^login/$', auth_views.LoginView.as_view()),
    #url(r'^login$', auth_views.login, {'template_name': 'login.html', 'authentication_form': LoginForm},name='login'), # Deprecated Django 11.1
]