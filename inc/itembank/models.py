from django.contrib.auth.models import User
from django.db import models


# Create your models here.
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


class Question(models.Model):
    user = models.ForeignKey(User)
    unit = models.ForeignKey(Unit3)
    title = models.TextField(default="")
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "4.문제(Question)"

    def __str__(self):
        return '[%d] %s : %s' % (self.id, self.title, self.is_active)

    def get_contents(self):
        return Content.objects.filter(question=self)


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
            return ChoiceItem.objects.filter(content=self)
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