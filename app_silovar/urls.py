from django.urls import path
from . import views

urlpatterns = [
    path('constructions/', views.construction_list, name='construction-list'),
    path('constructions/create/', views.construction_create, name='construction-create'),
    path('constructions/<int:pk>/update/', views.construction_update, name='construction-update'),
    path('constructions/<int:pk>/delete/', views.construction_delete, name='construction-delete'),
]
