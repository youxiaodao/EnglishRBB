import os
from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from MyFile.models import UploadFile, MyRead
class FileAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_operator', 'create_time', 'go_reading']
    search_fields = ['name']
    # def save_model(self, request, obj, form, change):
    #     print(obj)
    #     print(dir(obj))
    #     print(request.FILES)  # <MultiValueDict: {'file': [<InMemoryUploadedFile: 123.txt (text/plain)>]}>
    #     from django.core.files.uploadedfile import InMemoryUploadedFile
    #     file_name = request.FILES['file'][0].name
    #     print(file_name)
    #     print(dir(request.FILES))
    #     # ext = os.path.splitext()

    def go_reading(self, obj):
        return mark_safe(u'<a href="http://127.0.0.1:8081/?%s" target="_blank">%s</a' % (obj.id, "开始阅读"))

    go_reading.short_description = '开始阅读'
    go_reading.allow_tags = True
# Register your models here.

admin.site.register(UploadFile, FileAdmin)
# admin.site.register(MyRead)