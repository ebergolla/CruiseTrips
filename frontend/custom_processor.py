__author__ = 'ernesto'

from backend.models import Port, CruiseLine, SubRegion, Ship, TravelDates
from datetime import datetime
from django.core.cache import cache

def filter(request):
    subregions = cache.get('subregions')
    if subregions is None:
        subregions = SubRegion.objects.get_subregions_active()
        cache.set('subregions', subregions)

    subregions_data = []
    for sr in subregions:
        temp = {'id': sr.id, 'name': sr.alias}
        temp['selected'] = False

        if request.GET.has_key('destination') and sr.name == request.GET['destination']:
            temp['selected'] = True
        subregions_data.append(temp)

    cruises_lines = cache.get('cruises_lines')
    if cruises_lines is None:
        cruises_lines = CruiseLine.objects.all()
        cache.set('cruises_lines', cruises_lines)

    cruises_lines_data = []
    for cl in cruises_lines:
        temp = {'id': cl.id, 'name': cl.name}
        temp['selected'] = False

        if request.GET.has_key('cruiseLine') and cl.name == request.GET['cruiseLine']:
            temp['selected'] = True
        cruises_lines_data.append(temp)

    ship_data = []
    if request.GET.has_key('cruiseLine'):
        cruise_line_name = request.GET['cruiseLine']
        cruise_line_query = CruiseLine.objects.get(name= cruise_line_name)

        ship_query = Ship.objects.filter(cruise_line_id = cruise_line_query.id)

        for s in ship_query:
            temp = {'id': s.id, 'name': s.name}
            temp['selected'] = False
            if request.GET.has_key('ship') and s.name == request.GET['ship']:
                temp['selected'] = True
            ship_data.append(temp);

    departure_port = Port.objects.get_departure_port()


    departure_port_data = []
    for dp in departure_port:
        #if dp.traveldates_set.filter(traveldatesport__day_number = 1).count() != 0:
            name = dp.name
            if dp.country_id != None:
                name += ', ' + dp.country.name
            temp = {'id': dp.id, 'name': name, 'slug': dp.slug}
            temp['selected'] = False

            if request.GET.has_key('departure') and dp.slug == request.GET['departure']:
                temp['selected'] = True
            departure_port_data.append(temp)

    filter_length = TravelDates.objects.order_by("nights").values("nights").distinct()

    filter_length_data = []
    for fl in filter_length:
        temp = {'length_value': fl['nights'], }
        temp['selected'] = False

        if request.GET.has_key('length') and str(fl['nights']) == request.GET['length']:
            temp['selected'] = True
        filter_length_data.append(temp)
    date = None
    if request.GET.has_key('date'):
        date = request.GET['date']

    filter_data = {'date': date, 'departure_port': departure_port_data, 'ships': ship_data,
            'cruises_lines': cruises_lines_data, 'subregions': subregions_data, 'filter_length': filter_length_data}

    return {'filter_data' : filter_data}