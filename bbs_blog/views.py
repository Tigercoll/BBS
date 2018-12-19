from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
# Create your views here.
from geetest import GeetestLib
from django.db.models import Count
from bbs_blog import forms
from django.views import View
from bbs_blog.models import UserInfo, Article,ArticleFavour,Comment

from django.conf import settings

import datetime
import re
from django.contrib import auth

from django.db.models import F
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
import json
import base64
import urllib.parse
import requests
import qrcode

import cx_Oracle
class LoginView(View):
    def get(self, request):
        return render(request, 'login2.html')

    def post(self, request):
        data = {'stutas': 0, 'error': {}}
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        print(username)
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            user = auth.authenticate(username=username, password=password)
            if user:
                if remember:
                    aweek = 60 * 60 * 12 * 7
                    request.session.set_expiry(aweek)
                else:
                    request.session.set_expiry(0)
                auth.login(request, user)
                data['url'] = '/index/'
                return JsonResponse(data)
            else:
                data['status'] = 1
                data['error'] = '用户名或密码错误'
                return JsonResponse(data)
        else:
            data['status'] = 1
            data['error'] = '验证码错误'
            return JsonResponse(data)


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('/login/')


def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


class IndexView(View):
    def get(self, request):
        article_list = Article.objects.all()
        return render(request, 'index.html', {'article_list': article_list})


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        data = {'status': 0, 'error': {}}
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        login_name = request.POST.get("login_name")
        nick_name = request.POST.get("nick_name")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        header_img = request.FILES.get("header_img")
        print(email, phone, login_name, nick_name, password, re_password, header_img)

        # 判断邮箱格式是否正确
        if email:
            if '@' not in email:
                data['status'] = 1
                data['error']['email_error'] = '邮箱格式不正确'
            else:
                email_obj = UserInfo.objects.filter(email=email)
                if email_obj:
                    data['status'] = 1
                    data['error']['email_error'] = '邮箱已被注册'
        else:
            data['status'] = 1
            data['error']['email_error'] = '邮箱不能为空'

        # 判断手机格式是否正确
        if phone:
            pattern = r"^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$"
            searchObj = re.search(pattern, phone)
            if not searchObj:
                data['status'] = 1
                data['error']['phone_error'] = '手机格式不正确'
            else:
                phone_obj = UserInfo.objects.filter(phone=phone)
                if phone_obj:
                    data['status'] = 1
                    data['error']['phone_error'] = '手机号已被注册'
        else:
            data['status'] = 1
            data['error']['phone_error'] = '手机不能为空'

        # 判断登录名
        if login_name:
            if len(login_name) < 4:
                data['status'] = 1
                data['error']['login_name_error'] = '登录名不能少于4位'
            else:
                login_name_obj = UserInfo.objects.filter(username=login_name)
                if login_name_obj:
                    data['status'] = 1
                    data['error']['login_name_error'] = '登录名已被注册'
        else:
            data['status'] = 1
            data['error']['login_name_error'] = '登录名不能为空'

        # 判断昵称
        if nick_name:
            if len(nick_name) < 2:
                data['status'] = 1
                data['error']['nick_name_error'] = '昵称不能少于2位'
        else:
            data['status'] = 1
            data['error']['nick_name_error'] = '昵称不能为空'

        if password:
            if len(password) < 8:
                data['status'] = 1
                data['error']['password_error'] = '密码不能少于8位'
        else:
            data['status'] = 1
            data['error']['password_error'] = '密码不能为空'

        if password != re_password:
            data['status'] = 1
            data['error']['re_password_error'] = '两次密码不一致'

        if data['status'] == 0:
            try:
                UserInfo.objects.create_user(username=login_name, password=password, email=email, phone=phone,
                                             nick_name=nick_name, avatar=header_img)
                data['url'] = '/login/'
            except Exception as e:
                data['status'] = 2
                data['error']['unknown'] = '%s' % e
        return JsonResponse(data)


class UpLoad(View):
    def get(self, request):
        return render(request, 'upload.html')

    def post(self, request):
        files_obj = request.FILES.get('img_head')
        with open('static/%s' % files_obj.name, 'wb') as f:
            for chunk in files_obj.chunks():
                f.write(chunk)
        return HttpResponse('上传成功')


class HomeView(View):
    def get(self, request, username):
        print(username)

        user = UserInfo.objects.filter(username=username).first()
        if not user:
            return HttpResponse('ok')
        article_list = Article.objects.filter(author=user)
        return render(
            request,
            'home.html',
            {
                'article_list': article_list,
                'user': user,
            }
        )


class ArticleDetailView(View):
    def get(self,request,username,article_id):
        print(username,article_id)
        user = UserInfo.objects.filter(username=username).first()
        if not user:
            return HttpResponse("404")
        is_up = False
        detail = Article.objects.filter(author=user,pk=int(article_id)).first()
        if  request.user.is_authenticated:
            is_up = ArticleFavour.objects.filter(article=detail, user=request.user).values('is_up').first()
        return render(request,'article-detail.html',context={'user':user,'detail':detail,'is_up':is_up})


class UpFavourView(View):
    def get(self,request):
        data = {'status':'','msg':''}
        user= request.user
        article_id = request.GET.get('article_id')
        up_favour = ArticleFavour.objects.filter(user=user,article_id=article_id).values('is_up').first()
        if not request.user.is_authenticated:
            data['status'] = 1
            data['msg'] = '请先登录'
        if up_favour:
            data['status']=2
            ArticleFavour.objects.filter(user=user, article_id=article_id).first().delete()
            Article.objects.filter(pk=article_id).update(favour_count=F("favour_count") - 1)

        else:
            ArticleFavour.objects.create(user=user,article_id=article_id)
            Article.objects.filter(pk=article_id).update(favour_count=F("favour_count") + 1)
            data['status'] = 3
        return JsonResponse(data)

class CommentListView(View):
    def get(self,request,article_id):

        ret = list(Comment.objects.filter(article_id=article_id).extra(
        select={"comment_time": "strftime('%%Y-%%m-%%d %%H:%%M:%%S',bbs_blog_comment.create_time)",
                'comment_user__avatar,comment_user__username':"select avatar,username from bbs_blog_userinfo WHERE nid =bbs_blog_comment.nid "
                }).values('comment_time','parent_comment_id','comment_user__avatar','nid','comment_user__username','content')
                   )
        return JsonResponse(ret,safe=False)

class ShowSSRView(View):

    def get(self,request):

        def base64_encode(base64_str):
            return base64.urlsafe_b64encode((bytes(base64_str, encoding='utf-8'))).decode('utf-8').replace('=', '')

        def get_uri(server):
            password = base64_encode(server['password'])
            remarks = server['server'] + ' SSR'
            group = 'Tigercoll'
            remarks = base64_encode(remarks)
            group = base64_encode(group)
            obfsparam = ''
            try:
                ssr_url = '%s:%s:%s:%s:%s:%s' % (server['server'],
                                                 server['server_port'],
                                                 server['ssr_protocol'],
                                                 server['method'],
                                                 server['obfs'],
                                                 password)

            except Exception as e:
                print('%s' % e)

                ssr_url = '%s:%s:%s:%s:%s:%s' % (server['server'],
                                                 server['server_port'],
                                                 'origin',
                                                 server['method'],
                                                 'plain',
                                                 password)
            url_back = '/?obfsparam=%s&remarks=%s&group=%s' % (obfsparam, remarks, group)
            full_ulr = ssr_url + url_back
            uri = 'ssr://' + base64_encode(full_ulr)
            print(uri)
            return uri

        response = requests.get('http://mw-ssr.herokuapp.com/full/json')
        server = response.json()
        uri = get_uri(server)
        img_file = r'static/py_qrcode.png'
        img = qrcode.make(uri)
        # 图片数据保存至本地文件
        img.save(img_file)
        return render(request,'show_ssr.html',{'uri':uri})


def  get_uplode_counts(request):

    conn = cx_Oracle.connect('PFLIS/mksoft@192.168.20.189/orcl')
    a=[]
    b={}
    with conn:
        now = datetime.date.today()
        print(now)
        cur =conn.cursor()
        sql = '''select * from PT_LIS_SQD where djrq >= TO_DATE('%s 00:28:05', 'YYYY-MM-DD HH24:MI:SS') and sqdstatus <>-2'''%now
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                a.append(row[1])
        from collections import Counter
        result = Counter(a)
        print(result)
        for k,v in result.items():
            sql_name = 'select * from PT_BASE_JGDM where jgid =:1'
            args =(str(k),)
            cur.execute(sql_name,args)
            names = cur.fetchone()
            b[names[2]]=v

    print(json.dumps(b,ensure_ascii=False))
    conn.close()
    return  JsonResponse(b)


class PushCommentView(View):
    def post(self,request):
        if request.user.is_authenticated:
            article_id = request.POST.get('article_id')
            comment_content = request.POST.get('comment_content')
            pid = request.POST.get('pid','')
            if pid:
                try:
                    index = comment_content.index('\n')
                    comment_content = comment_content[index:]
                    Comment.objects.create(article_id=article_id,content=comment_content,comment_user=request.user,parent_comment_id=pid)
                except Exception as e:
                    Comment.objects.create(article_id=article_id, content=comment_content, comment_user=request.user)
            else:
                Comment.objects.create(article_id=article_id, content=comment_content, comment_user=request.user)
            print(article_id,comment_content,pid)
            Article.objects.filter(pk=article_id).update(comment_count=F("comment_count") + 1)
            return HttpResponse('评论成功')

        else:
            return HttpResponse('非法用户')

class ArchiveListView(View):
    def get(self,request,username,year,month):
        user = UserInfo.objects.filter(username=username).first()
        Article.objects.filter(author=user).dates(create_time__year=int(year),create_time__month=int(month))
        return HttpResponse()