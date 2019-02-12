from django.conf.urls import url

from frontend import views

urlpatterns = [
    url(r'^$', views.index,name='home'),
    url(r'^cruise-destinations/$', views.destinations,name='destinations'),
    url(r'^cruise-departures/$', views.departures, name='departures'),
    url(r'^cruiselines/$', views.cruises_lines, name='cruise_lines'),
    url(r'^cruise-deals/$', views.cruise_deals, name='cruise_deals'),

    url(r'^cruise-destinations/port/(?P<destination_port>[\w|\W]+)/$', views.cruise_by_destination_port),
    url(r'^cruise-destinations/(?P<type>region|subregion)/(?P<destination>[\w|\W]+)/$', views.cruise_by_destination),
    url(r'^cruise-departures/(?P<departure_port_slug>[\w|\W]+)/$', views.cruise_by_departure_port),
    url(r'^cruise/(?P<cruiseid>[0-9]+)/$', views.cruise),

    url(r'^cruiselines/(?P<cruise_line_slug>[\w|\W]+)/ship/(?P<ship_slug>[\w|\W]+)/$', views.cruise_by_line_ship),
    url(r'^cruiselines/(?P<cruise_line_slug>[\w|\W]+)/subregion/(?P<subregion>[\w|\W]+)/$', views.cruise_by_line_subregion),
    url(r'^cruiselines/(?P<cruise_line_slug>[\w|\W]+)/departure/(?P<departure_port_slug>[\w|\W]+)/$', views.cruise_by_line_departure),
    url(r'^cruiselines/(?P<slug>[\w|\W]+)/$', views.cruise_details),

    url(r'^search/(?:date/(?P<date>[0-9]{4}-[0-9]{2})/){0,1}(?:length/(?P<length>([0-9]{1,2}-[0-9]{1,2})|[0-9]{1,2}\+)/){0,1}(?:destination/(?P<destination>[\w|\W]+)/){0,1}(?:cruiseLine/(?P<cruise_line>[\w|\W]+)/){0,1}(?:ship/(?P<ship>[\w|\W]+)/){0,1}(?:departure-port/(?P<departure_port>[\w|\W]+)/){0,1}$', views.search_cruises, name='search_cruises_name'),

    url(r'^saved-travels', views.get_saved_travels, name='get_saved_travels'),

     url(r'^user/logout/$', views.logout_user,name='logout_user'),
    #----------ajax request------
    # url(r'^all-pricing/$', views.travels_pricing,{'SSL':True}, name='travel_pricing'),
    url(r'^ship-by-cruise/$', views.get_ships_by_cruiseline, name='ship_by_cruise'),
    url(r'^add_subscriber/$', views.subscribe, name='add_subscriber'),
    url(r'^send_email/$', views.send_email,name='send_email'),
    url(r'^login/$', views.authenticateUser,name='authenticateUser'),
    url(r'^create_user/$', views.create_user,name='create_user'),
    url(r'^save-travel/$', views.toggle_save_travel,name='toggle_save_travel'),

]