from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
# Create your views here.
from bbs_blog import forms
from django.views import View

import  re
from django.contrib import auth
class LoginView(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user:
            auth.login(request,user)
            return redirect('/index/')
        else:
            return render(request,'login.html',context={'msg':'用户名或密码错误'})

class LogoutView(View):
    def get(self,request):
        auth.logout(request)
        return redirect('/login/')




class IndexView(View):
    def get(self,request):
        return render(request,'index.html')



class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        data = {'status':'','error':{}}
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        login_name = request.POST.get("login_name")
        nick_name = request.POST.get("nick_name")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        header_img = request.FILES.get("header_img")
        print(email,phone,login_name,nick_name,password,re_password,header_img)

        # 判断邮箱格式是否正确
        if email :
            if '@' not  in email:
                data['status'] = 1
                data['error']['email_error'] = '邮箱格式不正确'
        else:
            data['status'] = 1
            data['error']['email_error'] = '邮箱不能为空'

        # 判断手机格式是否正确
        if phone :
            pattern = r"^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$"
            searchObj = re.search(pattern,phone)
            if not searchObj:
                data['status'] = 1
                data['error']['phone_error'] = '手机格式不正确'
        else:
            data['status'] = 1
            data['error']['phone_error'] = '手机不能为空'

        # 判断登录名
        if login_name:
            if len(login_name)<6:
                data['status'] = 1
                data['error']['login_name_error'] = '登录名不能少于6位'
        else:
            data['status'] = 1
            data['error']['login_name_error'] = '登录名不能为空'

        #判断昵称
        if nick_name :
            if len(nick_name)<2:
                data['status'] = 1
                data['error']['nick_name_error'] = '昵称不能少于2位'
        else:
            data['status'] = 1
            data['error']['login_name_error'] = '昵称不能为空'

        if password:
            if len(password)<8:
                data['status'] = 1
                data['error']['password_error'] = '密码不能少于2位'
        else:
            data['status'] = 1
            data['error']['password_error'] = '密码不能为空'

        if password != re_password:
            data['status'] = 1
            data['error']['password_error'] = '两次密码不一致'

        print(data)
        import json
        return JsonResponse(data)
















class UpLoad(View):
    def get(self,request):
        return  render(request,'upload.html')

    def post(self,request):
        files_obj = request.FILES.get('img_head')
        with open('static/%s'%files_obj.name,'wb') as f:
            for chunk in files_obj.chunks():
                f.write(chunk)
        return HttpResponse('上传成功')

