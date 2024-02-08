from django.urls import path
from .views import SiteCreateView, CollectorListView, ContactListView

urlpatterns = [
    path('collectors/', CollectorListView.as_view(), name='collectors-list'),
    path('create-site/', SiteCreateView.as_view(), name='create-site'),
    path('contacts/', ContactListView.as_view(), name='contacts-list')
]