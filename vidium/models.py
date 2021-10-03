from django.db import models

# Create your models here.
class Gene(models.Model):
    chrom = models.CharField(max_length=200)
    pos = models.IntegerField()
    ref = models.CharField(max_length=10)
    alt = models.CharField(max_length=200)
    filter = models.CharField(max_length=200)
    af = models.FloatField()
    vf = models.FloatField()
    dp = models.IntegerField()
    allele = models.CharField(max_length=200)
    effect = models.CharField(max_length=200)
    impact = models.CharField(max_length=200)
    gene = models.CharField(max_length=200)