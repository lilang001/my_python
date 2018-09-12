本demo可以直接manage.py server 运行

static和templates都挂在了app下

settings.py
INSTALLED_APPS 增加 "mz_plus"
TEMPLATE_DIRS 增加 os.path.join(PROJECT_ROOT, 'apps', 'mz_plus', 'templates').replace('\\', '/'),

urls.py
增加url(r'^plus/', include('mz_plus.urls'), name='plus')

/plus/ 为测试演示页面
/plus/recommend_video/ 为动态加载视频div


当前目录下的test.html可以直接打开
也可以http://127.0.0.1:8000/plus/  也是测试页面


/static/vbook.js中写死了127.0.0.1,,,可自行修改