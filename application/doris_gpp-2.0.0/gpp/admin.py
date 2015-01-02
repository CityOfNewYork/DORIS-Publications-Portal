from django.contrib import admin
from gpp.models import Document

class DocAdmin(admin.ModelAdmin):
	list_display = ('title', 'agency', 'category', 'type', 'url')

admin.site.register(Document, DocAdmin)
