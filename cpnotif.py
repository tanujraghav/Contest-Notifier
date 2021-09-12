#!/usr/bin/env python3

from argparse import ArgumentParser, RawTextHelpFormatter
from configparser import ConfigParser
from tweepy import OAuthHandler, API
from urllib.parse import quote
from requests import get
from datetime import date, datetime, timedelta
from pytz import timezone


def getArgs():

  parser = ArgumentParser(usage='%(prog)s [-h] [-d DAYS]',description='A personalized Twitter Bot that notifies about upcoming Competitive Programming Contests using CList API\n- by Tanuj Raghav, https://github.com/tanujraghav/Contest-Notifier',formatter_class=RawTextHelpFormatter)
  parser.add_argument('-d', dest='days', type=int, default=6, help='number of days to check for contests (default: 6)')

  return parser.parse_args()


def getConfig():

  config = ConfigParser()
  config.read("/etc/Contest-Notifier/cpnotif.rc")

  global CLIST, Twitter, TZ

  CLIST = {
    'USERNAME': config['CLIST']['username'],
    'API_KEY': config['CLIST']['api_key'],
    'RESOURCES': config['CLIST']['resources'],
    'EVENTS': config['CLIST']['events']
  }

  Twitter = {
    'API_KEY': config['Twitter']['api_key'],
    'API_SECRET_KEY': config['Twitter']['api_secret_key'],
    'ACCESS_TOKEN': config['Twitter']['access_token'],
    'ACCESS_TOKEN_SECRET': config['Twitter']['access_token_secret']
  }
  
  TZ = {
    'OFFSET': config['Time Zone']['offset'],
    'NAME': config['Time Zone']['name'],
    'CODE': config['Time Zone']['code']
  }


def TwitterAuth():

  global Twitter

  auth = OAuthHandler(
    Twitter['API_KEY'],
    Twitter['API_SECRET_KEY']
  )
  auth.set_access_token(
    Twitter['ACCESS_TOKEN'],
    Twitter['ACCESS_TOKEN_SECRET']
  )

  return API(auth)


def CLISTRequest(L,R):

  global CLIST, TZ

  API_REQUEST = 'https://clist.by:443/api/v2/contest/?username='+CLIST['USERNAME']+'&api_key='+CLIST['API_KEY']+'&resource='+CLIST['RESOURCES']+'&event__regex='+CLIST['EVENTS']+'&start__gte='+str(L)+'T00%3A00%3A00'+quote(TZ['OFFSET'])+'&start__lte='+str(R)+'T23%3A59%3A59'+quote(TZ['OFFSET'])+'&order_by=start'

  return get(API_REQUEST).json()['objects']


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


def notify(buff):

  for i in buff:
    STATUS = f"""
{i['event']}

{prettify(i['start']+'+0000')}  -  {prettify(i['end']+'+0000')}
{converter(i['duration'])}

Link: {i['href']}

#{i['host'][:-4]} #clist


made with ❤ by https://bit.ly/3zBPp43
    """

  return STATUS


if __name__ == "__main__":

  args = getArgs()

  try:
    getConfig()
  except:
    exit("ERROR: corrupt configuration file, see. /etc/Contest-Notifier/cpnotif.rc")

  try:
    api = TwitterAuth()
  except:
    exit("ERROR: unable to get Twitter authentication, please check you access keys")
  
  START = date.today()
  END = START + timedelta(args.days)

  try:
    response = CLISTRequest(START, END)
  except:
    exit("ERROR: unable to connect with CLIST API, please check your access keys")

  status = notify(response)

  try:
    api.update_status(status)
  except:
    exit()
