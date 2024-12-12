from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("import_csv/", views.import_csv, name="import_csv"),
    path('get-sections/<int:division_id>/', views.get_sections, name='get_sections'),
]
