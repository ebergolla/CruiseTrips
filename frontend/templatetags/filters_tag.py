import calendar
from django.http.request import QueryDict
from django.http.response import Http404
from backend.models import Port, CruiseLine, SubRegion, TravelDates, Travel,  Ship
from django import template
from django.db.models import QuerySet
from datetime import datetime
from frontend.models import BannerImage

__author__ = 'ernesto'


register = template.Library()

@register.inclusion_tag('frontend/_filters.html', takes_context=True)
def filters(context):
    return context['filter_data']

@register.inclusion_tag('frontend/_sorts.html')
def sort_by(request, type = 'desktop'):
    url = request.META['PATH_INFO']
    sort = request.GET.get('sort', 'date_asc')
    get = request.GET.copy()
    if request.GET.has_key('sort'):
        get.__delitem__('sort')

    data = {}

    sort_arr = sort.split('_')

    if len(sort_arr) == 2 and (sort_arr[1] == 'desc' or sort_arr[1] == 'asc'):
        data['sort'] = sort_arr[0]
        data['direction'] = sort_arr[1]
    else:
        raise Http404

    get_url = get.copy()
    if get_url.has_key('page'):
        get_url.__delitem__('page')
    date_get = get_url.copy()
    cruiseLine_get = get_url.copy()
    length_get = get_url.copy()
    ship_get = get_url.copy()
    departure_get = get_url.copy()
    price_inside_get = get_url.copy()
    price_oceanview_get = get_url.copy()
    price_balcony_get = get_url.copy()
    price_suite_get = get_url.copy()

    if data['direction'] == 'asc' and data['sort'] == 'price.inside':
        price_inside_get.appendlist('sort', 'price.inside_desc')
        data['price_inside_url'] = price_inside_get.urlencode()
    else:
        price_inside_get.appendlist('sort', 'price.inside_asc')
        data['price_inside_url'] = price_inside_get.urlencode()

    if data['direction'] == 'asc' and data['sort'] == 'price.oceanview':
        price_oceanview_get.appendlist('sort', 'price.oceanview_desc')
        data['price_oceanview_url'] = price_oceanview_get.urlencode()
    else:
        price_oceanview_get.appendlist('sort', 'price.oceanview_asc')
        data['price_oceanview_url'] = price_oceanview_get.urlencode()

    if data['direction'] == 'asc' and data['sort'] == 'price.balcony':
        price_balcony_get.appendlist('sort', 'price.balcony_desc')
        data['price_balcony_url'] = price_balcony_get.urlencode()
    else:
        price_balcony_get.appendlist('sort', 'price.balcony_asc')
        data['price_balcony_url'] = price_balcony_get.urlencode()

    if data['direction'] == 'asc' and data['sort'] == 'price.suite':
        price_suite_get.appendlist('sort', 'price.suite_desc')
        data['price_suite_url'] = price_suite_get.urlencode()
    else:
        price_suite_get.appendlist('sort', 'price.suite_asc')
        data['price_suite_url'] = price_suite_get.urlencode()


    if data['direction'] == 'desc' and data['sort'] == 'date':
        date_get.appendlist('sort', 'date_asc')
        data['date_url'] = date_get.urlencode()
    elif data['sort'] == 'date':
        date_get.appendlist('sort', 'date_desc')
        data['date_url'] = date_get.urlencode()
    else:
        date_get.appendlist('sort', 'date_asc')
        data['date_url'] = date_get.urlencode()

    if data['direction'] == 'desc' and data['sort'] == 'cruiseLine':
        cruiseLine_get.appendlist('sort', 'cruiseLine_asc')
        data['cruiseLine_url'] = cruiseLine_get.urlencode()
    elif data['sort'] == 'cruiseLine':
        cruiseLine_get.appendlist('sort', 'cruiseLine_desc')
        data['cruiseLine_url'] = cruiseLine_get.urlencode()
    else:
        cruiseLine_get.appendlist('sort', 'cruiseLine_asc')
        data['cruiseLine_url'] = cruiseLine_get.urlencode()

    if data['direction'] == 'desc' and data['sort'] == 'length':
        length_get.appendlist('sort', 'length_asc')
        data['length_url'] = length_get.urlencode()
    elif data['sort'] == 'length':
        length_get.appendlist('sort', 'length_desc')
        data['length_url'] = length_get.urlencode()
    else:
        length_get.appendlist('sort', 'length_asc')
        data['length_url'] = length_get.urlencode()

    if data['direction'] == 'desc' and data['sort'] == 'ship':
        ship_get.appendlist('sort', 'ship_asc')
        data['ship_url'] = ship_get.urlencode()
    elif data['sort'] == 'ship':
        ship_get.appendlist('sort', 'ship_desc')
        data['ship_url'] = ship_get.urlencode()
    else:
        ship_get.appendlist('sort', 'ship_asc')
        data['ship_url'] = ship_get.urlencode()

    if data['direction'] == 'desc' and data['sort'] == 'departure':
        departure_get.appendlist('sort', 'departure_asc')
        data['departure_url'] = departure_get.urlencode()
    elif data['sort'] == 'departure':
        departure_get.appendlist('sort', 'departure_desc')
        data['departure_url'] = departure_get.urlencode()
    else:
        departure_get.appendlist('sort', 'departure_asc')
        data['departure_url'] = departure_get.urlencode()

    data['type'] = type
    return data

@register.filter(name='price')
def price_filter(value):
    if value == None or value == '':
        value = 'Call for Pricing'
    else:
        value = '$' + str(value)
    return value

@register.filter(name='pricemobile')
def price_filter_mobile(value):
    if value == None or value == '':
        value = 'Call'
    else:
        value = '$' + str(value)
    return value

@register.inclusion_tag('frontend/_banner.html')
def main_banner():
    banners = BannerImage.objects.order_by('order')
    return {'banners': banners}