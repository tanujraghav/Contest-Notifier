# Contest Notifier

> A `personalized` Twitter Bot that notifies about upcoming Competitive Programming Contests using [CList API](https://clist.by)

**Set Up**

```bash
~ $ wget -O cpnotif-installer "https://raw.githubusercontent.com/tanujraghav/Contest-Notifier/master/install"
~ $ bash cpnotif-installer
```

**Usage**

```bash
~ $ cpnotif -h
usage: cpnotif [-h] [-d DAYS]

A personalized Twitter Bot that notifies about upcoming Competitive Programming Contests using CList API
- by Tanuj Raghav, https://github.com/tanujraghav/Contest-Notifier

optional arguments:
  -h, --help  show this help message and exit
  -d DAYS     number of days to check for contests (default: 6)
```

**Sample Config File**

```bash
[CLIST]
username = johndoe
api_key = yourclistapikey
resources = codechef.com,codeforces.com,topcoder.com
events = (Challenge)|(Codeforces Round)|(SRM)

[Time Zone]
offset = +05:30
name = Asia/Kolkata
code = IST

[Twitter]
api_key = yourtwitterapikey
api_secret_key = yourtwitterapisecretkey
access_token = yourtwitteraccesstoken
access_token_secret = yourtwitteraccesstokensecret
```
