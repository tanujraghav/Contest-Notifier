#!/usr/bin/env python3

from tweepy import OAuthHandler, API
from urllib.parse import quote
from requests import get
from datetime import date, datetime, timedelta
from pytz import timezone

CList = {
    'USERNAME': '<YOUR CLIST USERNAME>',
    'API_KEY': '<YOUR CLIST API KEY>',
    'RESOURCES': '<RESOURCE URLs separated by comma>',
    'EVENTS': '<EVENTS REGEX in parentheses seperated by pipe>'
    }

TZ = {
    'OFFSET': '<YOUR TIMEZONE OFFSET>',
    'NAME': '<YOUR TIMEZONE NAME>',
    'CODE': '<YOUR TIMEZONE CODE>'
    }

Twitter = {
    'API_KEY': '<YOUR TWITTER API KEY>',
    'API_SECRET_KEY': '<YOUR TWITTER API SECRET KEY>',
    'ACCESS_TOKEN': '<YOUR TWITTER ACCESS TOKEN>',
    'ACCESS_TOKEN_SECRET': '<YOUR TWITTER ACCESS TOKEN SECRET>'
    }

auth = OAuthHandler(
    Twitter['API_KEY'],
    Twitter['API_SECRET_KEY']
    )
auth.set_access_token(
    Twitter['ACCESS_TOKEN'],
    Twitter['ACCESS_TOKEN_SECRET']
    )

api = API(auth)

START = date.today()
END = START + timedelta(6)

API_REQUEST = 'https://clist.by:443/api/v2/contest/?username='+CList['USERNAME']+'&api_key='+CList['API_KEY']+'&resource='+CList['RESOURCES']+'&event__regex='+CList['EVENTS']+'&start__gte='+str(START)+'T00%3A00%3A00'+quote(TZ['OFFSET'])+'&start__lte='+str(END)+'T23%3A59%3A59'+quote(TZ['OFFSET'])+'&order_by=start'

RESPONSE = get(API_REQUEST).json()['objects']

def prettify(n):
  n = datetime.strptime(n, '%Y-%m-%dT%H:%M:%S%z')
  n.strftime("%A, %d %B, %R")
  return n.astimezone(timezone(TZ['NAME'])).strftime("%a. %d %B '%y, %R " + TZ['CODE'])

def converter(s):
  d = s // (24 * 3600)
  s = s % (24 * 3600)
  h = s // 3600
  s %= 3600
  m = s // 60
  s %= 60
  ans=''
  if d:
    ans += str(d)+' Day'
    ans += 's ' if d > 1 else ' '
  if h:
    ans += str(h)+' Hour'
    ans += 's ' if h > 1 else ' '
  if m:
    ans += str(m)+' Minute'
    ans += 's ' if m > 1 else ' '
  if s:
    ans += str(s)+' Second'
    ans += 's ' if s > 1 else ' '
  return ans

for i in RESPONSE:
  STATUS = f"""
{i['event']}

{prettify(i['start']+'+0000')}  -  {prettify(i['end']+'+0000')}
{converter(i['duration'])}

Link: {i['href']}

#{i['host'][:-4]} #clist


made with ❤ by https://bit.ly/3zBPp43
  """

  api.update_status(STATUS)
