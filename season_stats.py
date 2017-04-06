import urllib2
import json


player_id = '201142'
season = '2016-17'
seasontype="Regular+Season"
#nba_stats_url = 'http://stats.nba.com/stats/shotchartdetail?AheadBehind=&CFID=&CFPARAMS=&ClutchTime=&Conference=&ContextFilter=&ContextMeasure=FGM&DateFrom=&DateTo=&Division=&EndPeriod=10&EndRange=28800&GameEventID=&GameID=&GameSegment=&GroupID=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&Period=0&PlayerID=%s&PlayerPosition=&PointDiff=&Position=&RangeType=0&RookieYear=&Season=%s&SeasonSegment=&SeasonType=%s&ShotClockRange=&StartPeriod=1&StartRange=0&StarterBench=&TeamID=0&VsConference=&VsDivision=' % (player_id, season, seasontype)
nba_stats_url = 'http://stats.nba.com/stats/playerdashboardbyyearoveryear?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Scoring&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=%s&PlusMinus=N&Rank=N&Season=%s&SeasonSegment=&SeasonType=%s&ShotClockRange=&Split=yoy&VsConference=&VsDivision='% (player_id, season, seasontype)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'}

request = urllib2.Request(nba_stats_url,None,headers)
stats=urllib2.urlopen(request)
data=json.load(stats)
print(data)

for row in data['resultSets'][1]['rowSet']:
    print(row)

