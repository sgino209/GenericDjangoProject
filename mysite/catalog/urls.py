# (c) Shahar Gino, July-2018, sgino209@gmail.com
#
# Catalog URLs

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('books/', views.BookListView.as_view(), name='books'),
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),

    path('signup', views.signup, name='signup'),
    path('account_activation_sent', views.account_activation_sent, name='account_activation_sent'),
    path('activate/[0-9A-Za-z_\-]+)/[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
]