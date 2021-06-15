"""EnglishRBB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from MyFile.views import read
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('read/<int:id>', read.reading),
    path('mark_save/<int:id>', read.mark_save),
    path('word_save/<int:id>', read.word_save),
    path('word_del/<int:id>', read.word_del),
    path('search_word/<int:id>', read.search_word),
    path('get_trans/<int:id>', read.get_trans),
    path('get_words/<int:id>', read.get_words),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
