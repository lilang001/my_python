��demo����ֱ��manage.py server ����

static��templates��������app��

settings.py
INSTALLED_APPS ���� "mz_plus"
TEMPLATE_DIRS ���� os.path.join(PROJECT_ROOT, 'apps', 'mz_plus', 'templates').replace('\\', '/'),

urls.py
����url(r'^plus/', include('mz_plus.urls'), name='plus')

/plus/ Ϊ������ʾҳ��
/plus/recommend_video/ Ϊ��̬������Ƶdiv


��ǰĿ¼�µ�test.html����ֱ�Ӵ�
Ҳ����http://127.0.0.1:8000/plus/  Ҳ�ǲ���ҳ��


/static/vbook.js��д����127.0.0.1,,,�������޸�