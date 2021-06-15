from django.db import models

# Create your models here.


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


class CachingModel(models.Model):
    change_operator = models.CharField(verbose_name='修改者', max_length=30, null=True,
                                       editable=False)  # who last modify
    change_time = models.DateTimeField(verbose_name='修改时间', auto_now=True, editable=False, null=True)
    create_operator = models.CharField(verbose_name='创建者', max_length=30, null=True,
                                       editable=False)  # who create this object
    create_time = models.DateTimeField(verbose_name='创建时间', editable=False, null=True,auto_now=True)
    delete_operator = models.CharField(verbose_name='删除者', max_length=30, null=True,
                                       editable=False)  # who delete this object
    delete_time = models.DateTimeField(verbose_name='删除时间', editable=False, null=True)
    status = models.SmallIntegerField(verbose_name='状态', default=0, editable=False, null=True)
    # all_objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ['-change_time']


class MyRead(CachingModel):
    file = models.FileField(verbose_name='生成的html文件')


class UploadFile(CachingModel):
    name = models.CharField(verbose_name='文件名', max_length=100, null=True, blank=True, unique=True)
    file = models.FileField(verbose_name='文件', validators=[validate_file_extension])
    remark = models.TextField(verbose_name='备注', null=True, blank=True)
    readed_html = models.ForeignKey(to=MyRead, on_delete=models.DO_NOTHING, null=True,blank=True)
    text = models.TextField(verbose_name='markdown', default='', null=True, blank=True)


class MyWord(CachingModel):
    name = models.CharField(verbose_name='单词', max_length=100, null=True, blank=True,)
    file = models.ForeignKey(verbose_name='文件', to=UploadFile, null=True, blank=True, on_delete=models.DO_NOTHING)
    mark = models.TextField(verbose_name='笔记', default='', null=True, blank=True)

