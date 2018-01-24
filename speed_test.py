from urllib import request,parse
import time
# simple request
params = parse.urlencode({'text': 'sore throat'})
times=[]
for i in range(0, 100):
    start = time.time()
    request.urlopen('http://localhost:8080/find_matches?' + params).read()
    end = time.time()
    times.append(end-start)
print("Avg. time for simple request:", sum(times)/len(times))

# long text
params = parse.urlencode({'text': 'hi '*1000})
times=[]
for i in range(0, 100):
    start = time.time()
    request.urlopen('http://localhost:8080/find_matches?' + params).read()
    end = time.time()
    times.append(end-start)
print("Avg. time for a very long text: ",sum(times)/len(times))
