from django.http.response import Http404
from django.template.loader import render_to_string
from pure_pagination.paginator import Paginator, Page
from backend.models import TravelDates, TravelDatesPort, Travel, UsersSavedTravels
from django.db.models import Min


BASE_IMAGES_URL = 'https://cruiseplannersnet.com'

class PaginatorCustom(Paginator):
    def page(self, number):
        "Returns a Page object for the given 1-based page number."
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return PageCustom(self.object_list[bottom:top], number, self)

    def get_num_pages(self):
        return self._get_num_pages()

class PageCustom(Page):
    def render(self):
        return render_to_string('frontend/pagination.html', {
            'current_page':self,
            'page_obj':self, # Issue 9 https://github.com/jamespacileo/django-pure-pagination/issues/9
                             # Use same naming conventions as Django
            })
    def __repr__(self):
        return 'Page %s of %s' % (self.number, self.paginator.num_pages)

def _get_sort_result(request, travel_dates):
    sort = request.GET.get('sort', None)
    sort_by = None

    if sort != None:
        sort_by_arr = sort.split('_')
        if len(sort_by_arr) == 2 and (sort_by_arr[1] == 'desc' or sort_by_arr[1] == 'asc'):
            direction = sort_by_arr[1]
            sort_by = sort_by_arr[0]
        else:
            raise Http404

    if not sort_by:
        travel_dates = travel_dates.extra(order_by= ['depart_date'])
    elif sort_by == 'cruiseLine':
        if direction == 'desc':
            travel_dates = travel_dates.extra(order_by= ['-travel__ship__cruise_line__name'])
        else:
            travel_dates = travel_dates.extra(order_by= ['travel__ship__cruise_line__name'])
    elif sort_by == 'price.inside':
        travel_dates = travel_dates.annotate(min_price = Min('inside_price'))
        if direction == 'desc':
            travel_dates_not_null = travel_dates.exclude(min_price = None).extra(order_by= ['-min_price'])
            travel_dates_null = travel_dates.filter(min_price = None).extra(order_by= ['-min_price'])
        else:
            travel_dates_not_null = travel_dates.exclude(min_price = None).extra(order_by= ['min_price'])
            travel_dates_null = travel_dates.filter(min_price = None).extra(order_by= ['min_price'])
        travel_dates =  list(travel_dates_not_null) + list(travel_dates_null)

    elif sort_by == 'price.oceanview':
        travel_dates = travel_dates.annotate(min_price = Min('ocean_price'))
        if direction == 'desc':
            travel_dates_not_null = travel_dates.exclude(min_price = None).extra(order_by= ['-min_price'])
            travel_dates_null = travel_dates.filter(min_price = None).extra(order_by= ['-min_price'])
        else:
            travel_dates_not_null = travel_dates.exclude(min_price = None).extra(order_by= ['min_price'])
            travel_dates_null = travel_dates.filter(min_price = None).extra(order_by= ['min_price'])
        travel_dates =  list(travel_dates_not_null) + list(travel_dates_null)
    elif sort_by == 'price.balcony':
        travel_dates = travel_dates.annotate(min_price = Min('balcony_price'))
        if direction == 'desc':
            travel_dates_not_null = travel_dates.exclude(min_price = None).extra(order_by= ['-min_price'])
            travel_dates_null = travel_dates.filter(min_price = None).extra(order_by= ['-min_price'])
        else:
            travel_dates_not_null = travel_dates.exclude(min_price = None).extra(order_by= ['min_price'])
            travel_dates_null = travel_dates.filter(min_price = None).extra(order_by= ['min_price'])
        travel_dates =  list(travel_dates_not_null) + list(travel_dates_null)
    elif sort_by == 'price.suite':
        travel_dates = travel_dates.annotate(min_price = Min('suite_price'))
        if direction == 'desc':
            travel_dates_not_null = travel_dates.exclude(min_price = None).extra(order_by= ['-min_price'])
            travel_dates_null = travel_dates.filter(min_price = None).extra(order_by= ['-min_price'])
        else:
            travel_dates_not_null = travel_dates.exclude(min_price = None).extra(order_by= ['min_price'])
            travel_dates_null = travel_dates.filter(min_price = None).extra(order_by= ['min_price'])
        travel_dates =  list(travel_dates_not_null) + list(travel_dates_null)
    elif sort_by == 'date':
        if direction == 'desc':
            travel_dates = travel_dates.extra(order_by= ['-depart_date'])
        else:
            travel_dates = travel_dates.extra(order_by= ['depart_date'])
    elif sort_by == 'length':
        if direction == 'desc':
            travel_dates = travel_dates.extra(order_by= ['-travel__nights'])
        else:
            travel_dates = travel_dates.extra(order_by= ['travel__nights'])
    elif sort_by == 'ship':
        if direction == 'desc':
            travel_dates = travel_dates.extra(order_by= ['-travel__ship__name'])
        else:
            travel_dates = travel_dates.extra(order_by= ['travel__ship__name'])
    elif sort_by == 'departure':
        if direction == 'desc':
            travel_dates = travel_dates.extra(order_by= ['-departure_port'])
        else:
            travel_dates = travel_dates.extra(order_by= ['departure_port'])

    return travel_dates

def travel_obj_to_list_custom(travel_dates_query, filter_ports):
    travel_dates_data = []
    for travel in travel_dates_query:
        try:
            travel = Travel.objects.get(unique_id=travel['travel_id'])
            td = travel.travel_dates.all()[0]
        except Travel.DoesNotExist, IndexError:
            return travel_dates_data
        ship_obj = travel.ship
        ship = {'name': ship_obj.name, 'big_logo_src': ship_obj.big_logo_src, 'slug': ship_obj.slug}
        cruise_line_obj = travel.ship.cruise_line
        cruise_line = {'name': cruise_line_obj.name, 'logo': BASE_IMAGES_URL + cruise_line_obj.logo, 'slug': cruise_line_obj.slug}

        ports = td.visited_ports.exclude(name = 'At Sea').exclude(name = '').order_by('traveldatesport__day_number')
        ports_data = []
        ports_data_temp = {}
        ports_name = []
        for p in ports:
            port_temp_dict = {'name': p.alias, 'slug': p.slug}
            if ports_data_temp.has_key(p.id) == False:
                ports_data.append(port_temp_dict)
                ports_name.append(p.alias)
            ports_data_temp[p.id] = p.alias

        departing_port = td.visited_ports.filter(traveldatesport__day_number=1)
        if departing_port:
            departing_from = '{port}, {country}'.format(port=departing_port[0].alias, country=departing_port[0].country.name)
            ports_data.remove({'name': departing_port[0].alias, 'slug': departing_port[0].slug})
        else:
            departing_from = ' '

        inside_price = TravelDates.objects.exclude(inside_price = None).filter(travel=travel).aggregate(Min('inside_price'))['inside_price__min']
        ocean_price = TravelDates.objects.exclude(ocean_price = None).filter(travel=travel).aggregate(Min('ocean_price'))['ocean_price__min']
        balcony_price = TravelDates.objects.exclude(balcony_price = None).filter(travel=travel).aggregate(Min('balcony_price'))['balcony_price__min']
        suite_price = TravelDates.objects.exclude(suite_price = None).filter(travel=travel).aggregate(Min('suite_price'))['suite_price__min']
        salling_dates_available = travel.nights



        travel_temp_dict = {
            'id': td.id,
            'url': td.url,
            'count': salling_dates_available,
            'travel_unique_id': travel.unique_id,
            'name': travel.name,
            'depart_date': td.depart_date,
            'depart_date_str': str(td.depart_date),
            'ship': ship,
            'departing_from': departing_from,
            'ports': ports_data,
            'cruise_line': cruise_line,
            'inside': inside_price,
            'oceanview': ocean_price,
            'balcony': balcony_price,
            'suite': suite_price,
            'depart_year': str(td.depart_date.year)
        }
        if (compare_array(filter_ports, ports_name)):
            travel_dates_data.append(travel_temp_dict)

    return travel_dates_data


def travel_obj_to_list(travel_dates_query, request = None):
    travel_dates_data = []
    for travel in travel_dates_query:
        ship_obj = travel.ship
        ship = {'name': ship_obj.name, 'big_logo_src': ship_obj.big_logo_src, 'slug': ship_obj.slug}
        cruise_line_obj = travel.ship.cruise_line
        cruise_line = {'name': cruise_line_obj.name, 'logo': BASE_IMAGES_URL + cruise_line_obj.logo, 'slug': cruise_line_obj.slug}

        ports = travel.visited_ports.exclude(name = 'At Sea').exclude(name = '').order_by('traveldatesport__day_number')
        ports_data = []
        ports_data_temp = {}
        for p in ports:
            port_temp_dict = {'name': p.alias, 'slug': p.slug}
            if ports_data_temp.has_key(p.id) == False:
                ports_data.append(port_temp_dict)
            ports_data_temp[p.id] = p.alias

        departing_port = travel.departure_port
        if departing_port == None or departing_port.name == None:
            departing_from = ' '
        else:
            departing_from = departing_port.name

        is_saved = False
        if request.user.is_authenticated:
            if UsersSavedTravels.objects.filter(travel_date_id = travel.id).filter(user = request.user).count() > 0:
                is_saved = True


        inside_price = travel.inside_price
        ocean_price = travel.ocean_price
        balcony_price = travel.balcony_price
        suite_price = travel.suite_price
        salling_dates_available = travel.nights
        travel_temp_dict = {
            'id': travel.id,
            'url': travel.url,
            'count': salling_dates_available,
            'is_saved': is_saved,
            # 'travel_unique_id': travel.unique_id,
            'name': travel.name,
            'depart_date': travel.depart_date,
            'depart_date_str': str(travel.depart_date),
            'ship': ship,
            'departing_from': departing_from,
            'ports': ports_data,
            'cruise_line': cruise_line,
            'inside': inside_price,
            'oceanview': ocean_price,
            'balcony': balcony_price,
            'suite': suite_price,
            'depart_year': str(travel.depart_date.year)
        }
        travel_dates_data.append(travel_temp_dict)

    return travel_dates_data