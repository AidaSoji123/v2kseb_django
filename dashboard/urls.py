from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("import_csv/", views.import_csv, name="import_csv"),
]