import json
import requests
import time

class monochromator:
    device = {}
    curr_wl = 0

    def doRequest(self, req):
        print('http://' + self.device['ip'] + ':' + self.device['port'] +
              '/flugegeheimen')
        print(json.dumps(req))
        r = requests.post('http://' + self.device['ip'] + ':' + self.device['port'] +
                          '/flugegeheimen', data=json.dumps(req))
        return r.json()

    def getWavelength(self):
        req = {"reqtype": "getWavelength", "subsystem": "MDR"}
        ret = self.doRequest(req)
        print(ret)
        if ret['status'] == 'success':
            if ret['wavelength'] < 340 or ret['wavelength'] > 2520:
                time.sleep(1)
                self.getWavelength()
            self.curr_wl = ret['wavelength']

    def __init__(self, ip_addr, port):
        print('connecting to addrss: %s:%d' %(ip_addr, port))
        self.device = {'ip': ip_addr, 'port': str(port)}
        req_to_Zero = {"reqtype": "setZero", "subsystem": "MDR"}
        ret = self.doRequest(req_to_Zero)
        print(ret)
        time.sleep(20)
        self.getWavelength()

    def setWavelength(self, wavelength):
        req = {"reqtype":"setWavelength","wavelength":wavelength,"subsystem":"MDR"}
        ret = self.doRequest(req)
        print(ret)
        time.sleep(15)
        self.getWavelength()



