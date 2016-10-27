#coding: utf8
import re, time, datetime, logging
from collections import OrderedDict

logger_public = logging.getLogger("public")

def load_codemap(filename_codemap):
    dict_t = OrderedDict()
    
    f = open(filename_codemap, mode='r', encoding='utf8')
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue
        t = line.split('=')
        dict_t[t[0].strip()] = t[1].strip()

    return dict_t

def transform_code(dict_coadmap, cx):
    for key in list(dict_coadmap.keys()):
        if key in cx:
            return dict_coadmap[key]
    else:
        return ''
    
def parse_int(s):
    ss = re.search('\d+', s)
    if ss:
        return int(ss.group())
    return ''

def parse_float(s):
    ss = re.search('\d+\.\d+|\d+', s)
    if ss:
        return float(ss.group())
    return ''

def parse_datetime(s, format_from='%Y-%m-%d-%H-%M.txt', format_to='%Y-%m-%d %H:%M:%S'):
    try:
        a = time.strptime(s, format_from)
        return time.strftime(format_to,a)
    except:
        pass
    return ''

def transform_line(constants, sline):
    if not sline:
        return
    l_cols = sline.strip('\r\n').split('\t')
    if len(l_cols)!=66:
        logger_public.warn('cols : %s' % len(l_cols))
        logger_public.warn(sline)
        return
    #城市/行政区---------------------------------------------
    s_laiyuanlianjie = l_cols[4]
    m = re.search('(http://.*?)/.*', s_laiyuanlianjie)
    #用url转换城市
    code_shi = ''
    if m.group(1) in constants.dict_codemap_shiurl.keys():
        code_shi = constants.dict_codemap_shiurl[m.group(1)]
    s_chengshi = l_cols[1]
    s_xingzhengqu = l_cols[2]
    code_xingzhengqu = ''
    if code_shi:
        code_shi = code_shi.split(',')[0]
        if len(code_shi)==6:#如果是区县，根据规则转换成所属城市
            code_xingzhengqu = code_shi
            if code_shi[0:2] in ('11', '12', '31', '50'):#直辖市取前两位+01，确实存在蓟县=120225
                code_shi = code_shi[0:2] + '01'
            else:#其他城市直接取前四位
                code_shi = code_shi[0:4]
    else:
        #转换失败,使用城市名称转换
        
        l = list(constants.dict_codemap_shi.keys())
        for key in l:
            if s_chengshi in key or key in s_chengshi:
                code_shi = constants.dict_codemap_shi[key]
                break
        if not code_shi:
            l = list(constants.dict_codemap_quxian.keys())
            for key in l:
                if s_chengshi in key or key in s_chengshi:
                    code_shi = constants.dict_codemap_quxian[key]
                    code_xingzhengqu = code_shi
                    if code_shi[0:2] in ('11', '12', '31', '50'):#直辖市取前两位+01，确实存在蓟县=120225
                        code_shi = code_shi[0:2] + '01'
                    else:#其他城市直接取前四位
                        code_shi = code_shi[0:4]
                    break
    
    if not code_xingzhengqu:
        for key in list(constants.dict_codemap_quxian.keys()):
            if s_xingzhengqu and (s_xingzhengqu in key or key in s_xingzhengqu):
                code_xingzhengqu = constants.dict_codemap_quxian[key]
                break
    #城市/行政区---------------------------------------------
    
    #层类型/当前楼层/总楼层-----------------------------------
    #当前层1-127，必选，高中低-------------------------------
    
    i_zonglouceng = None
    i_dangqianlouceng = None
    try:
        i_zonglouceng = int(l_cols[12])
        i_dangqianlouceng = int(l_cols[13])
    except:
        pass
    #因当前楼层和总楼层式必要字段，判定楼层数据是否异常，异常则忽略该条数据
    if i_zonglouceng==1:
        i_dangqianlouceng = 1
    
    if i_zonglouceng:
        s_zonglouceng = str(i_zonglouceng)
    else:
        s_zonglouceng = ''
        
    if i_dangqianlouceng:
        s_dangqianlouceng = str(i_dangqianlouceng)
    else:
        s_dangqianlouceng = ''
    
    s_cengleixing = l_cols[14]
    code_cengleixing = transform_code(constants.dict_codemap_cengleixing, s_cengleixing)
    #层类型/当前楼层/总楼层--------------------------------
    
    #朝向
    code_chaoxiang = transform_code(constants.dict_codemap_chaoxiang, l_cols[15])
    if not code_chaoxiang:
        return
    #朝向
    
    #建成年份/房龄
    s_jianchengnianfen = parse_int(l_cols[9])
    s_fangling = parse_int(l_cols[10])
    i_curyear = int(str(datetime.date.today())[0:4])
    if not s_jianchengnianfen:
        if s_fangling:
            s_jianchengnianfen = i_curyear - s_fangling
    #建成年份/房龄
    
    #装修
    code_zhuangxiu = transform_code(constants.dict_codemap_zhuangxiu, l_cols[30])
    #装修
    
    code_zhuzhaileibie = transform_code(constants.dict_codemap_zhuzhaileibie, l_cols[28])
    code_chanquanxingzhi = transform_code(constants.dict_codemap_chanquanxingzhi, l_cols[29])
    code_jianzhuleibie = transform_code(constants.dict_codemap_jianzhuleibie, l_cols[31])
    #TODO: 是否考虑平房别墅四合院的影响
    return [l_cols[0],#信息来源
            s_chengshi, code_shi, s_xingzhengqu, code_xingzhengqu,
            l_cols[3],#片区 
            l_cols[4],#来源链接
            l_cols[5],#题名
            l_cols[6],#小区名称
            l_cols[7],#小区链接
            l_cols[8],#地址
            l_cols[9],#建成年份
            str(s_jianchengnianfen) if s_jianchengnianfen else '',#建成年份2
            l_cols[10],#房龄
            str(s_fangling),#房龄2
            l_cols[11],#楼层
            l_cols[12],#总楼层
            s_zonglouceng,#总楼层2
            l_cols[13],#当前楼层
            s_dangqianlouceng,#当前楼层2
            s_cengleixing,#层类型
            str(code_cengleixing),#层类型2
            l_cols[15],#朝向
            str(code_chaoxiang),#朝向2
            l_cols[16],#建筑面积
            str(parse_float(l_cols[16])),#建筑面积2
            l_cols[17],#使用面积
            str(parse_float(l_cols[17])),#使用面积2
            l_cols[18],#户型
            l_cols[19],#卧室数量
            str(parse_int(l_cols[19])),#卧室数量2
            l_cols[20],#客厅数量
            str(parse_int(l_cols[20])),#客厅数量2
            l_cols[21],#卫生间数量
            str(parse_int(l_cols[21])),#卫生间数量2
            l_cols[22],#厨房数量
            str(parse_int(l_cols[22])),#厨房数量2
            l_cols[23],#阳台数量
            str(parse_int(l_cols[23])),#阳台数量2
            l_cols[24],#总价
            str(parse_int(l_cols[24])),#总价2
            l_cols[25],#单价
            str(parse_int(l_cols[25])),#单价2
            l_cols[26],#本月均价
            l_cols[27],#小区开盘单价
            l_cols[28],#住宅类别
            str(code_zhuzhaileibie),#住宅类别2
            l_cols[29],#产权性质
            str(code_chanquanxingzhi),#产权性质2
            l_cols[30],#装修
            str(code_zhuangxiu),#装修2
            l_cols[31],#建筑类别
            str(code_jianzhuleibie),
            l_cols[32],#楼盘物业类型
            l_cols[33],#小区链接
            l_cols[34],#联系人
            l_cols[35],#联系人链接
            l_cols[36],#经纪公司
            l_cols[37],#门店
            l_cols[38],#电话号码
            l_cols[39],#服务商圈
            l_cols[40],#经纪人注册时间
            parse_datetime(l_cols[40], format_from='%Y-%m-%d'),# %H-%M-%S 经纪人注册时间2
            l_cols[41],#经纪公司房源编号
            l_cols[43],#小区总户数
            l_cols[44],#小区总建筑面积
            l_cols[45],#容积率
            l_cols[46],#小区总停车位
            l_cols[47],#开发商
            l_cols[48],#交通状况
            l_cols[49],#配套设施
            l_cols[50],#楼盘绿化率
            l_cols[51],#物业公司
            l_cols[52],#楼盘物业费
            l_cols[53],#土地使用年限
            l_cols[54],#入住率
            l_cols[55],#学校
            l_cols[56],#地上层数
            l_cols[57],#花园面积
            l_cols[58],#地下室面积
            l_cols[59],#车库数量
            l_cols[60],#车位数量
            l_cols[61],#厅结构
            l_cols[62],#导航
            l_cols[63],#房屋图片
            l_cols[64],#纬度
            l_cols[65],#经度
            ]


if __name__ == "__main__":
    dict_codemap_chaoxiang = OrderedDict([('不确定', '0'), ('南北', '1'), 
                                          ('东西', '2'), ('东南', '3'), 
                                          ('东北', '4'), ('西南', '5'), 
                                          ('西北', '6'), ('南', '7'), 
                                          ('北', '8'), ('东', '9'), 
                                          ('西', '10')])
#     print(transform_code(dict_codemap_chaoxiang, '东1南东1'))
#     print(transform_code(dict_codemap_chaoxiang, '南东1'))
#     print(transform_code(dict_codemap_chaoxiang, '南东1'))
#     print(transform_code(dict_codemap_chaoxiang, '南北朝向'))
#     print (parse_float('add.asd'))
#     print (int('0'))
#     a = datetime.date.today()
#     print(str(a))
#     if not '0':
#         print(1)
    d = {'a':'a'}
    a = 1 if 'aa' in d.keys() else 2
    print (a)