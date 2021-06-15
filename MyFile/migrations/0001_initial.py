# Generated by Django 3.2.3 on 2021-06-02 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyRead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_operator', models.CharField(editable=False, max_length=30, null=True, verbose_name='修改者')),
                ('change_time', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
                ('create_operator', models.CharField(editable=False, max_length=30, null=True, verbose_name='创建者')),
                ('create_time', models.DateTimeField(auto_now=True, null=True, verbose_name='创建时间')),
                ('delete_operator', models.CharField(editable=False, max_length=30, null=True, verbose_name='删除者')),
                ('delete_time', models.DateTimeField(editable=False, null=True, verbose_name='删除时间')),
                ('status', models.SmallIntegerField(default=0, editable=False, null=True, verbose_name='状态')),
                ('file', models.FileField(upload_to='', verbose_name='生成的html文件')),
            ],
            options={
                'ordering': ['-change_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_operator', models.CharField(editable=False, max_length=30, null=True, verbose_name='修改者')),
                ('change_time', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
                ('create_operator', models.CharField(editable=False, max_length=30, null=True, verbose_name='创建者')),
                ('create_time', models.DateTimeField(auto_now=True, null=True, verbose_name='创建时间')),
                ('delete_operator', models.CharField(editable=False, max_length=30, null=True, verbose_name='删除者')),
                ('delete_time', models.DateTimeField(editable=False, null=True, verbose_name='删除时间')),
                ('status', models.SmallIntegerField(default=0, editable=False, null=True, verbose_name='状态')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='文件名')),
                ('file', models.FileField(upload_to='', verbose_name='文件')),
                ('remark', models.TextField(verbose_name='备注')),
                ('readed_html', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MyFile.myread')),
            ],
            options={
                'ordering': ['-change_time'],
                'abstract': False,
            },
        ),
    ]