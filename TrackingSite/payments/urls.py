from django.urls import path, include, re_path
from django.conf.urls import url
from . import views

# Namespace all url related to 'payments'
app_name = 'payments'

urlpatterns = [
    # /payments/
    path('', views.IndexView.as_view(), name='index'),
    path('family/', views.FamilyList.as_view(), name='family'),
    path('family/<int:pk>', views.FamilyDetail.as_view(), name='family-detail'),
    path('family/add/', views.FamilyCreate.as_view(), name='family-add'),
    path('family/<int:pk>/update', views.FamilyUpdate.as_view(), name='family-update'),
    path('family/<int:pk>/delete', views.FamilyDelete.as_view(), name='family-delete'),
    path('family/<int:pk>/lessons', views.manage_lessons, name='lessons'),
    path('push/', views.push_test, name='push'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('<int:pk>/', views.LessonUpdate.as_view(), name='lesson-update'),      
]