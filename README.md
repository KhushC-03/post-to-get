# post-to-get
A simple way of completeing post requests in your browser. 

Example Request


```
BASE_URL = 'http://127.0.0.1:5000/'
data = {
    'URL':"Request Url",
    'PAYLOAD':json.dumps({"FormData Name 1":"Form Data Value 1","Form Data Name 2":"Form Data Value 2"})
}

r = requests.post(f'{BASE_URL}/post-to-get',data=data,timeout=4)
redirectURL = r.json()['requesturl']```
