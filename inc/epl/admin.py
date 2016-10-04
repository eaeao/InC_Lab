from django.contrib import admin

# Register your models here.
from inc.epl.models import EPL, EPLSpec, EPLImage


class EPLSpecInline(admin.StackedInline):
    model = EPLSpec
    can_delete = True


class EPLImageInline(admin.StackedInline):
    model = EPLImage
    can_delete = True


class EPLAdmin(admin.ModelAdmin):
    list_display = ('id','appname','name','color','logo','comment','cover','quickstart')
    inlines = [EPLSpecInline, EPLImageInline]


class EPLSpecAdmin(admin.ModelAdmin):
    list_display = ('id','epl','xi','title')


class EPLImageAdmin(admin.ModelAdmin):
    list_display = ('id','epl','src')

admin.site.register(EPL, EPLAdmin)
admin.site.register(EPLSpec, EPLSpecAdmin)
admin.site.register(EPLImage, EPLImageAdmin)