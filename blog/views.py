from django.shortcuts import render, HttpResponse
from blog.blog_forms import User
from django.http import JsonResponse
from blog.models import UserInfo
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
from django.contrib.auth import authenticate
from gvcode import VFCode


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
    res = {'code': 100, 'msg': '登陆成功'}
    code = request.POST.get('code')
    if request.session.get('code').lower() == code.lower():
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 如果认证成功（用户名和密码正确有效），便会返回一个 User 对象。
        obj = authenticate(username=username, password=password)
        if obj:
            return JsonResponse(res)
        res['code'] = 110
        res['msg'] = '用户名或密码错误'
        return JsonResponse(res)
    res['code'] = '120'
    res['msg'] = '验证码错误'
    return JsonResponse(res)


# 生成随机验证码
def get_code(request):
    vc = VFCode(width=350, height=50)
    vc.generate_mix()
    # vc.generate_op()
    print(vc.get_img_base64()[0])
    byte_io = BytesIO()
    vc.save(byte_io, fm='png')
    request.session['code'] = vc.get_img_base64()[0]
    return HttpResponse(byte_io.getvalue())


# 或取随机颜色 rgb
# def get_color():
#     return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


# def get_code(request):
#     # 1 直接返回一张验证码图片
#     # with open('./6F3pN.png', 'rb') as f:
#     #     data = f.read()
#     # return HttpResponse(data)
#
#     # 2 自己生成一张图片 返回 借助pillow模块
#     # # 2.1 生成一个图片对象
#     # img = Image.new('RGB', (350, 60), color=(0, 0, 0))
#     # # 2.2 保存图片到本地 并返回给前端
#     # with open('cond.png', 'wb') as f:
#     #     img.save(fp=f)
#     # with open(('./cond.png'), 'rb') as f:
#     #     return HttpResponse(f.read())
#
#     # 3 将图片保存在内存中
#     # 3.1 生成一个图片对象
#     # img = Image.new('RGB', (350, 60), color=(255, 0, 0))
#     # # 3.2 保存图片到内存地 并返回给前端
#     # byte_io = BytesIO()
#     # img.save(fp=byte_io, format='png')
#     # return HttpResponse(byte_io.getvalue())
#
#     # 4 在图片上写文字
#     # 4.1 生成一个图片对象
#     img = Image.new('RGB', (350, 50), color=(255, 255, 255))
#     draw = ImageDraw.Draw(img)
#     font = ImageFont.truetype(font='./static/font/1641263938811335.ttf', size=50)
#     code_str = ''
#     for i in range(5):
#         ran_num = str(random.randint(0, 9))
#         ran_upper = chr(random.randint(65, 90))
#         while ran_upper == 'I' or ran_upper == 'L':
#             ran_upper = chr(random.randint(65, 90))
#         ran_lower = chr(random.randint(97, 122))
#         while ran_lower == ('i' or 'l'):
#             ran_upper = chr(random.randint(65, 90))
#         res = random.choice([ran_num, ran_lower, ran_upper])
#         draw.text(xy=(10 + i * 60, 0), text=res, font=font, fill=get_color())
#         code_str += res
#     print(code_str)
#     request.session['code'] = code_str
#     # 画线
#     for i in range(10):
#         draw.line([(random.randint(0, 350), random.randint(0, 50)), (random.randint(0, 350), random.randint(0, 50))],
#                   fill=get_color())  # 起点和终点
#
#     # 画点
#     for i in range(100):
#         draw.point((random.randint(0, 350), random.randint(0, 50)), fill=get_color())
#
#     # 4.2 保存图片到内存地 并返回给前端
#     byte_io = BytesIO()
#     img.save(fp=byte_io, format='png')
#     return HttpResponse(byte_io.getvalue())


def index(request):
    print(request)
    return render(request, 'index.html')
