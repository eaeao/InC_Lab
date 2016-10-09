from django.contrib import admin

from inc.itembank.models import Unit1, Unit2, Unit3, Question, Content, ChoiceItem, ImageItem, TestpaperQuestion, \
    TestpaperQuestionChoiceItem, Testpaper, TestpaperQuestionResult, TestpaperResult


class Unit1Admin(admin.ModelAdmin):
    list_display = ('id','title')


class Unit2Admin(admin.ModelAdmin):
    list_display = ('id','unit','title')


class Unit3Admin(admin.ModelAdmin):
    list_display = ('id', 'unit', 'title')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'unit', 'type', 'title','src','date_created', 'is_active')


class ChoiceItemInline(admin.StackedInline):
    model = ChoiceItem
    can_delete = True


class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'type', 'contents')
    inlines = [ChoiceItemInline]


class ChoiceItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'text')


class ImageItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'src')


class TestpaperQuestionChoiceItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'testpaper_question', 'choice_item')


class TestpaperQuestionChoiceItemInline(admin.StackedInline):
    model = TestpaperQuestionChoiceItem
    can_delete = True


class TestpaperQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'testpaper', 'question')
    inlines = [TestpaperQuestionChoiceItemInline]


class TestpaperQuestionInline(admin.StackedInline):
    model = TestpaperQuestion
    can_delete = True


class TestpaperAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'date_created', 'is_active')
    inlines = [TestpaperQuestionInline]


class TestpaperQuestionResultInline(admin.StackedInline):
    model = TestpaperQuestionResult
    can_delete = True


class TestpaperResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'testpaper', 'school', 'year' ,'div', 'date_created')
    inlines = [TestpaperQuestionResultInline]


class TestpaperQuestionResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'testpaper_result', 'testpaper_question', 'answer')


admin.site.register(Unit1, Unit1Admin)
admin.site.register(Unit2, Unit2Admin)
admin.site.register(Unit3, Unit3Admin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(ChoiceItem, ChoiceItemAdmin)
admin.site.register(ImageItem, ImageItemAdmin)
admin.site.register(Testpaper, TestpaperAdmin)
admin.site.register(TestpaperQuestion, TestpaperQuestionAdmin)
admin.site.register(TestpaperQuestionChoiceItem, TestpaperQuestionChoiceItemAdmin)
admin.site.register(TestpaperResult, TestpaperResultAdmin)
admin.site.register(TestpaperQuestionResult, TestpaperQuestionResultAdmin)