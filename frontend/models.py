# Create your models here.
from django.db import models
from django.contrib import admin
import floppyforms.__future__ as forms
from floppyforms.widgets import Select

from suit.admin import SortableModelAdmin
from suit_redactor.widgets import RedactorWidget
from backend.models import CruiseLine, SubRegion


class BannerImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='uploads', help_text='The image dimension should be 1680x1050')
    order = models.PositiveIntegerField(null=True)

    def image_thumb(self):
        if self.image.__str__() != '':
            return '<img src="/media/%s" width="100" height="100" />' % (self.image)

    image_thumb.allow_tags = True

    def __str__(self):
        return self.title

class BannerImageAdmin(SortableModelAdmin):
    fields = ['title','image', 'image_thumb']
    list_display = ['title','image_thumb']
    readonly_fields = ['image_thumb']
    sortable = 'order'

class CruiseDeal(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField()
    expire_date = models.DateField()
    url = models.URLField(default='')
    cruise_line = models.ForeignKey(CruiseLine, null=True, on_delete=models.CASCADE)
    show_in_home = models.BooleanField(default=1, verbose_name='Show in Homepage')

    def image_thumb(self):
        if self.cruise_line.logo.__str__() != '':
            return '<img src="http://www.cruiseplanners.com{logo}" width="100" height="100" />'.format(logo=self.cruise_line.logo)

    image_thumb.allow_tags = True

    def __str__(self):
        return self.title


class CruiseDealForm(forms.ModelForm):
    class Meta:
        model = CruiseDeal
        fields = ('description',)
        widgets = {
            'description': RedactorWidget(editor_options={'lang': 'en'})
        }


class CruiseDealAdmin(SortableModelAdmin):
    fields = ('title','description', 'expire_date', 'url', 'cruise_line', 'show_in_home')
    list_display = ['title','image_thumb', 'expire_date', 'show_in_home']
    list_editable = ('show_in_home',)
    readonly_fields = ['image_thumb']
    form = CruiseDealForm
    sortable = 'order'


class TopDestination(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads', help_text='The image dimension should be 375x239')
    destination = models.ForeignKey(SubRegion, null=True, blank=True)
    order = models.PositiveIntegerField()

    def image_thumb(self):
        if self.image.__str__() != '':
            return '<img src="/media/%s" width="100" height="100" />' % (self.image)

    image_thumb.allow_tags = True

    def __str__(self):
        return self.title

class TopDestinationAdmin(SortableModelAdmin):
    fields = ('title','image', 'destination')
    list_display = ['title','image_thumb', 'destination']
    readonly_fields = ['image_thumb']
    sortable = 'order'


admin.site.register(BannerImage, BannerImageAdmin)
admin.site.register(CruiseDeal, CruiseDealAdmin)
admin.site.register(TopDestination, TopDestinationAdmin)