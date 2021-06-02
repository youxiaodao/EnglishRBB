from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import subprocess
import os

from MyFile.models import UploadFile
# Create your views here.


def reading(request, id):
    try:
        file_obj = UploadFile.objects.get(id=id)
        file_path = file_obj.file.path
        html_name = f'{file_obj.name}.html'
        temp_path = f'{settings.BASE_DIR}/MyFile/templates'
        pdf2htmlEx_path = f'{settings.BASE_DIR}/pdf2htmlEX/pdf2htmlex'
        if not os.path.exists(f'{temp_path}/{html_name}'):
            cmd = f'{pdf2htmlEx_path} --dest-dir {temp_path}  {file_path} {html_name}'
            res = subprocess.run(cmd)
            print(res)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return HttpResponse(traceback.format_exc())
    return render(request, f'{file_obj.name}.html')