import pp
import pandas as pd
from draw_trial import *
test = DrawSys()
trials = 10 ** 4
job_server = pp.Server()
s_time = time()
jobs = []
for i in range(10**3):
    jobs.append(job_server.submit(test.f1,args=(trials,), modules=("numpy",)))

results = [job() for job in jobs]
e_time = time()
job_server.destroy()
results = pd.DataFrame(results)
means = results.mean(axis=0)
result_fn = test_fn()
print(means)
print("Run time: %s s" % (e_time-s_time))

##### The two methods are similar
print("=========================================")
trials = 10**7
job_server = pp.Server()
s_time = time()
results = job_server.submit(test.f1,args=(trials,), modules=("numpy",))
results = results()
e_time = time()

print(results)
print("Run time: %s s" % (e_time-s_time))