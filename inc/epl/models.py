from django.db import models

# Create your models here.
class EPL(models.Model):
    appname = models.CharField(default="",max_length=20)
    name = models.TextField(default="")
    color = models.CharField(default="63,178,255",max_length=15)
    logo = models.FileField(upload_to="epl/")
    comment = models.TextField(default="")
    cover = models.FileField(upload_to="epl/")
    quickstart = models.TextField(default="",null=True,blank=True)
    meaning = models.TextField(default="")

    class Meta:
        verbose_name_plural = "1.EPL(EPL)"

    def __str__(self):
        return '[%d] %s : %s' % (self.id, self.name, self.appname)

    def get_specs(self):
        return EPLSpec.objects.filter(epl=self)

    def get_images(self):
        return EPLImage.objects.filter(epl=self)


class EPLSpec(models.Model):
    epl = models.ForeignKey(EPL)
    xi = models.CharField(max_length=30)
    title = models.TextField(default="")
    contents = models.TextField(default="")

    class Meta:
        verbose_name_plural = "2.특징(EPLSpec)"

    def __str__(self):
        return '[%d] %s : %s' % (self.id, self.epl, self.title)


class EPLImage(models.Model):
    epl = models.ForeignKey(EPL)
    src = models.FileField(upload_to="epl/")

    class Meta:
        verbose_name_plural = "3.스크린샷(EPLImage)"

    def __str__(self):
        return '[%d] %s : %s' % (self.id, self.epl, self.src)