from django.contrib import admin
from django.db.models.aggregates import Count
from backend.managers import *
from django.template import defaultfilters
from suit.admin import SortableTabularInline
from django.contrib.auth.models import User

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(null=True, blank=True)
    slug = models.SlugField(null=True, max_length=255)
    objects = RegionManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.name)
        super(Region, self).save(*args, **kwargs)

class CruiseLine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    logo = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(null=True, max_length=255)
    objects = CruiseLineManager()

    def __str__(self):
        return self.name

    def getTravelsByDestination(self, destination):
        travels = Travel.objects.values('id').filter(ship_id__in=self.ship_set.all()).filter(destination_id=destination)
        travels_data = []
        for travel in travels:
            if not travel['id'] in travels_data:
                travels_data.append(travel['id'])
        return travels_data

    def getTravelsByDeparture(self, port):
        travels = TravelDates.objects.filter(travel__ship_id__in=self.ship_set.all()).filter(departure_port=port)
        travels_data = []
        for travel_date in travels:
            if not travel_date.travel.id in travels_data:
                travels_data.append(travel_date.travel.id)
        return travels_data

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.name)
        super(CruiseLine, self).save(*args, **kwargs)

    def getDestinationByPort(self, port):
        travel = Travel.objects.values('destination_id').filter(ship__in = self.ship_set.all()).filter().order_by('destination__name').annotate(count = Count('destination_id'))


class SubRegion(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE)
    url = models.URLField(null=True, blank=True)
    slug = models.SlugField(null=True, max_length=255)
    objects = SubRegionManager()
    is_active_destination = models.BooleanField(default=1, verbose_name='Active for destination')
    alias = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def getTravels(self):
        travels = self.travel_set.values('id').all().annotate(count=Count('ship'))
        travels_data = []
        for travel in travels:
            if not travel['id'] in travels_data:
                travels_data.append(travel['id'])
        return travels_data

    def getCruisesLines(self):
        cruiseslines = CruiseLine.objects.values('id').filter(ship__travel__in=self.travel_set.all()).annotate(count=Count('id'))
        lines_data = []
        for cruiselines in cruiseslines:
            if not cruiselines['id'] in lines_data:
                lines_data.append(cruiselines['id'])
        return lines_data

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.name)
        super(SubRegion, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "SubRegions"
        verbose_name = 'SubRegion'
        ordering = ['name']

class Ship(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    big_logo_src = models.CharField(max_length=200, null=True, blank=True)
    small_logo_src = models.CharField(max_length=200, null=True, blank=True)
    cruise_line = models.ForeignKey(CruiseLine, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, max_length=255)

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.name)
        super(Ship, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Travel(models.Model):
    id = models.AutoField(primary_key=True)
    unique_id = models.CharField(unique=True, max_length=255, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    destination = models.ForeignKey(SubRegion, null=True, blank=True)
    ship = models.ForeignKey(Ship)
    nights = models.IntegerField(default=0)

    objects = TravelManager()

    def __str__(self):
        return self.ship.name

class TravelDates(models.Model):
    id = models.AutoField(primary_key=True)

    #----------------------
    destination = models.ForeignKey(SubRegion, null=True, blank=True)
    ship = models.ForeignKey(Ship)
    nights = models.IntegerField(default=0)
    name = models.CharField(max_length=200, null=False, blank=False)
    #----------------------


    # travel = models.ForeignKey(Travel, to_field='unique_id', null=True, blank=True, related_name='travel_dates')
    url = models.URLField(null=True, blank=True)


    depart_date = models.DateField(max_length=200, null=True, blank=True)
    return_date = models.DateField(max_length=200, null=True, blank=True)

    inside_price = models.FloatField(null=True, blank=True)
    ocean_price = models.FloatField(null=True, blank=True)
    balcony_price = models.FloatField(null=True, blank=True)
    suite_price = models.FloatField(null=True, blank=True)

    departure_port = models.ForeignKey('Port', related_name='departure_port', null=True, on_delete = models.SET_NULL)
    destination_port = models.ForeignKey('Port', related_name='destination_port', null=True, on_delete = models.SET_NULL)

    visited_ports = models.ManyToManyField('Port', through='TravelDatesPort')

    travelUserSaved = models.ManyToManyField(User, through='UsersSavedTravels')

    objects = TravelDatesManager()
    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=255)
    is_active_depart = models.BooleanField(default=1, verbose_name='Active for departure')
    is_active_destination = models.BooleanField(default=1, verbose_name='Active for destination')
    objects = CountryManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.is_active_depart:
            self.port_set.all().update(is_active_depart=0)

        if not self.is_active_destination:
            self.port_set.all().update(is_active_destination=0)

        super(Country, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "countries"
        ordering = ['name']

class Port(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(null=True, max_length=255)

    is_active_depart = models.BooleanField(default=1, verbose_name='Active for departure')
    is_active_destination = models.BooleanField(default=1, verbose_name='Active for destination')
    alias = models.CharField(max_length=255, null=True, blank=True)

    travels = models.ManyToManyField(TravelDates, through= "TravelDatesPort")

    objects = PortManager()

    def __str__(self):
        return self.name + ", " + self.country.name


    def getTravelsDestination(self):
        travels = self.traveldates_set.values('travel_id').filter(visited_ports__slug=self.slug).\
            filter(travel__destination__is_active_destination=1).annotate(count=Count('travel_id'))
        travels_data = []
        for travel in travels:
            travel = Travel.objects.get(unique_id=travel['travel_id'])
            if not travel.id in travels_data:
                travels_data.append(travel.id)
        return travels_data

    def getTravelsDeparture(self):
        travels = self.traveldates_set.values('travel_id').filter(departure_port=self.name).annotate(count=Count('travel_id'))
        travels_data = []
        for travel in travels:
            travel = Travel.objects.get(unique_id=travel['travel_id'])
            if not travel.id in travels_data:
                travels_data.append(travel.id)
        return travels_data

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.name + ' ' + self.country.name)
        if self.is_active_depart and not self.country.is_active_depart:
            self.country.is_active_depart = 1
            self.country.save()
        super(Port, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "ports"

class TravelDatesPort(models.Model):
    port = models.ForeignKey(Port, null=True, blank=True, on_delete=models.CASCADE)
    travel_date = models.ForeignKey(TravelDates, null=True, blank=True, on_delete=models.CASCADE)

    day_number = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    arrive_time = models.TimeField(null=True, blank=True)
    return_time = models.TimeField(null=True, blank=True)


class Subscriptions(models.Model):
    email = models.EmailField(max_length=255, blank=False, null=False, unique=True)
    exported = models.BooleanField(default=0, verbose_name='Exported')

    class Meta:
        verbose_name_plural = "Subscriptions"
        verbose_name = 'Subscriptions'


class UsersSavedTravels(models.Model):
    user = models.ForeignKey(User)
    travel_date = models.ForeignKey(TravelDates, on_delete=models.CASCADE)


class TravelsPortInline(admin.TabularInline):
    model = Port.travels.through


class CountryAdmin(admin.ModelAdmin):
    fields = ('name', 'is_active_depart', 'is_active_destination')
    list_display = ['name', 'is_active_depart', 'is_active_destination']
    list_editable = ('is_active_depart', 'is_active_destination')
    readonly_fields = ('name',)
    search_fields = ['name']
    list_per_page = 50

class SubRegionAdmin(admin.ModelAdmin):
    fields = ('name','alias', 'is_active_destination')
    list_display = ['name','alias','is_active_destination']
    list_editable = ('alias','is_active_destination',)
    #list_filter = ('name', )
    readonly_fields = ('name',)
    list_per_page = 25
    list_display_links = None
    search_fields = ['name']

class SubscriptionsAdmin(admin.ModelAdmin):
    fields = ('email','exported')
    list_display = ['email','exported']
    readonly_fields = ['email']
    list_editable = ('exported',)

class TravelDatesAdmin(admin.ModelAdmin):
    inlines = [TravelsPortInline, ]


    pass

admin.site.register(Country, CountryAdmin)
admin.site.register(SubRegion, SubRegionAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)
admin.site.register(TravelDates, TravelDatesAdmin)
