from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from MyFile.models import UploadFile, MyRead
class FileAdmin(admin.ModelAdmin):
    list_display = ['name', 'go_reading']
    search_fields = ['name']

    def go_reading(self, obj):
        return mark_safe(u'<a href="/read/%s" target="_blank">%s</a' % (obj.id, "开始阅读"))

    go_reading.short_description = '开始阅读'
    go_reading.allow_tags = True
# Register your models here.

admin.site.register(UploadFile, FileAdmin)
admin.site.register(MyRead)