import d6tflow
import pandas as pd

from d6tflow.functional import Flow
d6tflow.d6tcollect.submit = True
flow = Flow()

@flow.step(d6tflow.tasks.TaskCache)
def get_data1(task):
    df = pd.DataFrame({'a':range(3)})
    task.save(df)

@flow.step(d6tflow.tasks.TaskCache)
def get_data2(task):
    df = pd.DataFrame({'a':range(3)})
    task.save(df)

@flow.step(d6tflow.tasks.TaskPqPandas)
@flow.requires({"input1":get_data1, "input2":get_data2})
def use_data(task):
    data = task.inputLoad()
    df1 = data['input1']
    df2 = data['input2']
    df3 = df1.join(df2, lsuffix='1', rsuffix='2')
    df3['b']=df3['a1']*task.multiplier # use task parameter
    task.save(df3)

flow.add_params({'multiplier': d6tflow.IntParameter(default=0)})
use_params = {'multiplier':4}

flow.preview(use_data, params=use_params)

flow.run(use_data, params=use_params, forced_all_upstream=True, confirm=False)
flow.outputLoad(get_data1, params=use_params)