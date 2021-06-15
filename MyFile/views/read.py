# -*- coding: utf-8 -*-
import json
import traceback
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import subprocess
import os
import traceback
from MyFile.models import UploadFile, MyWord
import urllib
import importlib, sys

importlib.reload(sys)
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


def parse(DataIO, save_path):
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(DataIO)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 分析器和文档相互连接
    parser.set_document(doc)
    doc.set_parser(parser)
    # 提供初始化密码，没有默认为空
    doc.initialize()
    # 检查文档是否可以转成TXT，如果不可以就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF资源管理器，来管理共享资源
        rsrcmagr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        # 将资源管理器和设备对象聚合
        device = PDFPageAggregator(rsrcmagr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmagr, device)

        # 循环遍历列表，每次处理一个page内容
        # doc.get_pages()获取page列表

        text = ''
        for page in doc.get_pages():
            interpreter.process_page(page)
            # 接收该页面的LTPage对象
            layout = device.get_result()
            # 这里的layout是一个LTPage对象 里面存放着page解析出来的各种对象
            # 一般包括LTTextBox，LTFigure，LTImage，LTTextBoxHorizontal等等一些对像
            # 想要获取文本就得获取对象的text属性
            for x in layout:
                try:
                    if (isinstance(x, LTTextBoxHorizontal)):
                        # with open('%s' % (save_path), 'a') as f:
                            result = x.get_text()
                        #     f.write(result + "\n")
                            text += f'{result}'
                except:
                    traceback.print_exc()
                    print("Failed")
        return text

read_page = 2

def reading(request, id):
    try:
        file_obj = UploadFile.objects.get(id=id)
        text = file_obj.text

        if text and text != '解析中':
            return HttpResponse(file_obj.text, headers={"Access-Control-Allow-Origin": "*"})
        path = file_obj.file.path
        with open(path, 'rb') as pdf_html:
            res = parse(pdf_html, r'd.txt')

    except Exception as e:
        import traceback
        traceback.print_exc()
        return HttpResponse(traceback.format_exc(), headers={"Access-Control-Allow-Origin": "*"})
    return HttpResponse(res, headers={"Access-Control-Allow-Origin": "*"})


def mark_save(request, id):
    try:
        file_obj = UploadFile.objects.get(id=id)
        text = request.POST.get('text')
        # print(request.body)
        file_obj.text = text
        file_obj.save()
    except Exception as e:
        import traceback
        traceback.print_exc()
        return HttpResponse(traceback.format_exc(), headers={"Access-Control-Allow-Origin": "*"})
    return HttpResponse('ok', headers={"Access-Control-Allow-Origin": "*"})


def search_word(request, id):
    text = request.POST.get('text', None)
    print(text)

    from ECDICT.stardict import StarDict
    MyDict = StarDict('D:\\any_code\EnglishRBB\ECDICT\stardict.db')
    res = MyDict.query(text.strip())
    print(res)

    return JsonResponse({
        'result': res,
        'status': 'ok'
    }, headers={"Access-Control-Allow-Origin": "*"})

def word_save(request, id):
    """

    :param request:
    :param id:
    :return:
    """
    try:
        text = request.POST.get('text', None)
        if not text:
            return JsonResponse({
                'status': 'error'
            }, headers={"Access-Control-Allow-Origin": "*"})
        MyWord.objects.update_or_create(name=text.strip(), file_id=id)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return HttpResponse(traceback.format_exc(), headers={"Access-Control-Allow-Origin": "*"})
    return HttpResponse('ok', headers={"Access-Control-Allow-Origin": "*"})


def word_del(request, id):
    """

    :param request:
    :param id:
    :return:
    """
    try:
        file_obj = UploadFile.objects.get(id=id)
        text = request.POST.get('text')
        # print(request.body)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return HttpResponse(traceback.format_exc(), headers={"Access-Control-Allow-Origin": "*"})
    return HttpResponse('ok', headers={"Access-Control-Allow-Origin": "*"})

def get_trans(request, id):
    try:
        from ECDICT.stardict import StarDict
        MyDict = StarDict('D:\\any_code\EnglishRBB\ECDICT\stardict.db')
        words = MyWord.objects.filter(file_id=id).values_list('name', flat=True)  # values_list('number', flat=True)
        res = MyDict.query_batch(list(words))
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(traceback.format_exc(), headers={"Access-Control-Allow-Origin": "*"})
    return JsonResponse({
        'result': res,
        'status': 'ok'
    }, headers={"Access-Control-Allow-Origin": "*"})


def get_words(request, id):
    try:
        words = MyWord.objects.filter(file_id=id).values_list('name', flat=True)  # values_list('number', flat=True)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(traceback.format_exc(), headers={"Access-Control-Allow-Origin": "*"})
    return JsonResponse({
        'result': list(words),
        'status': 'ok'
    }, headers={"Access-Control-Allow-Origin": "*"})

def pdf2html(file_obj):
    html_name = f'{file_obj.name}.html'
    file_path = file_obj.file.path
    temp_path = f'{settings.BASE_DIR}/MyFile/templates'
    pdf2htmlEx_path = f'{settings.BASE_DIR}/pdf2htmlEX/pdf2htmlex'
    if not os.path.exists(f'{temp_path}/{html_name}'):
        cmd = f'{pdf2htmlEx_path} --dest-dir {temp_path}  {file_path} {html_name}'
        res = subprocess.run(cmd)

    return


# def read_pdf(file_obj):
#     path = file_obj.file.path
#     with pdfplumber.open(path) as pdf:
#         page_index = read_page - 1
#         for i in range(page_index):
#             page = pdf.pages[i]
#             chars = page.chars
#             for char in chars:
#                 print(char['text'])



