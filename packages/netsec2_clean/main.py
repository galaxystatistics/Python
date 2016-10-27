#coding:utf8
import os, sys, time, logging.handlers
from modules import public
from pyhdfs import HdfsClient

def get_main_path():
    return os.path.dirname(__file__)

filename_log = 'netsec2_clean.log'
path_main = get_main_path()
path_codemap = os.path.join(path_main, 'codemap')

hosts_hdfs = '192.168.10.121:50070'
dir_dataroot = '/user/hadoop/HADOOP_DATA'

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
    fn_shi_url = os.path.join(path_codemap, 'shi_url.lst')
    fn_shi = os.path.join(path_codemap, 'shi.lst')
    fn_quxian = os.path.join(path_codemap, 'quxian.lst')
    fn_cengleixing = os.path.join(path_codemap, 'cengleixing.lst')
    fn_chanquanxingzhi = os.path.join(path_codemap, 'chanquanxingzhi.lst')
    fn_chaoxiang  = os.path.join(path_codemap, 'chaoxiang.lst')
#     fn_fukuanfangshi = os.path.join(path_codemap, 'fukuanfangshi.lst')
    fn_jianzhuleibie = os.path.join(path_codemap, 'jianzhuleibie.lst')
    fn_zhuangxiu = os.path.join(path_codemap, 'zhuangxiu.lst')
    fn_zhuzhaileibie = os.path.join(path_codemap, 'zhuzhaileibie.lst')

    dict_codemap_shiurl = {}
    dict_codemap_shi = {}
    dict_codemap_quxian = {}
    dict_codemap_cengleixing = {}
    dict_codemap_chanquanxingzhi = {}
    dict_codemap_chaoxiang = {}
#     dict_codemap_fukuanfangshi = {}
    dict_codemap_jianzhuleibie = {}
    dict_codemap_zhuangxiu = {}
    dict_codemap_zhuzhaileibie = {}
    def __init__(self):
        logger_constants = logging.getLogger("Constants")
        self.dict_codemap_shiurl = public.load_codemap(self.fn_shi_url)
        logger_constants.info('load key map file : %s' % self.fn_shi_url)
        self.dict_codemap_shi = public.load_codemap(self.fn_shi)
        logger_constants.info('load key map file : %s' % self.fn_shi)
        self.dict_codemap_quxian = public.load_codemap(self.fn_quxian)
        logger_constants.info('load key map file : %s' % self.fn_quxian)
        self.dict_codemap_cengleixing = public.load_codemap(self.fn_cengleixing)
        logger_constants.info('load key map file : %s' % self.fn_cengleixing)
        self.dict_codemap_chanquanxingzhi = public.load_codemap(self.fn_chanquanxingzhi)
        logger_constants.info('load key map file : %s' % self.fn_chanquanxingzhi)
        self.dict_codemap_chaoxiang = public.load_codemap(self.fn_chaoxiang)
        logger_constants.info('load key map file : %s' % self.fn_chaoxiang)
#         self.dict_codemap_fukuanfangshi = public.load_codemap(self.fn_fukuanfangshi)
#         logger_constants.info('load key map file : %s' % self.fn_fukuanfangshi)
        self.dict_codemap_jianzhuleibie = public.load_codemap(self.fn_jianzhuleibie)
        logger_constants.info('load key map file : %s' % self.fn_jianzhuleibie)
        self.dict_codemap_zhuangxiu = public.load_codemap(self.fn_zhuangxiu)
        logger_constants.info('load key map file : %s' % self.fn_zhuangxiu)
        self.dict_codemap_zhuzhaileibie = public.load_codemap(self.fn_zhuzhaileibie)
        logger_constants.info('load key map file : %s' % self.fn_zhuzhaileibie)


if __name__ == "__main__":
    config_logging(logging.DEBUG, filename_log)
    logger = logging.getLogger('main')
    logger_pyhdfs = logging.getLogger('pyhdfs')
    logger_pyhdfs.setLevel(logging.ERROR)
    logger_requests = logging.getLogger('requests')
    logger_requests.setLevel(logging.ERROR)
    
    constants = Constants()
    logger.info('constants loaded')
    logger.info('init : hosts_hdfs   = %s' % hosts_hdfs)
    logger.info('init : dataroot     = %s' % dir_dataroot)
    logger.info('init : path main    = %s' % path_main)
    logger.info('init : path codemap = %s' % path_codemap)
    client = HdfsClient(hosts = hosts_hdfs)
    logger.info('connect hdfs')
    logger.info('---- start working ----')
#     type='DIRECTORY'   type='FILE'
    while 1:
        list_dirs = [ x['pathSuffix'] for x in client.list_status(dir_dataroot) if x['type']=='DIRECTORY' ]
        list_dirs.sort()
        for subdir in list_dirs:
            dir_subdata = os.path.join(dir_dataroot, subdir)
            logger.debug('data path : %s' % dir_subdata)
            dir_subdata_cleaned = os.path.join(dir_subdata, 'cleaned4netsec')
            logger.debug('data path for cleaned files : %s' % dir_subdata_cleaned)
            list_subdir_date = [ x['pathSuffix'] for x in client.list_status(dir_subdata) if x['type']=='FILE' ]
            if len(list_subdir_date)>0:
                if not client.exists(dir_subdata_cleaned):
                    client.mkdirs(dir_subdata_cleaned)
                    logger.debug('mkdir dir for cleaned files : %s' % dir_subdata_cleaned)
            
            list_subdir_date_cleaned = [ x['pathSuffix'] for x in client.list_status(dir_subdata_cleaned) if x['type']=='FILE' ]
            
            list_subdir_date.sort()
            for fname in list_subdir_date:
                if fname in list_subdir_date_cleaned:
#                     #TODO: to debug
#                     if client.exists(os.path.join(dir_subdata_cleaned, fname)):
#                         print (os.path.join(dir_subdata_cleaned, fname))
#                         client.delete(os.path.join(dir_subdata_cleaned, fname))
                    logger.debug('has been cleaned, ignore this file : %s' % fname)
                    continue
                s_guapairiqi = public.parse_datetime(fname,
                                            format_from='%Y-%m-%d-%H-%M.txt')
                f_fullname = os.path.join(dir_subdata, fname)
                logger.debug('doing file : %s' % f_fullname)
                f = client.open(f_fullname)
                try:
                    f_context = f.read().decode('gbk')
                except UnicodeDecodeError as e:
                    logger.error('decode error : %s' % f_fullname)
                    logger.error(e)
                    dir_error = os.path.join(dir_subdata, 'error_cleaning')
                    if not client.exists(dir_error):
                        client.mkdirs(dir_error)
                        logger.debug('mkdir dir for error files : %s' % dir_error)
                    #TODO: if success delete error files
                    fname_error = os.path.join(dir_error, fname)
                    if not client.exists(fname_error):
                        client.create(fname_error, None)
                        logger.warn('create error flag file : %s' % fname_error)
                    continue
                finally:
                    f.close()
                    
                list_datalines = f_context.split('\n')
                s_write_buffer = ''
                for line in list_datalines:
                    a = public.transform_line(constants, line)
                    if a:
                        a.append(s_guapairiqi)
                        s_write_buffer += '\t'.join(a)
                        s_write_buffer += '\n'
                
                s_write_buffer = s_write_buffer.encode(encoding='utf_8')
                fname_cleaned = os.path.join(dir_subdata_cleaned, fname)
                
                client.create(fname_cleaned, s_write_buffer)
                logger.info('clean ok : %s' % fname_cleaned)
            
        logger.debug('sleep %s s' % delay_sleep)
        time.sleep(delay_sleep)
