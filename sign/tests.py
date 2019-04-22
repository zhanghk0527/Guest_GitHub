# -*- coding:utf-8 -*-

from django.test import TestCase
from sign.models import Event,Guest
from sign.module_ex import Calculator
from django.contrib.auth.models import User # 以后追踪一下这个方法在什么地方，作用是什么？

'''
Auther: 张
Date: 2019-01-19 16:24
Describe: 使用Django内部unittest框架进行发布会管理系统单元测试
'''

'''
使用Django内部test命令运行测试的方法：
    
    运行指定应用下的所有测试用例：
        
        python manage.py test applicationName，例如：python manage.py test sign
    
    运行指定应用下tests.py文件：
        
        python manage.py test applicationName.tests.py，例如：python manage.py test sign.tests
        
    运行指定应用下，tests.py文件中的测试类：
      
        python manage.py test applicationName.tests.className，例如：python manage.py test sign.tests.ModelTest
        
    运行指定应用下，tests.py文件中的测试类下的某个测试方法（测试用例）：
    
        python manage.py test applicationName.tests.className.def，例如：python manege.py test sign.tests.ModelTest.test_event_models
        
    运行Django项目中所有测试用例，模糊匹配：-p (或：--pattern)
    
        python manage.py test -p test*.py  （匹配以“test”为开头“.py”为结尾的文件）
        
        或：python manage.py test --pattern test*.py
'''

# Create your tests here.
class ModelTest(TestCase):
    # 初始化测试数据
    def setUp(self):
        # 创建发布会
        Event.objects.create(id=6, name="oneplus 3 event", status=True, limit=2000, address="shenzhen", start_time="2019-04-19 16:27:50")

        # 创建用户
        Guest.objects.create(id=16, event_id=6, realname="alen", phone="17900001111", email="alen@mail.com", sign=False)

    # 测试用例001：检查新增的发布会是否正确
    def test_event_models(self):
        result = Event.objects.get(name="oneplus 3 event")
        self.assertEqual(result.address, "shenzhen")
        self.assertTrue(result.status)

    # 测试用例002：检查新增的用户是否正确
    def test_guest_models(self):
        reuslt = Guest.objects.get(phone="17900001111")
        self.assertEqual(reuslt.realname, "alen")
        self.assertFalse(reuslt.sign)

# 调用的计算器方法，检查运算
class Calculator1(TestCase):
    def setUp(self):
        self.cal = Calculator(8,4)

    def test_add(self):
        result = self.cal.add()
        self.assertEqual(result, 12)

# 首页的测试用例
class IndexPageTest(TestCase):
    def test_index_page_renders_index_template(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)

# 登录动作的测试用例
class LoginActionTest(TestCase):

    # 初始化测试数据：添加一个用户（username: zhangsan, email: zhangsan@mail.com, password: zhangsan123）
    def setUp(self):
        User.objects.create_user('zhangsan', 'zhangsan@mail.com', 'zhangsan123')

    # 测试用例001：测试用户是否存在
    def test_add_user(self):
        user = User.objects.get(username='zhangsan')
        self.assertEqual(user.username, "zhangsan")
        self.assertEqual(user.email, "zhangsan@mail.com")

    # 测试用例002：用户名和密码错误，判断提示信息
    def test_login_action_username_password_null(self):
        test_data = {'username':'','password':''}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    # 测试用例003：用户名和密码错误，判断提示信息
    def test_login_action_username_password_error(self):
        test_data = {'username':'abc','password':'123'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    # 测试用例004：用户名和密码正确，判断是否登录成功，302重定向到内部页面的状态码
    def test_login_action_success(self):
        test_data = {'username':'zhangsan','password':'zhangsan123'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)

# 发布会管理的测试用例
class EventManageTest(TestCase):
    def setUp(self):
        User.objects.create_user('lisi','lisi@mail.com','lisi123')
        Event.objects.create(name='iPhone_XS', limit='2000', address='beijing',status=1, start_time='2019-04-22 11:00')
        self.login_user = {"username":"lisi", "password":"lisi123"}

    def test_event_manage_success(self):
        # 登录系统
        response = self.client.post('/login_action/', data=self.login_user)
        # 进入发布会管理页面进行测试校验
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"iPhone_XS", response.content)
        self.assertIn(b"beijing", response.content)

    def test_event_manage_search_success(self):
        # 登录系统
        response = self.client.post('/login_action/', data=self.login_user)
        # 发布会查询操作校验
        response = self.client.post('/search_name/', {"name":"iPhone_XS"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"iPhone_XS", response.content)
        self.assertIn(b"beijing", response.content)

# 嘉宾管理的测试用例
class GuestManageTest(TestCase):
    # 初始化测试数据
    def setUp(self):
        User.objects.create_user('wangwu', 'wangwu@mail.com', 'wangwu123')
        Event.objects.create(id=6, name='xiaomi9', limit='2000', address='shenzhen', status=1, start_time='2019-04-22 12:10')
        Guest.objects.create(realname='Alen', phone='17600001234', email='Alen@mail,com', sign=0, event_id=6)
        self.login_user = {"username":"wangwu", "password":"wangwu123"}

    # 测试用例001：检查嘉宾信息是否存在
    def test_event_manage_success(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Alen", response.content)
        self.assertIn(b"17600001234", response.content)

    # 测试用例002：检查嘉宾搜索结果是否正确
    def test_guest_manage_search_success(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_phone/', {"phone":"17600001234"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Alen", response.content)
        self.assertIn(b"17600001234", response.content)
        print (response.content)

# 用户签到的测试用例
class SignIndexActionTest(TestCase):
    # 初始化测试数据
    def setUp(self):
        User.objects.create_user('zhaoliu','zhaoliu@mail.com','zhaoliu123')
        Event.objects.create(id=6, name='iPhone_XS', limit='2000', address='beijing', status=1, start_time='2019-04-22 15:30')
        Event.objects.create(id=7, name='OnePlus_4', limit='2000', address='shenzhen', status=1, start_time='2019-04-22 15:40')
        Guest.objects.create(realname='Alen', phone='17600001112', email='Alen@mail.com', sign=0, event_id=6)
        Guest.objects.create(realname='Luxi', phone='17611112222', email='Luxi@mail.com', sign=1, event_id=7)
        self.login_user = {"username":"zhaoliu", "password":"zhaoliu123"}

    # 测试用例001：手机号为空时，检查提示信息"phone error."
    def test_sign_index_action_phone_null(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/6/', {"phone":""})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"phone error.", response.content)

    # 测试用例002：手机号错误时，检查提示信息"event id or phone error."
    def test_sign_index_action_phone_or_event_id_error(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/7/', {"phone":"17600001112"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"event id or phone error.", response.content)

    # 测试用例003：手机号已签到，检查提示信息"user has sign in."
    def test_sign_index_action_user_sign_has(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/7/', {"phone":"17611112222"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user has sign in.", response.content)

    # 测试用例004：手机号正确，检查提示信息"sign in success!"
    def test_sign_index_action_sign_success(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/6/', {"phone":"17600001112"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"sign in success!", response.content)