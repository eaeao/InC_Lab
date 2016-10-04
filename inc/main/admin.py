from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from inc.main.models import UserProfile, Menu, Page, DocPaper, BoardFile, Board, BoardReply, DocBook, UserSchool, \
    get_or_none


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = True


class UserSchoolInline(admin.StackedInline):
    model = UserSchool
    max_num = 1
    can_delete = True


class UserSchoolAdmin(admin.ModelAdmin):
    list_display = ('id','user','grade','school','year','div')


class UserAdmin(UserAdmin):
    list_display = ('id','username','first_name','성별','last_login','date_joined')
    inlines = [UserProfileInline, UserSchoolInline]
    ordering = ('-id',)

    def 성별(self, instance):
        if instance.profile.gender == 0: return u"남자"
        return u"여자"


class MenuAdmin(admin.ModelAdmin):
    list_display = ('id','parent','order','title','title_en','title_jp','url','mode','is_blank','is_active')
    ordering = ('parent','order','-id')


class PageAdmin(admin.ModelAdmin):
    list_display = ('id','menu','user','date_created')
    ordering = ('-menu',)


class BoardImgInline(admin.StackedInline):
    model = BoardFile
    can_delete = True


class BoardAdmin(admin.ModelAdmin):
    list_display = ('id','menu','user','title','con','hits','is_headline','date_updated')
    readonly_fields = ('hits',)
    inlines = [BoardImgInline]


class BoardReplyAdmin(admin.ModelAdmin):
    list_display = ('id','board','user','con','date_updated')


class BoardFileAdmin(admin.ModelAdmin):
    list_display = ('id','board','src','is_visible')


class DocPaperAdmin(admin.ModelAdmin):
    list_display = ('id','user','type','author','title','journal','volume','number','page','date_publication','date_created')
    ordering = ('-id',)


class DocBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author', 'title', 'publisher', 'cover', 'date_publication', 'date_created')
    ordering = ('-id',)


def user_new_str(self):
    return "%s (%s)"%(self.first_name, self.email)

def get_school(self):
    return get_or_none(UserSchool, user=self)

User.__str__ = user_new_str
User.get_school = get_school

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserSchool, UserSchoolAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BoardReply, BoardReplyAdmin)
admin.site.register(BoardFile, BoardFileAdmin)
admin.site.register(DocPaper, DocPaperAdmin)
admin.site.register(DocBook, DocBookAdmin)