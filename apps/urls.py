from django.urls import include, path

urlpatterns = [
    path('auth/', include('apps.authentication.urls')),
    path('books/', include('apps.books.urls')),
    path('users/', include('apps.users.urls')),
]
