from django.db import models

# Create your models here.
class GlossaryContent(models.Model):
    language = models.IntegerField()
    page_field = models.IntegerField()
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'glossary_content'


class GlossaryField(models.Model):
    page_field = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'glossary_field'


class GlossaryLanguage(models.Model):
    language = models.TextField()
    language_full = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'glossary_language'
