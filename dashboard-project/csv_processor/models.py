from django.db import models
from dataset_importer.models import Importer

# Create your models here.
class CsvFile(Importer):
    filename = models.CharField(max_length=1024)