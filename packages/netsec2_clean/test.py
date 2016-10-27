#coding:utf8
import os, sys, time, logging.handlers
from modules import public

def get_main_path():
    return os.path.dirname(__file__)

filename_log = 'netsec2_clean.log'
path_main = get_main_path()
path_codemap = os.path.join(path_main, 'codemap')
delay_sleep = 600


def config_logging(log_level, file_name):
    rotatingFileHandler = logging.handlers.RotatingFileHandler(
                                                filename = file_name,
                                                maxBytes = 1024 * 1024 * 100,
                                                backupCount = 20 )
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(lineno)3d \
    %(levelname)-8s %(message)s")
    rotatingFileHandler.setFormatter(formatter)
    logging.getLogger("").addHandler(rotatingFileHandler)
    console = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(name)-12s: %(lineno)d \
    %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)
    logger = logging.getLogger("")
    logger.setLevel(log_level)

class Constants():
#     path_main = ''
#     path_codemap = ''
    fn_cengleixing = os.path.join(path_codemap, 'cengleixing.lst')
    fn_chanquanxingzhi = os.path.join(path_codemap, 'chanquanxingzhi.lst')
    fn_chaoxiang  = os.path.join(path_codemap, 'chaoxiang.lst')
    fn_fukuanfangshi = os.path.join(path_codemap, 'fukuanfangshi.lst')
    fn_zhuangxiu = os.path.join(path_codemap, 'zhuangxiu.lst')
    fn_zhuzhaileibie = os.path.join(path_codemap, 'zhuzhaileibie.lst')

    dict_codemap_shiurl = {}
    dict_codemap_shi = {}
    dict_codemap_quxian = {}
    dict_codemap_cengleixing = {}
    dict_codemap_chanquanxingzhi = {}
    dict_codemap_chaoxiang = {}
    dict_codemap_fukuanfangshi = {}
    dict_codemap_zhuangxiu = {}
    dict_codemap_zhuzhaileibie = {}
    def __init__(self):
        self.dict_codemap_cengleixing = public.load_codemap(self.fn_cengleixing)
        self.dict_codemap_chanquanxingzhi = public.load_codemap(self.fn_chanquanxingzhi)
        self.dict_codemap_chaoxiang = public.load_codemap(self.fn_chaoxiang)
        self.dict_codemap_fukuanfangshi = public.load_codemap(self.fn_fukuanfangshi)
        self.dict_codemap_zhuangxiu = public.load_codemap(self.fn_zhuangxiu)
        self.dict_codemap_zhuzhaileibie = public.load_codemap(self.fn_zhuzhaileibie)


if __name__ == "__main__":
    config_logging(logging.DEBUG, filename_log)
    
    constants = Constants()

    fw = open('output.txt', 'w')
    list_dirs = os.listdir('data')
    for fname in list_dirs:
        f = open(os.path.join('data', fname), mode='r', encoding='gbk')
        f_context = f.read()
        list_datalines = f_context.split('\n')
        s_write_buffer = ''
        for line in list_datalines:
            a = public.transform_line(constants, line)
            if a:
                s_write_buffer += '\t'.join(a)
                s_write_buffer += '\n'
                #print(s_write_buffer)
            
        
