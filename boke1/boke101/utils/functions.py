from django.http import HttpResponseRedirect
from django.urls import reverse


def is_login(func):

    def check(request):
        try:
            # 如果session中存在id值就说明可以访问首页
            request.session['user_id']
        except:
            # 不存在的话跳转到登录
            return HttpResponseRedirect(reverse('user:login'))

        return func(request)

    return check










