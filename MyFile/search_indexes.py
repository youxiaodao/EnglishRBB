# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   Project        EnglishRBB
   File Name:     search_indexes
   Description :  
   Author :       Xdao
   date:          2021-06-27 15:03
-------------------------------------------------
                  
"""
from haystack import indexes  # 导入索引

from MyFile import models   # 导入模型表


class FileIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    # document:使用文档建立索引字段　　　　
    # use_template:使用模板语法

    def get_model(self):  # 为那个模型表建立索引

        return models.UploadFile

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
