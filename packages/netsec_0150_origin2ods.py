#coding: utf8
import os,sys,time,logging,logging.handlers,psycopg2.extras,shutil

dbhost = '127.0.0.1'
dbport='5432'
dbuser='etl'
dbpassword='qwer1234~!@#'
dbdatabase='gxddb'
daley_work = 3

# create logs file folder
def config_logging(log_level = logging.DEBUG, filename = 'working.log'):
    rotatingFileHandler = logging.handlers.RotatingFileHandler(
                                            filename = filename,
                                            maxBytes = 1024 * 1024 * 100,
                                            backupCount = 20 )
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(lineno)3d \
%(levelname)-8s %(message)s")
    rotatingFileHandler.setFormatter(formatter)
    logging.getLogger("").addHandler(rotatingFileHandler)
    
    console = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(name)-12s: %(lineno)3d \
%(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)
    logger = logging.getLogger("")
    logger.setLevel(log_level)
    
    #返回所有已打开的文件号
    return [rotatingFileHandler.stream.fileno(), console.stream.fileno()]

def main():
    logger_main = logging.getLogger("main")
    #os.chdir(path_work)
    #logger_main.debug("cd %s" % path_work)
    
    db_conn = psycopg2.connect(host=dbhost, port=dbport, 
                        user=dbuser, password=dbpassword,
                        database=dbdatabase,
                        cursor_factory=psycopg2.extras.DictCursor)
    
    while 1:
        cursor = db_conn.cursor()
        cursor.execute("""select id,fn 
        from s01_status.t_netsec_0105_origin2ods_queue 
        where service_line='netsec' order by id""")
        data = cursor.fetchall()
        for line in data:
            logger_main.info("start %s" % line['fn'])
            try:
                cursor.execute("select s20_ods.fn_netsec_0150_origin2ods('%s')"
                               % line['fn'])
                db_conn.commit()
                logger_main.info("commit %s" % line['fn'])
            except Exception, e:
                logger_main.exception(e)
                #TODO: 写入监控日志——写入错误
                logger_main.error("check it : %s" % s_fullname)
                db_conn.rollback()

        time.sleep(daley_work)


if __name__ == "__main__":
    s_basename = 'netsec_0150_origin2ods'
    path_log = os.path.join('/opt/ETL/LOG','%s.log' % s_basename)
    path_pid = os.path.join('/opt/ETL/PID',"%s.pid" % s_basename)
    keep_fds = config_logging(logging.DEBUG, path_log)
    
    #path_work = os.path.dirname(os.path.abspath(sys.argv[0]))

    #from daemonize import Daemonize
    #后台执行方法，keep_fds参数的意义是，当使用daemonize方式启动进程时，会自动关闭一些已打开的文件号
    #这个参数指定保留哪些不要关闭，当前指定的是日志输出的文件号，如果不指定，则不写日志文件
    #daemon = Daemonize(app=s_basename, pid=path_pid, action=main, keep_fds=keep_fds)
    #daemon.start()
    main()
