from django.shortcuts import render,HttpResponse

# Create your views here.

from django.views import View












class UpLoad(View):
    def get(self,request):
        return  render(request,'upload.html')

    def post(self,request):
        files_obj = request.FILES.get('img_head')
        with open('static/%s'%files_obj.name,'wb') as f:
            for chunk in files_obj.chunks():
                f.write(chunk)
        return HttpResponse('上传成功')

