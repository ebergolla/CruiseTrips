from django.http.response import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from launchCodeDemo.settings import BASE_IMAGES_URL, EMAIL_HOST_USER, LOGIN_URL
from pure_pagination import PageNotAnInteger
from backend.helpers import PaginatorCustom, _get_sort_result, travel_obj_to_list
from launchCodeDemo.settings import OBJECTS_PER_PAGE
from django.http.response import HttpResponse, Http404
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from frontend.models import *
from backend.models import *

# Create your views here.

def index(request):
    deals = CruiseDeal.objects.exclude(show_in_home=0).order_by('order')[:4]
    top_dest = TopDestination.objects.order_by('order')[:12]
    return render(request, 'frontend/index.html',{'deals': deals, 'top_dest': top_dest, 'base_image_url':BASE_IMAGES_URL})

def cruise_deals(request):
    try:
        page = request.GET.get('page', 1)
        page = int(page)
    except PageNotAnInteger:
        page = 1
    except ValueError:
        raise Http404

    cruises_deals = CruiseDeal.objects.order_by('order')
    paginator = PaginatorCustom(cruises_deals,OBJECTS_PER_PAGE, request=request)
    cruises_deals_page = paginator.page(page)

    return render(request, 'frontend/cruise_deals.html',
                              {'cruises_deals': cruises_deals,'deals_page': cruises_deals_page,'base_image_url':BASE_IMAGES_URL},
                              )

def destinations(request):

    regions_query = Region.objects.all()
    subregions_query = SubRegion.objects.get_subregions_active()

    regions_data = []
    list_temp = []
    for r in regions_query:
        if TravelDates.objects.get_by_region_id(r.id).count() != 0:
            temp = {'id': r.id, 'name': r.name, 'slug': r.slug}
            list_temp.append(temp)
            if len(list_temp) == 3 or r == regions_query[len(regions_query) - 1]:
                regions_data.append(list_temp)
                list_temp = []

    subregions_data = []
    for sr in subregions_query:
         if TravelDates.objects.get_by_subregion_id(sr.id).count() != 0:
            temp = {'id': sr.id, 'name': sr.name, 'slug': sr.slug}
            subregions_data.append(temp)


    count_regions = len(subregions_data)
    part_1 = part_2 = part_3 = count_regions/3

    if count_regions%3 == 1:
        part_1 += 1
    elif count_regions%3 == 2:
        part_1 += 1
        part_2 += 1

    r_data_1 = subregions_data.__getslice__(0, part_1)
    r_data_2 = subregions_data.__getslice__(part_1, part_1 + part_2)
    r_data_3 = subregions_data.__getslice__(part_1 + part_2, count_regions + 1)


    from django.template import defaultfilters
    country_destinations = Country.objects.get_destination_countries()

    country_destinations_data = []

    for cd in country_destinations:
        ports = cd.port_set.get_destination_port()
        ports_add = []
        for p in ports:
            port_temp = {'slug': p.slug, 'name': p.name, "id": p.id}
            if p.traveldates_set.count() != 0:
                ports_add.append(port_temp)

        if len(ports_add) > 0:
            temp = {'country_name': cd.name, 'country_slug': defaultfilters.slugify(cd.name),'ports': ports_add}
            country_destinations_data.append(temp)

    count_ports = len(country_destinations_data)
    part_1 = part_2 = part_3 = count_ports/3

    if count_ports%3 == 1:
        part_1 += 1
    elif count_ports%3 == 2:
        part_1 += 1
        part_2 += 1

    port_data_1 = country_destinations_data.__getslice__(0, part_1)
    port_data_2 = country_destinations_data.__getslice__(part_1, part_1 + part_2)
    port_data_3 = country_destinations_data.__getslice__(part_1 + part_2, count_ports + 1)

    countries = Country.objects.values('id','name' ).all()
    return render(request, 'frontend/destinations.html',
                              {'regions': regions_data,
                               'subregions': [r_data_1, r_data_2, r_data_3],
                                'countries': countries,
                                'port_data_1': port_data_1,
                                'port_data_2': port_data_2,
                                'port_data_3': port_data_3,
                              },
                              )

def departures(request):

    departure_ports = Port.objects.get_departure_port()
    departure_ports_data = []
    for p in departure_ports:
        if p.traveldates_set.all().count() != 0:
            name = p.name
            if p.country != None:
                name += ', ' + p.country.name
            temp = {'id': p.id, 'name':name, 'slug': p.slug}
            departure_ports_data.append(temp)

    count_d = len(departure_ports_data)
    part_1 = part_2 = part_3 = count_d/3

    if count_d%3 == 1:
        part_1 += 1
    elif count_d%3 == 2:
        part_1 += 1
        part_2 += 1

    port_data_1 = departure_ports_data.__getslice__(0, part_1)
    port_data_2 = departure_ports_data.__getslice__(part_1, part_1 + part_2)
    port_data_3 = departure_ports_data.__getslice__(part_1 + part_2, count_d + 1)

    return render(request, 'frontend/departures.html', {'ports': [port_data_1, port_data_2, port_data_3]})

def cruises_lines(request):
    cruise_lines_query = CruiseLine.objects.all()

    cruise_lines_data = []
    list_temp = []
    for cl in cruise_lines_query:
        if TravelDates.objects.get_by_cruise_line_slug(cl.slug).count() != 0:
            temp = {'id': cl.id, 'name': cl.name, 'slug': cl.slug}
            cruise_lines_data.append(temp)

    count_l = len(cruise_lines_data)
    part_1 = part_2 = part_3 = count_l/3

    if count_l%3 == 1:
        part_1 += 1
    elif count_l%3 == 2:
        part_1 += 1
        part_2 += 1

    l_data_1 = cruise_lines_data.__getslice__(0, part_1)
    l_data_2 = cruise_lines_data.__getslice__(part_1, part_1 + part_2)
    l_data_3 = cruise_lines_data.__getslice__(part_1 + part_2, count_l + 1)

    return render(request, 'frontend/cruises_lines.html',
                                    {'cruise_lines': [l_data_1, l_data_2, l_data_3]},
                                    )

def cruise_details(request, slug):

    try:
        cruise_line = CruiseLine.objects.get(slug = slug)
    except CruiseLine.DoesNotExist:
        raise Http404
    cruise_line_data = {'name': cruise_line.name, 'slug': cruise_line.slug}

    ships = Ship.objects.filter(cruise_line = cruise_line).order_by('name')

    ship_data = []

    for s in ships:
        ship_data.append({'slug': s.slug, 'name': s.name, 'small_logo': s.small_logo_src, 'big_logo': s.big_logo_src})

    destinations_data = []

    t_destinations = Travel.objects.values('destination_id').filter(ship__in = ships).order_by('destination__name').annotate(count = Count('destination_id'))

    for d in t_destinations:
        dest = SubRegion.objects.get(pk = d['destination_id'])
        if TravelDates.objects.get_by_cruise_line_slug(slug).get_by_subregion_slug(dest.slug).count() != 0:
            destinations_data.append({'name': dest.name, 'id': dest.id, 'slug': dest.slug})

    departure_port_data = []

    departure_port_query = TravelDates.objects.values('departure_port').filter(ship_id__in = ships, traveldatesport__day_number = 1).order_by('departure_port').annotate(count = Count('departure_port'))

    for dp in departure_port_query:
        try:
            d_temp = Port.objects.get_by_name(dp['departure_port'])
            if d_temp.is_active_depart:
                name = d_temp.name
                if d_temp.country != None:
                    name += ', ' + d_temp.country.name
                departure_port_data.append({'name': name, 'slug': d_temp.slug})
        except Port.DoesNotExist:
            pass

    params = {'cruise_line': cruise_line_data,'ships': ship_data,'destinations': destinations_data,'departures': departure_port_data}

    return render(request, 'frontend/cruises_line_details.html',params)


@csrf_exempt
def search_cruises(request, **kwargs):
    travel_dates = TravelDates.objects.all()

    if request.GET.has_key('date'):
        date =  '01/' + request.GET['date']
        try:
            import datetime
            date = datetime.datetime.strptime(date, '%d/%m/%Y')
        except Exception, e:
            raise Http404
        travel_dates = travel_dates.get_by_date(date)
    elif len(request.GET) == 0 or (len(request.GET) == 1 and (request.GET.has_key('sort') or request.GET.has_key('page'))):
        pass

    if request.GET.has_key('length'):
        length = request.GET['length']
        travel_dates = travel_dates.get_by_length(length)

    if request.GET.has_key('destination'):
        destination = request.GET['destination']
        travel_dates = travel_dates.get_by_subregion_alias(destination)

    if request.GET.has_key('cruiseLine'):
        cruise_line = request.GET['cruiseLine']
        travel_dates = travel_dates.get_by_cruise_line_name(cruise_line)

    if request.GET.has_key('ship'):
        ship = request.GET['ship']
        travel_dates = travel_dates.get_by_ship_name(ship)

    if request.GET.has_key('departure'):
        departure = request.GET['departure']
        travel_dates = travel_dates.get_by_departure_port_slug(departure)

    if request.GET.has_key('q'):
        from django.db.models import Q
        query_text = request.GET['q']
        travel_dates = travel_dates.filter(Q(name__icontains = query_text)
        | Q(destination_port__name__icontains = query_text) | Q(ship__name__icontains = query_text)
        | Q(ship__cruise_line__name__icontains = query_text) | Q(departure_port__name__icontains = query_text))


    try:
        page = request.GET.get('page', 1)
        page = int(page)
    except PageNotAnInteger:
        page = 1
    except ValueError:
        raise Http404

    travel_dates = _get_sort_result(request, travel_dates)

    paginator = PaginatorCustom(travel_dates,OBJECTS_PER_PAGE, request=request)

    try:
        travel_dates_page = paginator.page(page)
        travel_dates_data = travel_obj_to_list(travel_dates_page.object_list, request)
    except Exception:
        paginator = PaginatorCustom(TravelDates.objects.none(),OBJECTS_PER_PAGE, request=request)
        travel_dates_page = paginator.page(1)
        travel_dates_data = {}


    params = {'travels': travel_dates_data, 'pager': travel_dates_page}

    return render(request, 'frontend/search_result.html',params)

def cruise_by_destination_port(request, destination_port):

    travel_dates = TravelDates.objects.get_by_destination_port(destination_port).order_by('depart_date')
    travel_dates = _get_sort_result(request, travel_dates)
    try:
        page = request.GET.get('page', 1)
        page = int(page)
    except PageNotAnInteger:
        page = 1
    except ValueError:
        raise Http404

    paginator = PaginatorCustom(travel_dates,OBJECTS_PER_PAGE, request=request)

    try:
        travel_dates_page = paginator.page(page)
        travel_dates_data = travel_obj_to_list(travel_dates_page.object_list, request)
    except Exception:
        paginator = PaginatorCustom(TravelDates.objects.none(),OBJECTS_PER_PAGE, request=request)
        travel_dates_page = paginator.page(1)
        travel_dates_data = {}

    params = {'travels': travel_dates_data, 'pager': travel_dates_page}

    return render(request, 'frontend/search_result.html',params)

def cruise_by_departure_port(request, departure_port_slug):

    travel_dates = TravelDates.objects.get_by_departure_port_slug(departure_port_slug)
    travel_dates = _get_sort_result(request, travel_dates)
    try:
        page = request.GET.get('page', 1)
        page = int(page)
    except PageNotAnInteger:
        page = 1
    except ValueError:
        raise Http404


    paginator = PaginatorCustom(travel_dates,OBJECTS_PER_PAGE, request=request)

    try:
        travel_dates_page = paginator.page(page)
        travel_dates_data = travel_obj_to_list(travel_dates_page.object_list, request)
    except Exception:
        paginator = PaginatorCustom(TravelDates.objects.none(),OBJECTS_PER_PAGE, request=request)
        travel_dates_page = paginator.page(1)
        travel_dates_data = {}

    params = {'travels': travel_dates_data, 'pager': travel_dates_page}

    return render(request, 'frontend/search_result.html',params)

def cruise_by_destination(request, type, destination):

    if type == 'subregion':
        travel_dates = TravelDates.objects.get_by_subregion_slug(destination).order_by('depart_date')
    elif type == 'region':
        travel_dates = TravelDates.objects.get_by_region_slug(destination).order_by('depart_date')
    travel_dates = _get_sort_result(request, travel_dates)
    try:
        page = request.GET.get('page', 1)
        page = int(page)
    except PageNotAnInteger:
        page = 1
    except ValueError:
        raise Http404

    paginator = PaginatorCustom(travel_dates,OBJECTS_PER_PAGE, request=request)

    try:
        travel_dates_page = paginator.page(page)
        travel_dates_data = travel_obj_to_list(travel_dates_page.object_list, request)
    except Exception:
        paginator = PaginatorCustom(TravelDates.objects.none(),OBJECTS_PER_PAGE, request=request)
        travel_dates_page = paginator.page(1)
        travel_dates_data = {}
    params = {'travels': travel_dates_data, 'pager': travel_dates_page}

    return render(request, 'frontend/search_result.html',params)

def cruise(request, cruiseid):
    travel = TravelDates.objects.get(pk=cruiseid)
    from django.shortcuts import redirect
    return redirect(travel.url)

def cruise_by_line_ship(request, cruise_line_slug, ship_slug):

    travel_dates = TravelDates.objects.get_by_ship_slug(ship_slug)
    travel_dates = _get_sort_result(request, travel_dates)

    try:
        page = request.GET.get('page', 1)
        page = int(page)
    except PageNotAnInteger:
        page = 1
    except ValueError:
        raise Http404

    paginator = PaginatorCustom(travel_dates,OBJECTS_PER_PAGE, request=request)

    try:
        travel_dates_page = paginator.page(page)
        travel_dates_data = travel_obj_to_list(travel_dates_page.object_list, request)
    except Exception:
        paginator = PaginatorCustom(TravelDates.objects.none(),OBJECTS_PER_PAGE, request=request)
        travel_dates_page = paginator.page(1)
        travel_dates_data = {}


    params = {'travels': travel_dates_data, 'pager': travel_dates_page}

    return render(request, 'frontend/search_result.html',params)

def cruise_by_line_subregion(request, cruise_line_slug, subregion):

    travel_dates = TravelDates.objects.get_by_cruise_line_slug(cruise_line_slug).get_by_subregion_slug(subregion)
    travel_dates = _get_sort_result(request, travel_dates)
    try:
        page = request.GET.get('page', 1)
        page = int(page)
    except PageNotAnInteger:
        page = 1
    except ValueError:
        raise Http404

    paginator = PaginatorCustom(travel_dates,OBJECTS_PER_PAGE, request=request)

    try:
        travel_dates_page = paginator.page(page)
        travel_dates_data = travel_obj_to_list(travel_dates_page.object_list, request)
    except Exception:
        paginator = PaginatorCustom(TravelDates.objects.none(),OBJECTS_PER_PAGE, request=request)
        travel_dates_page = paginator.page(1)
        travel_dates_data = {}

    params = {'travels': travel_dates_data, 'pager': travel_dates_page}

    return render(request, 'frontend/search_result.html',params)
def cruise_by_line_departure(request, cruise_line_slug, departure_port_slug):

    travel_dates = TravelDates.objects.get_by_cruise_line_slug(cruise_line_slug).\
        get_by_departure_port_slug(departure_port_slug)
    travel_dates = _get_sort_result(request, travel_dates)

    try:
        page = request.GET.get('page', 1)
        page = int(page)
    except PageNotAnInteger:
        page = 1
    except ValueError:
        raise Http404

    paginator = PaginatorCustom(travel_dates,OBJECTS_PER_PAGE, request=request)

    try:
        travel_dates_page = paginator.page(page)
        travel_dates_data = travel_obj_to_list(travel_dates_page.object_list, request)
    except Exception:
        paginator = PaginatorCustom(TravelDates.objects.none(),OBJECTS_PER_PAGE, request=request)
        travel_dates_page = paginator.page(1)
        travel_dates_data = {}



    params = {'travels': travel_dates_data, 'pager': travel_dates_page}

    return render(request, 'frontend/search_result.html',params)


def save_travel(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (LOGIN_URL, request.path))

def get_saved_travels(request):
    if request.user.is_authenticated:
        travel_dates = request.user.traveldates_set.all()
        travel_dates = _get_sort_result(request, travel_dates)

        try:
            page = request.GET.get('page', 1)
            page = int(page)
        except PageNotAnInteger:
            page = 1
        except ValueError:
            raise Http404

        paginator = PaginatorCustom(travel_dates,OBJECTS_PER_PAGE, request=request)

        try:
            travel_dates_page = paginator.page(page)
            travel_dates_data = travel_obj_to_list(travel_dates_page.object_list, request)
        except Exception:
            paginator = PaginatorCustom(TravelDates.objects.none(),OBJECTS_PER_PAGE, request=request)
            travel_dates_page = paginator.page(1)
            travel_dates_data = {}

        params = {'travels': travel_dates_data, 'pager': travel_dates_page}

    return render(request, 'frontend/saved_travels.html',params)
#funciton that returns JSON

def get_ships_by_cruiseline(request):
    if request.GET.has_key('cruise_line_id'):
        cruise_line_id =  request.GET['cruise_line_id']
        ships_query = Ship.objects.filter(cruise_line_id = cruise_line_id)
        ships_arr = []
        for ship in ships_query:
            ships_arr.append({'id': ship.id, 'name': ship.name})
        json_result = json.dumps(ships_arr)

        return HttpResponse(json_result, content_type='application/json')
    else:
        return HttpResponse(json.dumps({}), content_type='application/json')

def subscribe(request):
    if request.POST.has_key('email'):
        email = request.POST['email']
        try:
            Subscriptions.objects.get(email = email)
            data = json.dumps({'success': 0})
        except Subscriptions.DoesNotExist:
            Subscriptions.objects.create(email=email)
            data = json.dumps({'success': 1})
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def send_email(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        comment = request.POST['comment']
        send_mail('Customer Question', comment, email, [EMAIL_HOST_USER],fail_silently=False)
    return redirect(request.META['HTTP_REFERER'])

def authenticateUser(request):
    if request.POST.has_key('username') and request.POST.has_key('password'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(json.dumps({"message": "Authentication successful!" ,'success': 1}), content_type='application/json')
    return HttpResponse(json.dumps({'message': "Username or password are incorrect!" ,'success': 0}), content_type='application/json')

def create_user(request):
    username = request.POST['username']
    password = request.POST['password']
    from django.contrib.auth.models import User
    try:
        user = User.objects.create_user(username, username, password)
        message = "User created successful!"
        success = 1
    except Exception, e:
        message = "Invalid email!"
        success = 0
    return HttpResponse(json.dumps({"message": message,'success': success}), content_type='application/json')


def logout_user(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('/')

def toggle_save_travel(request):
    if request.user.is_authenticated:
        traveldate_id = request.GET['travel_id']
        saved_travels = UsersSavedTravels.objects.filter(travel_date_id = traveldate_id).filter(user = request.user)
        if len(saved_travels) == 0:
            travelUser = UsersSavedTravels(travel_date_id = traveldate_id, user = request.user)
            travelUser.save()
            return HttpResponse(json.dumps({"message": "Travel was saved successful!",'success': 1}), content_type='application/json')
        else:
            saved_travels[0].delete()
            return HttpResponse(json.dumps({"message": "Travel was unsaved successful!",'success': 2}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({"message": "You need be authenticated!",'success': 0}), content_type='application/json')
