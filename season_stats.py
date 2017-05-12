import urllib2
import json

kd_stats = 'C:/Users/greg6750/Documents/IPython Notebooks/NBAproject/kd.json'

with open(kd_stats) as data_file:
    data = json.load(data_file)

for row in data['resultSets'][0]['rowSet']:
    print(row)

##----------------------------------------
##player_id = '201142'
##season = '2016-17'
##seasontype="Regular+Season"
###nba_stats_url = 'http://stats.nba.com/stats/shotchartdetail?AheadBehind=&CFID=&CFPARAMS=&ClutchTime=&Conference=&ContextFilter=&ContextMeasure=FGM&DateFrom=&DateTo=&Division=&EndPeriod=10&EndRange=28800&GameEventID=&GameID=&GameSegment=&GroupID=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&Period=0&PlayerID=%s&PlayerPosition=&PointDiff=&Position=&RangeType=0&RookieYear=&Season=%s&SeasonSegment=&SeasonType=%s&ShotClockRange=&StartPeriod=1&StartRange=0&StarterBench=&TeamID=0&VsConference=&VsDivision=' % (player_id, season, seasontype)
###'http://stats.nba.com/stats/playergamelog?DateFrom=&DateTo=&LeagueID=00&PlayerID=201142&Season=2016-17&SeasonType=Regular+Season'
##nba_stats_url = 'http://stats.nba.com/stats/playergamelog?DateFrom=&DateTo=&LeagueID=00&PlayerID=201142&Season=2016-17&SeasonType=Regular+Season'#'http://stats.nba.com/stats/playerdashboardbyyearoveryear?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Scoring&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=%s&PlusMinus=N&Rank=N&Season=%s&SeasonSegment=&SeasonType=%s&ShotClockRange=&Split=yoy&VsConference=&VsDivision='% (player_id, season, seasontype)
##headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
###headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'}
##



##request = urllib2.Request(nba_stats_url,None,headers)
##print(request)
##stats=urllib2.urlopen(request)
##print(stats)
##data=json.loads(stats)
##print(data)
##
##for row in data['resultSets'][1]['rowSet']:
##    print(row)

