
#-*- coding:utf-8 -*-

import json
import urllib2

if __name__ == '__main__':
    
    print "split rest test ..."
    
    jsonReq = {"body":[{"cityName":"北京市","addrs":[{"districtName":"丰台区","communityName":"富锦嘉园"},{"districtName":"丰台区","communityName":"蒲安北里"}]},{"cityName":"大连市","addrs":[{"districtName":"大连经济技术开发区","communityName":"润海园中区"},{"districtName":"沙河口区","communityName":"锦云南园"},{"districtName":"金州区","communityName":"金沙小区"}]}]} 
    
    data = json.dumps(jsonReq)
    
    req = urllib2.Request("http://localhost:8080/AddrRevaluation/rest/splits/getCommunityInfo")
    
    req.add_header('Content-type', 'application/json')
    req.method = "POST"
    
    try:
        print '请求报文 %s%s' % (json.dumps(data, ensure_ascii=False),'\n')
        response = urllib2.urlopen(req, data=data, timeout=60)
        rjson = response.read()
        print '响应报文 %s%s' % (rjson, '\n')
        
    except Exception , e:
        print e
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    