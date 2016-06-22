#from registration.backends.hmac.views import RegistrationView
#from registration.backends.model_activation.views import RegistrationView
from registration.backends.simple.views import RegistrationView
from registration.forms import RegistrationForm
from editor.forms import UserRegistrationForm
from editor import views 
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('editor.urls')),
    url(r'^editor/', include('editor.urls')),
#    url(r'^accounts/', include('registration.backends.hmac.urls')),
#    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/profile/$', views.dispatch_ad_source, name='dispatch_ad_source'),
    url(r'^accounts/register/$',
        RegistrationView.as_view(
            form_class = UserRegistrationForm
        ),
        name='registration_register',
    ),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', admin.site.urls),
]
