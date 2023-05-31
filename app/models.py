from django.db import models
from django.contrib.auth.models import User


class CV(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    professional_summary = models.TextField()


class WorkExperience(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()


class Education(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()


class Skill(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
