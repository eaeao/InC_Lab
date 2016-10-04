from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class EvaluationQuestion(models.Model):
    user = models.ForeignKey(User)
    title = models.TextField(default="")
    content = models.TextField(default="")
    result_exec = models.TextField(default="")
    source_exec = models.TextField(default="")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "1.프로그래밍 평가 문제(EvaluationQuestion)"

    def __str__(self):
        return '[%d] %s > %s' % (self.id, self.title, self.content)

    def get_cases(self):
        return EvaluationQuestionInputCase.objects.filter(question=self)


class EvaluationQuestionInputCase(models.Model):
    question = models.ForeignKey(EvaluationQuestion)
    case = models.TextField(default="")

    class Meta:
        verbose_name_plural = "2.프로그래밍 평가 문제 입력 케이스(EvaluationQuestionInputCase)"

    def __str__(self):
        return '[%d] %s :: %s' % (self.id, self.question, self.case)

class EvaluationRecord(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(EvaluationQuestion)
    source_exec = models.TextField(default="")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "3.프로그래밍 평가 기록(EvaluationRecord)"

    def __str__(self):
        return '[%d] %s : %s' % (self.id, self.user, self.question)