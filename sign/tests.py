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
    def setUp(self):
        Event.objects.create(id=6, name="oneplus 3 event", status=True, limit=2000, address="shenzhen", start_time="2019-04-19 16:27:50")

        Guest.objects.create(id=16, event_id=6, realname="alen", phone="17900001111", email="alen@mail.com", sign=False)

    def test_event_models(self):
        result = Event.objects.get(name="oneplus 3 event")
        self.assertEqual(result.address, "shenzhen")
        self.assertTrue(result.status)

    def test_guest_models(self):
        reuslt = Guest.objects.get(phone="17900001111")
        self.assertEqual(reuslt.realname, "alen")
        self.assertFalse(reuslt.sign)

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