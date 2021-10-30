from django.urls import path, include
from django.conf.urls import url
from .views import *

app_name = 'olive_grove'

urlpatterns = [
    path('', OliveGroveListView.as_view(), name='olive_groves'),
    path('new', OliveGroveCreateView.as_view(), name='olive_grove_create'),
    path('view/<int:pk>/', OliveGroveDetailView.as_view(), name='olive_grove_detail'),
    path('edit/<int:pk>/', OliveGroveUpdateView.as_view(), name='olive_grove_update'),
    path('delete/<int:pk>/', OliveGroveDeleteView.as_view(), name='olive_grove_delete'),
    path('view/<int:pk>/notes/new', NoteCreateView.as_view(), name='note_create'),
    path('view/<int:og_id>/notes/view/<int:pk>', NoteDetailView.as_view(), name='note_detail'),
    path('view/<int:og_id>/notes/edit/<int:pk>', NoteUpdateView.as_view(), name='note_update'),
    path('view/<int:og_id>/notes/delete/<int:pk>', NoteDeleteView.as_view(), name='note_delete'),

]