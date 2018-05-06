from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from core.forms import LoginForm
from rest_framework_docs.views import DRFDocsView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name="login"),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(next_page='/'), name="logout"),
    url('^accounts/', include('django.contrib.auth.urls')),
    url('^$', login_required(DRFDocsView.as_view(), login_url="/api-auth/login/"), name="drfdocs"),
]
