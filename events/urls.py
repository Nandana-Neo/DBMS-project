from django.urls import path
from . import views


urlpatterns = [
    path('', views.EventListView.as_view(), name='event-list'),
    path('event/<int:pk>/',views.EventDetailView.as_view(),name='event-detail'),
    path('event/<int:pk>/update',views.EventUpdateView.as_view(),name='event-update'),
    path('event/<int:pk>/delete',views.EventDeleteView.as_view(),name='event-delete'),
    path('event/<int:pk>/register/', views.register_for_event, name='event-register'),
    path('post/new/',views.EventCreateView.as_view(),name='event-create'),
    path('event/<int:pk>/attendance',views.MarkAttendanceView.as_view(),name='attendance'),
    path('event/org/<str:username>',views.EventUserListView.as_view(),name='event-userlist'),
    path('event/reg/<str:username>',views.EventRegListView.as_view(),name='event-reglist'),
    path('search/event/', views.event_search, name='event_search'),
    path('user/<str:username>',views.UserEventView, name='user-events'),
    path('api/posts/',views.event_date_list,name='event-date-list'),
    path('calendar/<str:date>/', views.get_events_by_date.as_view(), name='get_events_by_date'),
    # path('create/', views.event_create, name='event-create'),
    # path('<int:event_id>/', views.event_detail, name='event-detail')
    
]
