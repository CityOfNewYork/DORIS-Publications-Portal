from django.db import models
class Document(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    date_created = models.DateField(null=False)
    filename = models.CharField(max_length=255, null=False)
    common_id = models.IntegerField(default=None, null=True)
    section_id = models.IntegerField(default=None, null=True)
    num_access = models.IntegerField(default=0, null=False)
    agency = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=False)
    pub_or_foil = models.CharField(max_length=20, null=False)
    docText = models.TextField(null=True)

    def __unicode__(self):
        return self.title