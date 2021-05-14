from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'home_app'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home_app:login'), name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),

    path('', views.Tasklist.as_view(), name='tasks'),
    path('detail/<int:pk>/', views.DetailTask.as_view(), name='detail'),
    path('task-create/', views.TaskCreate.as_view(), name='create'),
    path('task-update/<int:pk>/', views.TaskUpdate.as_view(), name='update'),
    path('task-delete/<int:pk>/', views.DeleteTask.as_view(), name='delete'),
]
