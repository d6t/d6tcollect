'''

Much like websites, this library collects anonymous usage statistics.
It ONLY collects import and function call events. It does NOT collect any of your data.
Example: {'profile': 'prod', 'package': 'd6tmodule', 'module': 'd6tmodule.utils', 'classModule': 'd6tmodule.utils.MyClass', 'class': 'MyClass',
    'function': 'MyClass0.myfunction_1', 'functionModule': 'd6tmodule.utils.MyClass.myfunction_1', 'event': 'call', 'params': {'args': 1, 'kwargs': 'another'}}
For privacy notice see https://www.databolt.tech/index-terms.html#privacy

'''

import queue
from datetime import datetime
from datetime import timedelta
import sys
import os
import urllib.request

import json
import threading
import uuid
import sqlite3
from pathlib import Path
import hashlib

submit = True
ignore_errors = True
profile = 'prod'

host = 'http://localhost:8080'
host = os.environ.get('D6TCOLLECT_SVR', 'https://d6tcollect.databolt.tech')
endpoint = '/v1/api/collect'
source = 'd6tcollect'

# NEED TO PASTE THIS CODE SOMEWHERE ELSE RELEVANT


def create_db():
    """ Creates a db if it doesn't already exists 
    and returns the path to it """
    collect_folder = ".d6tcollect"
    db_name = "collect.sqlite"
    db_path = Path.home() / collect_folder
    db_path.mkdir(parents=True, exist_ok=True)
    db_path = str(db_path / db_name)
    events_table = """CREATE TABLE IF NOT EXISTS events (
            id text PRIMARY KEY,
            date text NOT NULL,
            payload text NOT NULL,
            submit integer NOT NULL
        );"""
    events_submitted_table = """CREATE TABLE IF NOT EXISTS events_submitted (
            id integer PRIMARY KEY,
            date text NOT NULL,
            payload text NOT NULL
        );"""
    date_submitted_table = """CREATE TABLE IF NOT EXISTS date_submitted (
            id integer PRIMARY KEY,
            date text NOT NULL,
            datetime text NOT NULL
        );"""
    with sqlite3.connect(db_path) as conn:
        conn.execute(events_table)
        conn.execute(events_submitted_table)
        conn.execute(date_submitted_table)

    return db_path


DB_PATH = create_db()


def daily_summary_sent():
    select_statement = """ 
        select date from date_submitted where date=?
    """
    record = None
    with get_connection() as conn:
        cur = conn.cursor()
        record = cur.execute(
            select_statement, (datetime.now().date().isoformat(),)
        ).fetchall()

    return len(record) != 0


def get_payloads():
    select_statement = """ 
        select date, payload from events
    """
    payloads = None
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(select_statement)
        payloads = cur.fetchall()
    return payloads


def move_payloads(payloads, delete_original_payloads=True):
    insert_statement_submitted = """
        insert into events_submitted(date, payload)
        values(?, ?)
    """

    delete_statement_events = """ 
        delete from events where date=? and payload=?
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.executemany(insert_statement_submitted, payloads)

        if delete_original_payloads:
            cur.executemany(delete_statement_events, payloads)

        conn.commit()

def today():
    return datetime.now().strftime("%Y-%m-%d")

def insert_date_submitted():
    date_time_submitted = datetime.now().isoformat()
    date_submitted = datetime.now().date().isoformat()

    insert_statement = """
        insert into date_submitted(date, datetime)
        values(?, ?)
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(insert_statement, (date_submitted, date_time_submitted))


daily_submits_queue = queue.Queue(maxsize=-1)


def DailySubmission(q):
    payload = q.get()
    while payload != "done":
        _request(payload[1], from_db=True)
        payload = q.get()


def send_daily_summary(forced=False):
    if daily_summary_sent() and not forced:
        return
    #print("send_daily_summary")
    payloads = get_payloads()

    for payload in payloads:
        # daily_submits_queue.put(payload)
        _submit(payload[1], put_in_queue=False, from_db=True)
    move_payloads(payloads, delete_original_payloads=True)

    if payloads:
        insert_date_submitted()


payload_queue = queue.Queue(maxsize=-1)


def get_connection():
    path = create_db()
    return sqlite3.connect(path)


def insert_event(id, date, payload, submitted):
    submitted = 1 if submitted else 0

    payload = json.dumps(payload, default=str).encode('utf-8')
    insert_statement = """ 
        INSERT or IGNORE INTO events(id, date, payload, submit)
        VALUES (?, ?, ?, ?)
        """
    with get_connection() as conn:
        conn.execute(insert_statement, (id, date, payload, submitted))
        conn.commit()


def insert_payload(payload):
    id = hashlib.md5(str(payload.values()).encode('utf-8')).hexdigest()
    date = datetime.now().isoformat()
    submitted = False

    insert_event(id, date, payload, submitted)


def Writer(payload_queue):
    main_thread_alive = True

    while(main_thread_alive):
        for i in threading.enumerate():
            if i.name == "MainThread":
                main_thread_alive = i.is_alive()
        try:
            payload = payload_queue.get()
            # print("payload: ", payload)
            if payload == "EXIT":
                break

            # insert payload in db
            insert_payload(payload)
        except queue.Empty:
            pass

    while not payload_queue.empty():
        payload = payload_queue.get()
        insert_payload(payload)


_t = threading.Thread(target=Writer, args=(payload_queue,))
_t.daemon = True
_t.start()


def _request(payload, from_db):
    try:
        if from_db:
            req = urllib.request.Request(
                host + endpoint, data=payload,
                headers={'content-type': 'application/json', "Source": source})

        else:
            payload['uuid'] = str(uuid.UUID(int=uuid.getnode())).split('-')[-1]
            req = urllib.request.Request(host + endpoint, data=json.dumps(payload, default=str).encode(
                'utf-8'), headers={'content-type': 'application/json', "Source": source})
        urllib.request.urlopen(req)
    except Exception as e:
        if ignore_errors:
            pass
        else:
            raise e


def _submit(payload, put_in_queue=True, from_db=False):
    if put_in_queue:
        payload_queue.put(payload)
    else:
        _t = threading.Thread(target=_request, args=(
            payload, from_db))
        _t.daemon = True
        _t.start()
        _t.join()


def init(_module):

    module = _module.split('.')
    payload = {
        'profile': profile,
        'package': module[0] if len(module) > 0 else module,
        'module': _module,
        'event': 'import',
        'date_of_collection': today()
    }
    _submit(payload)


def collect(func):
    def wrapper(*args, **kwargs):
        # print("kwargs",  ",".join(kwargs))
        if submit == False:
            return func(*args, **kwargs)

        module = func.__module__.split('.')
        payload = {
            'profile': profile,
            'package': module[0] if len(module) > 0 else module,
            'module': func.__module__,
            'classModule': None,
            'class': None,
            'function': func.__qualname__,
            'functionModule': ".".join([func.__module__, func.__qualname__]),
            'event': 'call',
            'params': {'args': len(args), 'kwargs': ",".join(kwargs)},
            'date_of_collection': today()
        }
        payload['uuid'] = str(uuid.UUID(int=uuid.getnode())).split('-')[-1]
        # print(payload)
        _submit(payload)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            payload['event'] = 'exception'
            payload['exceptionType'] = e.__class__.__name__
            payload['exceptionMsg'] = str(e)
            _submit(payload)
            raise e

    return wrapper


def get_og_class(cls, func):
    ''' og_class is the original implementor of the function func'''
    func_implementor = func.__qualname__.split(".")[0]
    for _cls in cls.__mro__:
        if _cls.__name__ == func_implementor:
            return _cls


def _collectClass(func):
    def wrapper(self, *args, **kwargs):
        if submit == False:
            return func(self, *args, **kwargs)
        og_class = get_og_class(self.__class__, func)

        if og_class is None:
            # This should never happen but just to be sure
            return func(self, *args, **kwargs)

        module = func.__module__.split('.')
        payload = {
            'profile': profile,
            'package': module[0] if len(module) > 0 else module,
            'module': og_class.__module__,
            'classModule': ".".join([og_class.__module__, og_class.__qualname__]),
            'class': og_class.__qualname__,
            'function': func.__qualname__,
            'functionModule': ".".join([og_class.__module__, og_class.__name__, func.__name__]),
            'event': 'call',
            'params': {'args': len(args), 'kwargs': ",".join(kwargs)},
            'date_of_collection': today()
        }
        payload['uuid'] = str(uuid.UUID(int=uuid.getnode())).split('-')[-1]
        # print(payload)
        _submit(payload)
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            payload['event'] = 'exception'
            payload['exceptionType'] = e.__class__.__name__
            payload['exceptionMsg'] = str(e)
            _submit(payload)
            raise e

    return wrapper


class Collect(type):
    def __new__(cls, name, bases, namespace, **kwds):
        namespace = {k: v if k.startswith('_') else _collectClass(
            v) for k, v in namespace.items()}
        return type.__new__(cls, name, bases, namespace)


send_daily_summary()
