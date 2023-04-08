from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import about_view
from .views import contact_view
from .views import login_view
from .views import logout_view
from .views import registration_view
from .views import get_dealerships
from .views import get_dealer_details
from .views import add_review



app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

  
    # path for about view

    path('about.html', about_view, name='about'),

    # path for contact us view

    path('contact_us.html', contact_view, name='contact'),

    # path for registration

    path('registration', registration_view, name='registration'),

    # path for login

    path('login', login_view, name='login'),

    # path for logout

    path('logout', logout_view, name='logout'),

    # path for dealerships

    path('', get_dealerships, name='index'),

    # path for dealer reviews view

    path('dealer/<int:dealer_id>', get_dealer_details, name="dealer_details"),

    # path for add a review view

    path('dealer/add_review/<int:dealer_id>', add_review, name="add_review"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)