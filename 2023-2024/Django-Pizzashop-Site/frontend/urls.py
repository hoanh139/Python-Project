from django.urls import path
from .page_views.bestellung_view import BestellungView
from .page_views.kundendaten_view import KundendatemView
from .page_views.home_view import HomepageView
from .page_views.speisekarte_view import SpeisekarteView


urlpatterns = [
    path('', HomepageView.as_view(), name='home'),
    path('kundendaten/', KundendatemView.as_view(), name='user-info'),
    path('speisekarte/', SpeisekarteView.as_view(), name='menu'),
    path('bestellung/', BestellungView.as_view(), name='order'),
]