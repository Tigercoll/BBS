from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
# Create your views here.
from geetest import GeetestLib
from django.db.models import Count
from bbs_blog import forms
from django.views import View
from bbs_blog.models import UserInfo, Article

from django.conf import settings

import datetime
import re
from django.contrib import auth

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


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
        category_list = article_list.values('category__name').annotate(
            count=Count('category__name')).values('category__name', 'count')
        tag_list = article_list.values('tag__name').annotate( count=Count('tag__name')).values('tag__name', 'count')
        archive_list = []
        archive = article_list.dates('create_time','month',order='DESC')
        for i in archive:
            archive_count=article_list.filter(create_time__year=i.year,create_time__month=i.month).count()
            archive_list.append([i,archive_count])
        print(archive_list)



        return render(
            request,
            'home.html',
            {
                'article_list': article_list,
                'user': user,
                'category_list': category_list,
                'tag_list':tag_list,
                'archive_list':archive_list
            }
        )
