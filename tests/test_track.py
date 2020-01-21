import pytest
import importlib, requests
from bs4 import BeautifulSoup as bs
import pandas as pd

import d6tcollect
d6tcollect.submit = True
d6tcollect.ignore_errors = False
d6tcollect.host = 'http://192.168.33.10:5000'
d6tcollect.host = 'https://d6tpipe-staging-demo.herokuapp.com'
d6tcollect.host = 'http://localhost:8080'
d6tcollect.endpoint = '/v1/api/content/'

url_base = d6tcollect.host+'/v1/api'

import d6tcollect.track

def url(endpoint):
    return url_base+endpoint

def run(endpoint,method='get',body=None):
    fun = getattr(requests,method)
    if method in ['post','put','patch']:
        return fun(url(endpoint), json=body).json()
    else:
        return fun(url(endpoint)).json()

def runpost(url,body=None):
    return run(url,method='post',body=body)

@pytest.fixture
def cleanup():
    runpost('/utest-wipeall')
    yield True
    runpost('/utest-wipeall')

def test_TrackAppUserEmail(cleanup):
    htmltext = '''
    <html>
    <body>
    Hello world!
    <a href="https://www.deepmind.com">click here</a>
    <img src="#">
    </body>
    </html>
    '''

    tracker = d6tcollect.track.TrackAppUserEmail(htmltext,"app-utest","utest-event1")
    cfg_receiver = ['a@b.com','c@d.com']
    cfg_nreceiver = len(cfg_receiver)
    cfg_nlinks = len(bs(htmltext, "html.parser").findAll('a'))
    user_content = tracker.process_all(cfg_receiver)

    # test code
    for k,v in user_content.items():
        soup = bs(v, "html.parser")
        assert all([d6tcollect.host in a['href'] for a in soup.findAll('a')])
        assert v.count('/content/img/')==1

    # test processing
    for k,v in user_content.items():
        soup = bs(v, "html.parser")
        for a in soup.findAll('a'):
            r = requests.get(a['href'])
            assert r.status_code==200
        for i in soup.findAll('img'):
            if 'http' in i['src']:
                r = requests.get(i['src'])
                assert r.status_code==200

    r = runpost('/query/content')
    assert len(r)==cfg_nreceiver*2
    dft = pd.DataFrame(list(r))
    t = dft['userid'].unique().tolist()
    assert len(t)==cfg_nreceiver
    assert t==cfg_receiver

    t = dft['action'].unique().tolist()
    assert t==['open-link','open-email']
