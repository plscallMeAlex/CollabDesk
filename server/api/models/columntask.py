from django.db import models

class ColumnTask(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    row_index = models.IntegerField()
    bulletin_column = models.ForeignKey('BulletinColumn', on_delete=models.CASCADE)