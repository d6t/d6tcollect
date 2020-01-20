import requests

from bs4 import BeautifulSoup as bs

import d6tcollect

class TrackAppUserEmail(object):
    def __init__(self, bodyhtml, appid, target, appversion=None, args=None):
        self.bodyhtml = bodyhtml
        self.appid = appid
        self.target = target
        self.appversion = appversion
        self.args = args

    def link_replace(self,userid,username,bodyhtml=None):
        soup = bs(self.bodyhtml if bodyhtml is None else bodyhtml, "html.parser" )
        for a in soup.findAll('a'):
            if 'http' in a['href']:
                link_old = a['href']
                url = d6tcollect.host + d6tcollect.endpoint + 'link'
                payload = {
                    "userid": userid,
                    "username": username,
                    "appid": self.appid,
                    "appversion": self.appversion,
                    "target": self.target,
                    "args": {**self.args,**{'url':link_old}}
                }
                hashid = requests.post(url, json=payload).json()['hashid']
                a['href'] = f'{url}/{hashid}'
        return str(soup)

    def img_insert(self,userid,username,bodyhtml=None):
        url = d6tcollect.host + d6tcollect.endpoint + 'img'
        payload = {
            "userid": userid,
            "username": username,
            "appid": self.appid,
            "appversion": self.appversion,
            "target": self.target,
            "args": self.args
        }
        hashid = requests.post(url, json=payload).json()['hashid']
        src = f'<img href="{url}/{hashid}">'
        bodyhtml = self.bodyhtml if bodyhtml is None else bodyhtml
        bodyhtml = self.bodyhtml.replace('</body>',f'{src}</body>')
        return bodyhtml

    def process_all(self,recipients):
        return {email: self.img_insert(email,email,self.link_replace(email,email)) for email in recipients}
