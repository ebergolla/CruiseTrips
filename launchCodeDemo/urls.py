from django.conf.urls import include, url
from django.contrib import admin
from frontend.urls import urlpatterns as frontend_urls
import settings
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'launchCodeDemo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(frontend_urls)),
    #url(r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
