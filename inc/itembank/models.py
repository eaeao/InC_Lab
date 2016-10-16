import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from inc.main.models import get_or_none


class Unit1(models.Model):
    title = models.TextField(default="")

    class Meta:
        verbose_name_plural = "1.대단원(Unit1)"

    def __str__(self):
        return '[%d] %s' % (self.id, self.title)


class Unit2(models.Model):
    unit = models.ForeignKey(Unit1)
    title = models.TextField(default="")

    class Meta:
        verbose_name_plural = "2.중단원(Unit2)"

    def __str__(self):
        return '[%d] %s > %s' % (self.id,self.unit.title, self.title)


class Unit3(models.Model):
    unit = models.ForeignKey(Unit2)
    title = models.TextField(default="")

    class Meta:
        verbose_name_plural = "3.소단원(Unit3)"

    def __str__(self):
        return '[%d] %s > %s > %s' % (self.id, self.unit.unit.title, self.unit.title, self.title)

    def get_title(self):
        return '%s > %s > %s' % (self.unit.unit.title, self.unit.title, self.title)


TYPE_IN_QUESTION_CHOICES = (
    ('선다형', '선다형'),
    ('진위형', '진위형'),
    ('단답형', '단답형'),
    ('완성형', '완성형'),
    ('서술형', '서술형')
)


class Question(models.Model):
    user = models.ForeignKey(User)
    unit = models.ForeignKey(Unit3)
    type = models.CharField(max_length=10,choices=TYPE_IN_QUESTION_CHOICES,default='선다형')
    title = models.TextField(default="")
    keyword = models.TextField(default="",blank=True,null=True)
    src = models.FileField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "4.문제(Question)"

    def __str__(self):
        return '[%d] (%s) %s : %s' % (self.id, self.type, self.title, self.is_active)

    def get_contents(self):
        return Content.objects.filter(question=self)

    def get_answer(self):
        return self.get_contents().filter(type__in=['answer_text','answer_textarea','answer_choice']).values_list("contents",flat=True)

    def get_testpaper_question(self):
        return TestpaperQuestion.objects.filter(question=self)

    def get_results(self):
        return TestpaperQuestionResult.objects.filter(testpaper_question__question=self)

    def get_difficulty(self):
        tqr = self.get_results()
        tqr_correct = tqr.filter(answer__in=self.get_answer())
        try :
            return tqr_correct.count()/float(tqr.count())
        except Exception as e :
            return 0.0

class Content(models.Model):
    question = models.ForeignKey(Question)
    type = models.CharField(max_length=32)
    contents = models.TextField(default="")

    class Meta:
        verbose_name_plural = "5.내용(Content)"

    def __str__(self):
        return '[%d]%s, %s : %s' % (self.id, self.question.title, self.type, self.contents)

    def get_items(self):
        if self.type == "answer_choice" :
            arr = []
            for ele in ChoiceItem.objects.filter(content=self,text=self.contents) :
                arr.append(ele)
            for ele in ChoiceItem.objects.filter(Q(content=self)&~Q(text=self.contents)).order_by('?')[:3] :
                arr.append(ele)
            random.shuffle(arr)
            return arr
        elif self.type == "image" :
            return get_or_none(ImageItem,content=self)
        else:
            return None


class ChoiceItem(models.Model):
    content = models.ForeignKey(Content)
    text = models.TextField(default="")

    class Meta:
        verbose_name_plural = "6.객관식 보기(ChoiceItem)"

    def __str__(self):
        return '[%d]%s, %s' % (self.id, self.content, self.text)


class ImageItem(models.Model):
    content = models.ForeignKey(Content)
    src = models.FileField()

    class Meta:
        verbose_name_plural = "7. 보기 이미지(ImageItem)"

    def __str__(self):
        return '[%d]%s, %s' % (self.id, self.content, self.src)


class Testpaper(models.Model):
    user = models.ForeignKey(User)
    title = models.TextField(default="")
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "8. 시험지(Testpaper)"

    def __str__(self):
        return '[%d] %s: %s' % (self.id, self.user, self.title)

    def get_testpaper_questions(self):
        return TestpaperQuestion.objects.filter(testpaper=self).order_by("id")

    def get_questions(self):
        questions = self.get_testpaper_questions().values_list('question', flat=True)
        return Question.objects.filter(id__in = questions)

    def get_forms(self):
        form = []
        d = dict(TYPE_IN_QUESTION_CHOICES)
        for str_type in d.keys():
            type = self.get_questions().filter(type=str_type)
            if type :
                form.append({"type":str_type,"count":type.count()})
        return form

    def get_difficulty(self):
        tqs = TestpaperQuestion.objects.filter(testpaper=self)
        avg_tqs = 0.0
        for tq in tqs :
            avg_tqs = avg_tqs + tq.question.get_difficulty()
        try :
            return avg_tqs/float(tqs.count())
        except Exception as e :
            return 0.0

class TestpaperQuestion(models.Model):
    testpaper = models.ForeignKey(Testpaper)
    question = models.ForeignKey(Question)

    class Meta:
        verbose_name_plural = "9. 시험지 문제(TestpaperQuestion)"

    def __str__(self):
        return '[%d] %s: %s' % (self.id, self.testpaper, self.question)

    def get_contents(self):
        tmp_contents = []
        contents = self.question.get_contents()
        for content in contents:
            if content.type == "answer_choice":
                choice_items = []
                tqcs = TestpaperQuestionChoiceItem.objects.filter(testpaper_question=self)
                for tqc in tqcs:
                    choice_items.append(tqc.choice_item)
                tmp_contents.append({"type":"answer_choice","get_items":choice_items})
            else :
                tmp_contents.append(content)
        return tmp_contents

class TestpaperQuestionChoiceItem(models.Model):
    testpaper_question = models.ForeignKey(TestpaperQuestion)
    choice_item = models.ForeignKey(ChoiceItem)

    class Meta:
        verbose_name_plural = "10. 시험지 문제 객관식 보기(TestpaperQuestionChoiceItem)"

    def __str__(self):
        return '[%d] %s: %s' % (self.id, self.testpaper_question, self.choice_item)


class TestpaperResult(models.Model):
    user = models.ForeignKey(User)
    testpaper = models.ForeignKey(Testpaper)
    school = models.TextField(default="")
    year = models.IntegerField(default=1)
    div = models.TextField(default=None, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "11. 제출된 시험지(TestpaperResult)"

    def __str__(self):
        return '[%d] %s: %s' % (self.id, self.user, self.testpaper)


class TestpaperQuestionResult(models.Model):
    testpaper_result = models.ForeignKey(TestpaperResult)
    testpaper_question = models.ForeignKey(TestpaperQuestion)
    answer = models.TextField(default="")

    class Meta:
        verbose_name_plural = "12. 제출된 시험지 문제(TestpaperQuestionResult)"

    def __str__(self):
        return '[%d] %s: %s = %s' % (self.id, self.testpaper_result, self.testpaper_question, self.answer)