from django.test import TestCase
# from django.contrib.auth.models import check_pa
from game.views import create_user, create_company
from game.models import User, Company, Record



# import json
# Create your tests here.

class GameTestCase(TestCase):
    def test_new_user_register(self):
        response = self.client.post('/game/register',
            data={'username': 'runtu881', 'password': 'runtuRmumu233', 'email': 'dsa@me.com'})
        # 状态码是200
        self.assertEqual(response.status_code, 200)
        # 数据库里面多一个user
        self.assertEqual(User.objects.count(), 1)
        # 用户名和密码没错
        runtu = User.objects.first()
        self.assertEqual(runtu.username, 'runtu881')
        self.assertTrue(runtu.password, 'runtuRmumu233') # 密码被加密了，不能直接对比

    # def test_user_create_new_company(self):
    #     # 搞一个人来创建公司
    #     self.client.post('/game/register',
    #         data={'username': 'runtu881', 'password': 'runtuRmumu233', 'email': 'dsa@me.com'})
    #     founder = User.objects.first()
    #
    #     # 先登录
    #     self.client.post('/login',
    #         data={'username': 'runtu881', 'password': 'runtuRmumu233'})
    #     # 创建公司
    #     response = self.client.post('/game/create_company',
    #         data={'user_id': founder.id, 'company_name': '激情骄阳'})
    #     # Company table里面多了个object
    #     self.assertEqual(Company.objects.count(), 1)
    #
    #     # 闰土的公司是新建的这个公司
    #     founder = User.objects.first()
    #     new_company = Company.objects.first()
    #     self.assertEqual(founder.company, new_company)
    #
    # def test_can_join_company(self):
    #     # 一个创建者和一个公司
    #     self.client.post('/game/register',
    #         data={'username': 'runtu881', 'password': 'runtuRmumu233', 'email': 'dsa@me.com'})
    #     founder = User.objects.first()
    #     self.client.post('/game/create_company',
    #         data={'user_id': founder.id, 'company_name': '激情骄阳'})
    #     # 创建一个新用户
    #     self.client.post('/game/register',
    #         data={'username': 'khachiyan', 'password': 'aladeen!motherfuker', 'email': 'ss@me.com'})
    #     # 新用户加入公司
    #     self.client.post('/game/join_company',
    #         data={'company_name': "激情骄阳", 'user_id': 2})
    #     # khachiyan的公司也是激情骄阳
    #     company = Company.objects.first()
    #     khachiyan = User.objects.get(pk=2)
    #     self.assertEqual(khachiyan.company, company)
    #
    #
    #     # TODO: views.py里面的companys多了个object，不知道怎么测试

    def test_user_login_then_logout(self):
        # 创建一个闰土
        self.client.post('/game/register',
            data={'username': 'runtu881', 'password': 'runtuRmumu233', 'email': 'dsa@me.com'})
        runtu = User.objects.first()

        # 输错密码的登录
        response = self.client.post('/login',
            data={'username': 'runtu881', 'password': 'caonima'})
        # 被redirect到主页
        self.assertEqual(response.status_code, 302)

        # 闰土登录
        response = self.client.post('/login',
            data={'username': 'runtu881', 'password': 'runtuRmumu233'})
        # 确认登录成功
        self.assertEqual(response.status_code, 200)

        # 闰土logout
        response = self.client.post('/logout')
        # redirect到主页
        self.assertEqual(response.status_code, 302)



    '''
    上面是用户相关的，下面是游戏相关的
    '''
    def test_start_game(self):
        # 创建一个闰土
        self.client.post('/game/register',
            data={'username': 'runtu881', 'password': 'runtuRmumu233', 'email': 'dsa@me.com'})
        runtu = User.objects.first()

        # 闰土登录
        response = self.client.post('/login',
            data={'username': 'runtu881', 'password': 'runtuRmumu233'})

        # # 闰土创建一个公司
        # self.client.post('/game/create_company',
        #     data={'company_name': '激情骄阳'})

        # 闰土点开始游戏
        response = self.client.post('/game/start_game')

        self.assertEqual(response.status_code, 200)

        # 数据库里面多了一条Record
        self.assertEqual(Record.objects.count(), 1)
        # 时间是是创建时间
        # self.assertAlmostEqual()
        # Record的players里面有闰土
        record = Record.objects.first()
        self.assertTrue(runtu in record.players.all())
