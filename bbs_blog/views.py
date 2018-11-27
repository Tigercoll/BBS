from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
# Create your views here.
from bbs_blog import forms
from django.views import View

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
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        login_name = request.POST.get("login_name")
        nick_name = request.POST.get("nick_name")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        header_img = request.FILES.get("header_img")
        print(email,phone,login_name,nick_name,password,re_password,header_img)




        return HttpResponse("ok")
















class UpLoad(View):
    def get(self,request):
        return  render(request,'upload.html')

    def post(self,request):
        files_obj = request.FILES.get('img_head')
        with open('static/%s'%files_obj.name,'wb') as f:
            for chunk in files_obj.chunks():
                f.write(chunk)
        return HttpResponse('上传成功')

