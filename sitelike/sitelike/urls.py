from django.conf import settings
from django.urls import path
from django.contrib import admin
from directory.views import DirectoryListView, DirectoryDetailView, DirectoryCreateView, DirectoryUpdateView, DirectoryDeleteView, TopDirectoryListView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('websites/', DirectoryListView.as_view(), name='website-list'),
    path('websites/rank-wise-list/', TopDirectoryListView.as_view(), name='top-website-list'),
    path('websites/latest-list/', DirectoryListView.as_view(), name='latest-website-list'),
    path('websites/<int:pk>/', DirectoryDetailView.as_view(), name='website-detail'),
    path('websites/create/', DirectoryCreateView.as_view(), name='website-create'),
    path('websites/<int:pk>/update/', DirectoryUpdateView.as_view(), name='website-update'),
    path('websites/<int:pk>/delete/', DirectoryDeleteView.as_view(), name='website-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)