# -*- coding: utf-8 -*-
""" 
@Time    : 2023-01-31 10:25
@Author  : zck
@FileName: proxydemo.py
@SoftWare: PyCharm
"""


from queue import Queue
import requests

class cyProxy:
    def __init__(self, getProxy=None, proxyList=[], max=3, maxerr=2):
        '''

        :param getProxy: 返回一个代理的列表的函数
        :param proxyList: 初始化代理输入列表
        :param max: 最大的代理请求连接数
        :param maxerr: 最大的代理错误数
        '''
        self._proxies = {}
        self._badproxy = set('')
        self.maxerr = maxerr
        self._max = max
        self._getproxy = getProxy
        self._proxyList = proxyList
        self._Qproxy = Queue(maxsize=max * 5)
        self._putProxyDict()
        self._putProxy()

    def _putProxyDict(self):
        if self._getproxy != None:
            self._proxyList += self._getproxy()
        while 1:
            if len(self._proxyList) + self._Qproxy.qsize() == 0:
                if len(self._proxies) == 0:
                    raise Exception("代理不够了")
                return
            if len(self._proxyList) == 0:
                return
            s = self._proxyList.pop()
            if s in self._badproxy:
                if len(self._proxyList) == 0:
                    break
                continue
            self._proxies[s] = [self._max, 0]
            if len(self._proxyList) == 0:
                break

    def _putProxy(self):
        while 1:
            off2 = 0
            off = 1
            for k, v in self._proxies.items():
                if self._Qproxy.full():
                    off = 0
                    break
                elif v[0] > 0:
                    off2 = 1
                    self._Qproxy.put(k)
                    v[0] -= 1
            if off == 0 or off2 == 0:
                break

    def get(self):
        if self._Qproxy.empty():
            self._putProxyDict()
            self._putProxy()
            if self._Qproxy.empty():
                return None
        proxy = self._Qproxy.get()
        if self._Qproxy.qsize() < 4:
            self._putProxyDict()
            self._putProxy()
        return proxy

    def updata(self, proxy):
        if proxy not in self._proxies:
            return
        self._proxies[proxy][0] += 1
        print(self._proxies)

    def puterr(self, proxies):
        if proxies not in self. _proxies:
            return
        self._proxies[proxies][1] += 1
        if self._proxies[proxies][1] >= self.maxerr:
            self._proxies.pop(proxies)
            self._badproxy.add(proxies)


class _error:
    def __init__(self, id, error, request, data, errNum):
        self.id = id
        self.error = error
        self.request = request
        self.requestData = data
        self.errNum = errNum

a = 0
def getProxies():
    global a
    # req = cyRequest.get("http://101.35.218.236:5010/get")
    # 下面返回 101.36.33.33:8080
    # text = req.response.text
    # 设置https代理

    # 设置http代理
    # proxy = "http://" + text

    # 返回一个代理给线程池（可以返回多个）

    if a == 0:
        a += 1
        return ["https://192.168.32.22:8090"]
    elif a == 2 :
        return ["https://192.168.0.53:8090"]
    else:
        return [""]

class Request:
    def __init__(self,url,errnum):
        self.url = url
        self.errnum = errnum



class zckRequest:
    def __init__(self,header,cookie):
        self.header = header
        self.cookie = cookie

    def get(self):
        self._get()

    def _get(self):
        pass





def main():


    proxylist = cyProxy(
        # 设置获取代理的函数
        getProxy= getProxies,
        # 最大有3个请求共同使用这个代理（默认3个）
        max=3,
        # 这个代理最大错误几次后会被舍弃
        maxerr=3
    )

    p = proxylist.get()


    print(proxylist.get())                                  #获取代理


    proxylist.updata("https://192.168.32.22:8090")          #更新代理
    proxylist.updata("https://192.168.32.22:8090")
    proxylist.updata("https://192.168.32.22:8090")

    print(proxylist.get())





if __name__ == '__main__':
    main()









