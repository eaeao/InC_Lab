import os

from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.db import models

# Create your models here.
from django.utils.dateformat import DateFormat
from django.utils.html import strip_tags

admin_index = 1

GRADE_IN_SCHOOL_CHOICES = (
    (0, '초등학교'),
    (1, '중학교'),
    (2, '고등학교'),
    (3, '대학교'),
    (4, '기타'),
)

class UserSchool(models.Model):
    user = models.OneToOneField(User,related_name="school")
    grade = models.IntegerField(choices=GRADE_IN_SCHOOL_CHOICES, default=0)
    school = models.TextField(default="")
    year = models.IntegerField(default=1)
    div = models.TextField(default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = "%d.소속 학교(UserSchool)"%(admin_index)

    def __str__(self):
        return '[%d] %s' %(self.id,self.user.first_name)

GRADE_IN_PROFILE_CHOICES = (
    (0, '일반'),
    (1, '학생'),
    (2, '교사'),
)

GENDER_IN_PROFILE_CHOICES = (
    (0, '남자'),
    (1, '여자'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="profile")
    grade = models.IntegerField(choices=GRADE_IN_PROFILE_CHOICES, default=0)
    gender = models.IntegerField(choices=GENDER_IN_PROFILE_CHOICES, default=0)
    src = models.FileField(upload_to="upload/",null=True,blank=True)

    def __str__(self):
        return '[%d] %s' %(self.id,self.user.first_name)

    def get_grade(self):
        return "%s" % GRADE_IN_PROFILE_CHOICES[self.grade][1]

    def get_gender(self):
        return "%s" % GENDER_IN_PROFILE_CHOICES[self.gender][1]


MODE_IN_MENU_CHOICES = (
    (0, '외부링크'),
    (1, '페이지'),
    (2, '일반게시판'),
    (3, '웹진게시판'),
    (4, '갤러리'),
    (5, '자료실'),
    (6, 'EPL'),
)


class Menu(models.Model):
    parent = models.ForeignKey('self',blank=True,null=True)
    order = models.IntegerField(default=1)
    title = models.TextField(default="")
    title_en = models.TextField(default="",blank=True,null=True)
    title_jp = models.TextField(default="", blank=True, null=True)
    mode = models.IntegerField(choices=MODE_IN_MENU_CHOICES)
    url = models.TextField(default="",blank=True,null=True)
    appname = models.TextField(default="")
    is_blank = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "%d.메뉴(Menu)"%(admin_index+1)

    def __str__(self):
        return '[%d]%s > %s (%s) %s' % (self.id, self.parent, self.title, MODE_IN_MENU_CHOICES[self.mode][1], self.is_active)

    def get_parent(self):
        if self.parent :
            return  '%s > %s' % (self.parent.get_parent(), self.title)
        else :
            return '메인'

    def get_sub(self):
        return Menu.objects.filter(parent=self,is_active=True).order_by('order')

    def get_page(self):
        return get_or_none(Page, menu=self)

    def get_boards(self):
        return Board.objects.filter(menu=self).order_by('-date_updated')

    def get_url(self):
        if self.mode == 0 :
            return self.url
        else :
            return "/menu/%d"%self.id

    def get_blank(self):
        if self.is_blank :
            return "_blank"
        return "_self"


class Page(models.Model):
    menu = models.ForeignKey(Menu)
    user = models.ForeignKey(User)
    contents = models.TextField(default="", blank=True, null=True)
    contents_en = models.TextField(default="", blank=True, null=True)
    contents_jp = models.TextField(default="", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "%d.페이지(Page)"%(admin_index+2)

    def __str__(self):
        return '[%d]%s by %s' % (self.id, self.menu, self.user)


TYPE_IN_PAPER_CHOICES = (
    (0, 'International Journal'),
    (1, 'International Conference'),
    (2, 'Domestic Journal'),
    (3, 'Domestic Conference'),
)


class DocPaper(models.Model):
    type = models.IntegerField(default=0,choices=TYPE_IN_PAPER_CHOICES)
    user = models.ForeignKey(User)
    author = models.TextField(default="")
    title = models.TextField(default="")
    journal = models.TextField(default="")
    volume = models.TextField(default="",null=True,blank=True)
    number = models.TextField(default="",null=True,blank=True)
    page  = models.TextField(default="",null=True,blank=True)
    date_publication = models.DateField()
    link = models.TextField(default="",blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "%d.논문(DocPaper)"%(admin_index+3)

    def __str__(self):
        return '%s, (%s). %s. %s, %s.' % (self.author, DateFormat(self.date_publication).format('Y'), self.title, self.journal, self.page)


class DocBook(models.Model):
    user = models.ForeignKey(User)
    author = models.TextField(default="")
    title = models.TextField(default="")
    publisher = models.TextField(default="")
    date_publication = models.DateField()
    link = models.TextField(default="",blank=True,null=True)
    cover = models.FileField(upload_to="upload/",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "%d.저서(DocBook)"%(admin_index+4)

    def __str__(self):
        return '%s, (%s). %s. %s.' % (self.author, DateFormat(self.date_publication).format('Y'), self.title, self.publisher)

    def get_cover(self):
        if self.cover :
            return self.cover.url
        return None


class Board(models.Model):
    menu = models.ForeignKey(Menu)
    user = models.ForeignKey(User)
    title = models.TextField()
    con = models.TextField()
    hits = models.IntegerField(default=0)
    is_headline = models.BooleanField(default=False)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "%d.게시물(Board)"%(admin_index+5)

    def get_reply(self):
        return BoardReply.objects.filter(board=self)

    def get_files(self):
        return BoardFile.objects.filter(board=self)

    @property
    def get_con(self):
        con = self.con
        con = con.replace(find_between(con, "<style>", "</style>"),"")
        con = strip_tags(con)
        for i in range(0,10) :
            con = con.replace("{{%d}}"%i, "")
        if con.__len__() > 1500 :
            con = "%s..."%con[:1500]
        return con

    def __str__(self):
        return '[%d] (%s)%s' %(self.id,self.menu,self.title)


class BoardFile(models.Model):
    board = models.ForeignKey(Board)
    src = models.FileField(upload_to="upload/")
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return '[%d] %s > %s' %(self.id, self.board, self.src)

    class Meta:
        verbose_name_plural = "%d.게시물 파일(BoardFile)"%(admin_index+6)

    def get_name(self):
        return os.path.basename(self.src.name)

    def get_size(self):
        size = self.src.size
        if size < 1000 :
            return "%.2f B"%(size * 1.0 )
        elif size < 1000000 :
            return "%.2f KB"%(size / 1000.0)
        elif size < 1000000000:
            return "%.2f MB" % (size / 1000000.0)


class BoardReply(models.Model):
    board = models.ForeignKey(Board)
    user = models.ForeignKey(User)
    con = models.TextField(max_length=200)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "%d.게시물 댓글(BoardReply)"%(admin_index+7)

    def __str__(self):
        return '[%d] (%s)%s:%s' %(self.id,self.board,self.user,self.con)



def get_or_none(model,order=None, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except MultipleObjectsReturned as e:
        if order == "-":
            res = model.objects.filter(**kwargs).order_by("-id")
        else :
            res = model.objects.filter(**kwargs).order_by("id")
        if res:
            return res[0]
        return None
    except Exception as e:
        return None


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""