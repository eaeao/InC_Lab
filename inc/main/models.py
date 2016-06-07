from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.db import models

# Create your models here.
GRADE_IN_PROFILE_CHOICES = (
    (0, '학생'),
    (1, '교사')
)

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="profile")
    grade = models.IntegerField(choices=GRADE_IN_PROFILE_CHOICES, default=0)
    src = models.FileField(upload_to="upload/",null=True,blank=True)

    def __str__(self):
        return '[%d] %s' %(self.id,self.user.first_name)

    def get_grade(self):
        return "%s" % GRADE_IN_PROFILE_CHOICES[self.grade][1]


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