__author__ = 'ernesto'
from datetime import timedelta
import datetime
from django.db import models


class RegionQuerySet(models.QuerySet):
    pass

class RegionManager(models.Manager):
    def get_queryset(self):
        return RegionQuerySet(self.model, using=self._db).order_by('name')

class CruiseLineQuerySet(models.QuerySet):
    def filter_by_destination(self, destination):
        pass

class CruiseLineManager(models.Manager):
    def get_queryset(self):
        return CruiseLineQuerySet(self.model, using=self._db).order_by('name')

    def filter_by_destination(self, destination):
        return self.get_queryset().filter_by_destination(destination);

class SubRegionQuerySet(models.QuerySet):
    def get_subregions_active(self):
        return self.filter(is_active_destination = 1)

class SubRegionManager(models.Manager):
    def get_queryset(self):
        return SubRegionQuerySet(self.model, using=self._db).order_by('name')

    def get_subregions_active(self):
        return self.get_queryset().get_subregions_active()


class TravelQuerySet(models.QuerySet):
    def get_nights(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT t.nights
            FROM backend_travel t
            GROUP BY nights
            ORDER BY t.nights asc""")

        result_list = []
        for row in cursor.fetchall():
            print row
            p = self.model(nights=row[0])
            result_list.append(p)
        return result_list



class TravelManager(models.Manager):
    def get_queryset(self):
        return TravelQuerySet(self.model, using=self._db).all()

    def get_nights(self):
        return self.get_queryset().get_nights()


class TravelDatesQuerySet(models.QuerySet):

    def get_travels_current_month(self):
        current_month = datetime.datetime.today().month
        current_year = datetime.datetime.today().year
        import calendar
        last_day = calendar.monthrange(current_year, current_month)[1]
        last_date = datetime.date(current_year, current_month, int(last_day))
        return self.filter(depart_date__lte = last_date)

    def get_by_date(self, date):
        return self.filter(depart_date__year = date.year).filter(depart_date__month = date.month)

    def get_by_region(self, destination):
        return self.filter(travel__destination__region__name = destination)

    def get_by_region_id(self, region_id):
        return self.filter(destination__region_id = region_id)

    def get_by_region_slug(self, region_slug):
        return self.filter(destination__region__slug = region_slug)

    def get_by_subregion(self, destination):
        return self.filter(destination__name = destination)

    def get_by_subregion_alias(self, destination):
        if destination == 'Caribbean':
            return self.filter(destination__alias__icontains = destination)

        return self.filter(destination__alias = destination)

    def get_by_subregion_id(self, subregion_id):
        return self.filter(destination_id = subregion_id)

    def get_by_subregion_slug(self, destination_slug):
        return self.filter(destination__slug = destination_slug).filter(destination__is_active_destination=1)

    def get_by_cruise_line_name(self, cruise_line_name):
        return self.filter(ship__cruise_line__name =  cruise_line_name)

    def get_by_cruise_line_slug(self, cruise_line_slug):
        return self.filter(ship__cruise_line__slug =  cruise_line_slug)

    def get_by_ship_name(self, ship_name):
        return self.filter(ship__name =  ship_name)

    def get_by_ship_slug(self, ship_slug):
        return self.filter(ship__slug =  ship_slug)

    def get_by_departure_port(self, departure_port_name):
        return self.filter(visited_ports__name = departure_port_name, traveldatesport__day_number = 1)

    def get_by_departure_port_slug(self, departure_port_slug):
        return self.filter(visited_ports__slug = departure_port_slug, traveldatesport__day_number = 1)

    def get_by_length_range(self, min_length = 0, max_length = 0):
        if max_length != 0:
            return self.filter(nights__gte = min_length).filter(travel__nights__lte = max_length)
        else:
            return self.filter(nights__gte = min_length)

    def get_by_length(self, length = 0):
        if length != 0:
            return self.filter(nights = length)
        else:
            return self.all()

    def get_by_destination_port(self, destination_port):
        from django.db.models import Count
        return self.filter(visited_ports__slug = destination_port).annotate(Count('id'))


class TravelDatesManager(models.Manager):
    def get_queryset(self):
        yesterday = datetime.datetime.today() - timedelta(days=1)
        return TravelDatesQuerySet(self.model, using=self._db).filter(depart_date__gt = yesterday)

    def get_travels_current_month(self):
        return self.get_queryset().get_travels_current_month()

    def get_by_date(self, date):
        return self.get_queryset().get_by_date(date)

    def get_by_region(self, destination):
        return self.get_queryset().get_by_region(destination)

    def get_by_region_id(self, region_id):
        return self.get_queryset().get_by_region_id(region_id)

    def get_by_region_slug(self, region_slug):
        return self.get_queryset().get_by_region_slug(region_slug)

    def get_by_subregion(self, destination):
        return self.get_queryset().get_by_subregion(destination)

    def get_by_subregion_id(self, subregion_id):
        return self.get_queryset().get_by_subregion_id(subregion_id)

    def get_by_subregion_slug(self, destination_slug):
        return self.get_queryset().get_by_subregion_slug(destination_slug)

    def get_by_cruise_line_name(self, cruise_line_name):
        return self.get_queryset().get_by_cruise_line_name(cruise_line_name=cruise_line_name)

    def get_by_cruise_line_slug(self, cruise_line_slug):
        return self.get_queryset().get_by_cruise_line_slug(cruise_line_slug=cruise_line_slug)

    def get_by_ship_name(self, ship_name):
        return self.get_queryset().get_by_ship_name(ship_name=ship_name)

    def get_by_ship_slug(self, ship_slug):
        return self.get_queryset().get_by_ship_slug(ship_slug=ship_slug)

    def get_by_departure_port(self, departure_port_name):
        return self.get_queryset().get_by_departure_port(departure_port_name)

    def get_by_departure_port_slug(self, departure_port_slug):
        return self.get_queryset().get_by_departure_port_slug(departure_port_slug)

    def get_by_length_range(self, min_length = 0, max_length = 0):
        return self.get_queryset().get_by_length_range(min_length=min_length, max_length=max_length)

    def get_by_destination_port(self, destination_port):
        return self.get_queryset().get_by_destination_port(destination_port)


class PortQuerySet(models.QuerySet):
    def get_departure_port(self):
        return self.filter(is_active_depart = 1).exclude(name = 'At Sea').exclude(name = '').exclude(name = None)

    def get_destination_port(self):
        return self.filter(is_active_destination = 1).exclude(name = 'At Sea').exclude(name = '').exclude(name = None)

    def get_by_name(self, name):
        return self.get(name = name)


class PortManager(models.Manager):
    def get_queryset(self):
        return PortQuerySet(self.model, using=self._db).order_by('name')

    def get_departure_port(self):
        return self.get_queryset().get_departure_port()

    def get_destination_port(self):
        return self.get_queryset().get_destination_port()

    def get_by_name(self, name):
        return self.get_queryset().get_by_name(name=name)


class CountryQuerySet(models.QuerySet):
    def get_destination_countries(self):
        return self.filter(is_active_destination = 1)

class CountryManager(models.Manager):
    def get_queryset(self):
        return CountryQuerySet(self.model, using=self._db).order_by('name')

    def get_destination_countries(self):
        return self.get_queryset().get_destination_countries()