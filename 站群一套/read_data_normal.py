#ecoding:utf-8
import json
import traceback
import sys
import datetime
import redis
from collections import defaultdict

reload(sys)
sys.setdefaultencoding("utf-8")

#db_spider = factory.get_db('spider')

ID_GEN = 'zhanqun_id_generator'
ID_RECORD = 'zhanqun_taskid_record'
client = redis.StrictRedis(host='52a34c024547489a.m.cnbja.kvstore.aliyuncs.com', port=6379, db=12, password='52a34c024547489a:0s9j09sHSj1sdf1oL')

HOST = '52a34c024547489a.m.cnbja.kvstore.aliyuncs.com'
DB = 12
PORT = 6379
PASSWD='52a34c024547489a:0s9j09sHSj1sdf1oL'
client = redis.StrictRedis(host=HOST, port=PORT, db=DB, password=PASSWD)
img_url_rec = 'zhanqun_pic_rec'

def get_id(task_id):
    if client.hexists(ID_RECORD, task_id):
        return client.hget(ID_RECORD, task_id)
    else:
        id = client.incr(ID_GEN)
        client.hset(ID_RECORD, task_id, id)
        return id

def parse_source(url):
    _list = ['114', 'xdf', 'baidu', '360', 'so', 'iask']
    for s in _list:
        if s in url:
            return s
    return 'other'

def process_time(date):
    if u'今天' in date or u'小时' in date or u'分钟' in date:
        return '2016-06-27'
    if u'昨天' in date:
        return '2016-06-26'
    return date.replace('.', '-')

category_id_dic = {
u'校园生活':['-3',],
u'谜语':['-2',],
u'翻译':['0',],
u'保健养生':['0',],
u'高考':['342',],
u'学习':['-1',],
u'购物':['0',],
u'烦恼':['897','1196','1199'],
u'服饰':['0',],
u'学校':['-3',],
u'求职就业':['0',],
u'升学入学':['-1',],
u'手机':['0',],
u'北京':['0',],
u'语言学':['-3',],
u'军事':['0',],
u'家庭关系':['897','1196','1199'],
u'法律':['-1',],
u'时事政治':['-1',],
u'文学':['-1',],
u'互联网':['573',],
u'外语学习':['-1',],
u'恋爱':['897','1196','1199'],
u'人文':['-1',],
u'民俗传统':['0',],
u'教育':['-1',],
u'小说':['0',],
u'动漫':['0',],
u'编程语言':['573',],
u'交通':['0',],
u'古诗词':['-1',],
u'语文':['-1',],
u'英语':['-1',],
u'硬件':['573',],
u'花鸟鱼虫':['-1',],
u'人体常识':['0',],
u'家电':['0',],
u'院校信息':['-3',],
u'脑筋急转弯':['-2',],
u'中考':['237',],
u'汽车':['0',],
u'广东':['0',],
u'游戏':['-2',],
u'歌词':['-2',],
u'美食':['-2',],
u'礼节礼仪':['0',],
u'日语':['0',],
u'企业管理':['0',],
u'操作系统':['573',],
u'感情':['897','1196','1199'],
u'网络':['573','619','623'],
u'诗歌':['-1',],
u'生活':['0',],
u'资源共享':['0',],
u'公务员':['817',],
u'电影':['-2',],
u'宠物':['-2',],
u'软件':['573',],
u'历史':['-1',],
u'理工学科':['-1',],
u'会计':['0',],
u'职业教育':['-1',],
u'计算机':['573',],
u'大学':['387',],
u'驾校':['0',],
u'成语':['-1',],
u'小学':['107',],
u'宗教':['0',],
u'作文':['-1',],
u'哲学':['-1',],
u'音乐':['-1',],
u'公务办理':['0',],
u'生活常识':['0',],
u'商业':['0',],
u'地理':['-1',],
u'起名':['0',],
u'明星':['-2',],
u'数学':['-1',],
u'中国古代史': ['266','302','306'],
u'教师交流': ['-1',],
u'高考地理': ['342',],
u'高中学习讲义': ['266','1245'],
u'大学英语': ['387',],
u'高考': ['342',],
u'初中语文': ['161','167'],
u'高考指南卡': ['342',],
u'师生关系': ['-1',],
u'初中历史': ['161',],
u'大学政治': ['387','410','418'],
u'高考数学': ['342','343','344'],
u'世界近现代史': ['266','302','306'],
u'问吧频道': ['0',],
u'初中物理': ['161',],
u'政治生活': ['-1',],
u'高考物理': ['342','353','354'],
u'高二生物': ['342','359','360'],
u'高校咨询': ['-3',],
u'同学关系': ['0',],
u'必修课程': ['266','267',],
u'青春叛逆': ['897','1196','1199'],
u'高考政治': ['342',],
u'自主招生': ['342',],
u'高考题库系列': ['342',],
u'阅读理解': ['266','272'],
u'区域地理': ['324','349','350'],
u'选修课程': ['266','267'],
u'师范国防': ['342',],
u'其他分类': ['-3',],
u'电脑常识': ['573',],
u'有机物': ['266','297'],
u'高一生物': ['266','307'],
u'初中英语': ['161','172'],
u'初中生物': ['161','212'],
u'电磁学': ['266','292'],
u'高招政策': ['342',],
u'元素化合物': ['266','297'],
u'高考化学': ['342','355','356'],
u'初中政治': ['161','212'],
u'艺体高考': ['342',],
u'心理调节': ['897','1196','1199'],
u'考试答案交流区': ['266','1245'],
u'基础知识': ['-1',],
u'初中数学': ['161','162'],
u'哲学生活': ['0',],
u'高考复习讲义': ['342',],
u'奥数竞赛': ['-1',],
u'写作指引': ['-1',],
u'初中地理': ['161','212'],
u'高考英语': ['342',],
u'试题调研系列': ['266','1245'],
u'家长咨询': ['-1',],
u'经济生活': ['-3',],
u'化学实验': ['266','297'],
u'基本概念、规律': ['266','297'],
u'人文地理': ['324','349','350'],
u'专题调研系列': ['266','1245'],
u'高考语文': ['342',],
u'海外留学': ['783',],
u'大学数学': ['387','410','414'],
u'书面表达': ['-1',],
u'高考冲刺讲义': ['342',],
u'热光原': ['266','292'],
u'中国近现代史': ['266','302','306'],
u'高三生物': ['266','307'],
u'自然地理': ['324','349','350'],
u'疯狂阅读系列': ['266','1245'],
u'校园早恋': ['0',],
u'高中力学': ['266','292'],
u'广西公务员':['817',],
u'江西公务员':['817',],
u'河北公务员':['817',],
u'宁夏公务员':['817',],
u'重庆公务员':['817',],
u'河南公务员':['817',],
u'辽宁公务员':['817',],
u'浙江公务员':['817',],
u'甘肃公务员':['817',],
u'四川公务员':['817',],
u'山西公务员':['817',],
u'青海公务员':['817',],
u'广东公务员':['817',],
u'山东公务员':['817',],
u'新疆公务员':['817',],
u'云南公务员':['817',],
u'广东教师考试':['-1',],
u'云南教师考试':['-1',],
u'河南教师考试':['-1',],
u'江西教师考试':['-1',],
u'北京教师考试':['-1',],
u'山西教师考试':['-1',],
u'西藏教师考试':['-1',],
u'陕西教师考试':['-1',],
u'湖南教师考试':['-1',],
u'福建教师考试':['-1',],
u'海南教师考试':['-1',],
u'广西教师考试':['-1',],
u'四川教师考试':['-1',],
u'辽宁教师考试':['-1',],
u'山东教师考试':['-1',],
u'浙江教师考试':['-1',],
u'江苏教师考试':['-1',],
u'贵州教师考试':['-1',],
u'河北教师考试':['-1',],
u'上海教师考试':['-1',],
u'新疆教师考试':['-1',],
u'天津教师考试':['-1',],
u'湖北教师考试':['-1',],
u'考务教师考试':['-1',],
u'内蒙古教师考试':['-1',],
u'安徽教师考试':['-1',],
u'青海教师考试':['-1',],
u'吉林教师考试':['-1',],
u'宁夏教师考试':['-1',],
u'黑龙江教师考试':['-1',],
u'甘肃教师考试':['-1',],
u'重庆教师考试':['-1',],
u'出国留学':['783',],
u'医学教育':['-3',],
u'研究生':['387',],
u'小语种':['-3',],
u'大学':['387',],
u'英语':['387',],
u'中小学':['140',],
u'职业教育':['502',],
u'编程问答':['573',],
u'情感家庭':['897','1196','1199'],
u'游戏':['-2',],
u'手机数码':['-2',],
u'体育运动':['-1',],
u'社会民生':['0',],
u'电脑网络':['573',],
u'教育科学':['-3',],
u'休闲爱好':['-2',],
u'文化艺术':['975'],
u'吃穿住行':['0',],
u'商业理财':['0',],
u'明星娱乐':['-2',],
u'地区相关':['0',],
u'电脑/网络':['573',],
u'生活':['0',],
u'游戏':['-2',],
u'烦恼':['897','1196','1199'],
u'商业/理财':['0',],
u'文化/艺术':['975',],
u'教育/科学':['-3',],
u'教育/科学':['-3',],
u'资源共享':['0',],
u'社会民生':['0',],
u'电子数码':['573',],
u'体育/运动':['0',],
u'校园生活':['-1',],
u'学习':['-1',],
u'升学入学':['-1',],
u'家庭关系':['897','1196','1199'],
u'法律':['852',],
u'时事政治':['',],
u'文学':['-1',],
u'人文':['0',],
u'民俗传统':['0',],
u'教育':['-1',],
u'交通':['0',],
u'古诗词':['-1',],
u'语文':['-1',],
u'英语':['-1',],
u'院校信息':['-3',],
u'脑筋急转弯':['-2',],
u'感情':['0',],
u'网络':['573',],
u'生活常识':['0',],
u'生活':['0',],
u'资源共享':['0',],
u'历史':['-1',],
u'理工学科':['-1',],
u'职业教育':['502',],
u'大学':['387',],
u'成语':['-1',],
u'作文':['-1',],
u'诗歌':['-1',],
u'音乐':['975','1011'],
u'外语学习':['714',],
u'商业':['0',],
u'起名':['0',],
u'明星':['-2',],
u'求职就业':['0',],
u'数学':['-1',],
u'交通出行':['0',],
u'育儿':['-1',],
u'商业理财':['0',],
u'网络游戏':['-2',],
u'购车养车':['0',],
u'娱乐休闲':['-2',],
}
del_res = [
    u'资源平台',
    u'网络课堂',
    u'虚拟货币咨询',
    u'高考指南卡',
]
def read(data):
    dic = defaultdict(int)
    sub_class = 34
    fw = open('%s.res'%(data.split('/')[-1]), 'w')
    for line in open(data):
        try:
            (taskid, result) = line.strip().split('$$$$$')
            data = json.loads(result.replace('\\\\','\\'))
            title = data.get('title', '')
            #print title
            if not title:
                continue
            #type = data.get('type', '')
            if len(data['category_id']) == 0:
                category = ''
            else:
                category = data.get('category_id', '')[0]
            if category in del_res:
                continue
            if data.has_key('id'):
                data.pop('id')
            update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            source = data['source']
            category_id_list = category_id_dic.get(category, ['0', ])
            data['category_id'] = category_id_list
            id = get_id(taskid)
            #print id
            _list = [str(id), str(sub_class), json.dumps(data), source, update_time, taskid]
           # print len(_list)
            fw.write('\x01'.join(_list) + '\n')
            fw.flush()
        except Exception, e:
            traceback.print_exc()
            #print e
            print taskid

def sta(data):
    dic = defaultdict(int)
    sub_class = 34
    #fw = open('%s.res'%(data.split('/')[-1]), 'w')
    dic = defaultdict(int)
    for line in open(data):
        try:
            (taskid, result) = line.strip().split('$$$$$')
            data = json.loads(result.replace('\\\\','\\'))
            #print data
            title = data.get('title', '')
            #print title
            if not title:
                continue
            #type = data.get('category_id', '')
            if len(data['category_id'])==0:
                continue
            category = data.get('category_id', '')[0]
            #if category in del_res:
             #   continue
            dic[category] += 1
            '''
            update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            source = data['source']
            category_id_list = category_id_dic.get(type, ['0', ])
            data['category_id'] = category_id_list
            id = get_id(taskid)
            _list = [str(id), str(sub_class), json.dumps(data), source, update_time, taskid]
            fw.write('\x01'.join(_list) + '\n')
            fw.flush()
            '''
        except Exception, e:
            #print e
            #print taskid
            pass
    for k, v in dic.iteritems():
        if v > 600:
            print 'u\''+k+'\':[\'\',],'
        #print k, v

if __name__ == '__main__':
    filename = sys.argv[1]
    read(filename)
    #sta(filename)
