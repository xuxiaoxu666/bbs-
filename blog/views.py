from django.shortcuts import render
from blog.blog_forms import User
from django.http import JsonResponse
from blog.models import UserInfo


# Create your views here.

# 注册功能
def register(request):
    form_obj = User()
    if request.method == 'GET':
        return render(request, 'register.html', {'form_obj': form_obj})
    else:
        res = {'code': 100, 'msg': '注册成功'}
        forms_obj = User(data=request.POST)
        if forms_obj.is_valid():
            register_data = forms_obj.cleaned_data
            register_data.pop('re_password')
            if request.FILES.get('icon'):
                register_data['icon'] = request.FILES.get('icon')
            UserInfo.objects.create_user(**register_data)
            return JsonResponse(res)
        else:
            res['code'] = 101
            res['msg'] = '注册失败'
            res['errors'] = forms_obj.errors
            return JsonResponse(res)


def check_name(request):
    # print(request.GET)
    res = {'msg': '用户已存在', 'code': 110}
    name = request.GET.get('name')
    obj = UserInfo.objects.filter(username=name).first()
    if obj:
        return JsonResponse(res)
    else:
        res['code'] = 100
        res['msg'] = '用户不存在'
        return JsonResponse(res)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        pass
