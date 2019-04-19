from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render, get_object_or_404
# Create your views here.
def index(request):
    # return HttpResponse("Hello Django!")
    return render(request,"index.html")

# 登录操作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username= username,password= password)
        if user is not None:
            auth.login(request, user)
            # 使用session方式获取用户信息，将获取到的session信息记录到浏览器
            request.session['user'] = username
        # if username == 'admin' and password == 'admin123':
            # return render(request,'event_manage.html')
            response = HttpResponseRedirect('/event_manage/')
            # 使用cookie方式获取用户信息
            # response.set_cookie('user',username,3600) # 添加浏览器cookie
            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})

# 发布会管理
@login_required # 添加装饰，以类的方式运行
def event_manage(request):
    # 读取浏览器cookie
    # username = request.COOKIES.get('user','')
    event_list = Event.objects.all()
    username = request.session.get('user','')

    # 读取浏览器session
    # username = request.session.get('user','')
    return render(request,"event_manage.html", {"user":username,
                                                "events":event_list})

    # return render(request,"event_manage.html")

# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html",{"user":username,
                                                "events":event_list})

# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list,5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts})

# 嘉宾名称搜索
@login_required
def search_phone(request):
    username = request.session.get('user', '')
    search_phone = request.GET.get("phone", "")
    guest_list = Guest.objects.filter(phone__contains=search_phone)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": guest_list})

# 签到页面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id = eid)
    return render(request, 'sign_index.html', {'event': event})

# 签到动作
@login_required
def sign_index_action(request,eid):
    # 在Event数据中查找对应id，如果查询不到，返回404页面
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print (phone)

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'phone error.'})

    result = Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'event id or phone error.'})

    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': "user has sign in."})
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'sign in success!',
                                                   'guest': result})

# 退出操作
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response