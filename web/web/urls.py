from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from web.views import temp_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # TODO Delete home view, when add Products home view.
    path('', temp_view, name='home'),
    path('users/', include('users.urls',namespace='users'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
