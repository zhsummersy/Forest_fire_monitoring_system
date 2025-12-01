from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from rest_framework.parsers import JSONParser
import requests
import json
import re
import sqlite3  

# Create your views here.


def read(request):
    return render(request, 'home/read.html')

def position(request):
    return render(request, 'home/position.html')

def weather(request):

    def parse_string(input_string):  
        data = {}  
        lines = input_string.split('\n')  
        for line in lines:  
            if ':' in line:  
                title, value = line.split(':')[0], line.split(':')[1] 
                title = title.strip()  
                value = value.strip()  
                data[title] = value  
        return data 
    
    UA = {
        'Referer': 'http://www.weather.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43'
      }
 
    class GetSkWeather():
        def get_sk_weather(area_id):
        # 请求的URL
            URL = f'http://d1.weather.com.cn/sk_2d/{area_id}.html'
            # 发起请求
            req = requests.get(URL, headers=UA)
            
            if req.status_code == 200:
                req.encoding = 'utf-8'
                
                # 使用正则表达式匹配实况天气
                sk_weather = re.search(r'{.*}', req.text)
                if sk_weather:
                    # 将JSON格式的字符串转换为对应的Python对象
                    weather_json = json.loads(sk_weather.group())
        
                    sk_weather = f'''
                    今日日期: {weather_json['date']}
                    更新时间: {weather_json['time']}
                    当前城市: {weather_json['cityname']}
                    当前温度: {weather_json['temp']}℃
                    当前天气: {weather_json['weather']}
                    风向风速: {weather_json['WD']} {weather_json['WS']}
                    相对湿度: {weather_json['SD']}
                    空气指数: {weather_json['aqi']}
                    '''
                else:
                    return "暂未获取实况天气"
        
                return sk_weather
            
            else:
                return "数据请求失败"
    input_string = GetSkWeather.get_sk_weather(101080101)
    data = parse_string(input_string) 
    print(data)
    return render(request, 'home/weather.html',{'data':data})

def upload(request):
    if request.method == 'GET':
        return HttpResponse('404')
    else:
        data = JSONParser().parse(request)
        print(data)
        c = Upload(
                   Temperature = data['Temperature'],
                   Humidity = data['Humidity'],
                   MQ = data['MQ'],
                   WaterRate = data['WaterRate'],
                   detected = data['detected'],
                   Illumination = data['Illumination'],
                   fire = data['fire'])

        c.save()
        return HttpResponse('Server has received')

def alarm(request):
    if request.method == 'GET':
        data = alarming.objects.all().order_by('-id')[:10]
        context = {'data' : data}
        return render(request, 'home/alarm.html',context)
    else:
        data = JSONParser().parse(request)
        print(data)
        c = alarming(
                   alarm = data['alert'],
                   value = data['value'],
                   )
        c.save()
        return HttpResponse('Server has received')

def pollute(request):
    data = Upload.objects.all().order_by('-id')[:30]
    chart = data[:10]
    sql = '''SELECT id,
    CASE   
        WHEN AVG(WaterRate) > 30 AND AVG(Illumination) > 30 THEN '优'  
        ELSE '差'  
    END AS Result,AVG(WaterRate) as WaterRate ,AVG(Illumination) as Illumination
FROM   
    (SELECT * FROM blog_upload ORDER BY ID DESC LIMIT 50) AS subquery
		'''
    conn = sqlite3.connect('db.sqlite3')  
    cur = conn.cursor()   
    cur.execute(sql)
    conn.commit() 
    predict = cur.fetchall()[0]
    conn.close() 
    print(predict)
    info = '最新50条数据显示平均土壤湿度为'+str(predict[2])+'%,平均光照强度为'+str(predict[3])[:4]+'%,系统预测预测森林的生长状况为:'+str(predict[1])
    context = {'data' : data,'chart' : chart,'predict':info}
    return render(request, 'home/pollute.html',context)


def recommend(request):
    return render(request, 'home/recommend.html')


def blogHome(request):
    allPosts = Post.objects.all()[:5]
    context = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html', context)


def blogPost(request, pk):
    post = Post.objects.filter(pk=pk).latest('timeStamp')
    print(post)
    context = {'post': post}
    return render(request, 'blog/blogPost.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f':Your account has been created! You are now able to log in ')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f':Your account has been Updated ')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog/profile.html', context)
