"""-----------------------------------------------------------------------------
Name:        single_player_shotchart.py
Purpose:     This script creates an NBA shot chart that can be visualized in
             ArcGIS.
Author:      Gregory Brunner, Esri
Created:     October 1, 2015
Last Update: August 16, 2016
-----------------------------------------------------------------------------"""

from __future__ import division

#import urllib2
#import json
import requests
import os
import datetime
import time
#from fake_useragent import UserAgent


import arcpy

arcpy.env.overwriteOutput = True

fc_fields = ("SHAPE@XY","GRID_TYPE","GAME_ID","GAME_EVENT_ID","PLAYER_ID","PLAYER_NAME","TEAM_ID",
    "TEAM_NAME","PERIOD","MINUTES_REMAINING","SECONDS_REMAINING","EVENT_TYPE",
    "ACTION_TYPE","SHOT_TYPE","SHOT_ZONE_BASIC","SHOT_ZONE_AREA",
    "SHOT_ZONE_RANGE","SHOT_DISTANCE","LOC_X","LOC_Y","SHOT_ATTEMPTED_FLAG",
    "SHOT_MADE_FLAG", "THREE", "GAME_DATE", "SEASON_DATE")

#game_dict = {'0021600270': datetime.datetime(2016, 11, 30, 0, 0), '0021600820': datetime.datetime(2017, 2, 13, 0, 0), '0021601142': datetime.datetime(2017, 4, 2, 0, 0), '0021601000': datetime.datetime(2017, 3, 14, 0, 0), '0021600415': datetime.datetime(2016, 12, 19, 0, 0), '0021600740': datetime.datetime(2017, 2, 1, 0, 0), '0021600908': datetime.datetime(2017, 3, 2, 0, 0), '0021600255': datetime.datetime(2016, 11, 28, 0, 0), '0021600433': datetime.datetime(2016, 12, 21, 0, 0), '0021600399': datetime.datetime(2016, 12, 17, 0, 0), '0021600341': datetime.datetime(2016, 12, 9, 0, 0), '0021600235': datetime.datetime(2016, 11, 25, 0, 0), '0021600555': datetime.datetime(2017, 1, 7, 0, 0), '0021600211': datetime.datetime(2016, 11, 22, 0, 0), '0021600195': datetime.datetime(2016, 11, 20, 0, 0), '0021600473': datetime.datetime(2016, 12, 27, 0, 0), '0021600861': datetime.datetime(2017, 2, 24, 0, 0), '0021600178': datetime.datetime(2016, 11, 18, 0, 0), '0021600946': datetime.datetime(2017, 3, 7, 0, 0), '0021600459': datetime.datetime(2016, 12, 25, 0, 0), '0021601100': datetime.datetime(2017, 3, 27, 0, 0), '0021600596': datetime.datetime(2017, 1, 13, 0, 0), '0021600357': datetime.datetime(2016, 12, 11, 0, 0), '0021600513': datetime.datetime(2017, 1, 2, 0, 0), '0021600164': datetime.datetime(2016, 11, 16, 0, 0), '0021600373': datetime.datetime(2016, 12, 13, 0, 0), '0021600112': datetime.datetime(2016, 11, 9, 0, 0), '0021600011': datetime.datetime(2016, 10, 26, 0, 0), '0021600079': datetime.datetime(2016, 11, 5, 0, 0), '0021600973': datetime.datetime(2017, 3, 11, 0, 0), '0021601135': datetime.datetime(2017, 3, 31, 0, 0), '0021600507': datetime.datetime(2016, 12, 31, 0, 0), '0021600932': datetime.datetime(2017, 3, 5, 0, 0), '0021600307': datetime.datetime(2016, 12, 5, 0, 0), '0021600893': datetime.datetime(2017, 2, 28, 0, 0), '0021601112': datetime.datetime(2017, 3, 29, 0, 0), '0021601028': datetime.datetime(2017, 3, 18, 0, 0), '0021600690': datetime.datetime(2017, 1, 26, 0, 0), '0021600916': datetime.datetime(2017, 3, 3, 0, 0), '0021600064': datetime.datetime(2016, 11, 2, 0, 0), '0021600813': datetime.datetime(2017, 2, 11, 0, 0), '0021600727': datetime.datetime(2017, 1, 31, 0, 0), '0021600529': datetime.datetime(2017, 1, 4, 0, 0), '0021601159': datetime.datetime(2017, 4, 4, 0, 0), '0021600634': datetime.datetime(2017, 1, 18, 0, 0), '0021600445': datetime.datetime(2016, 12, 23, 0, 0), '0021600750': datetime.datetime(2017, 2, 3, 0, 0), '0021600712': datetime.datetime(2017, 1, 29, 0, 0), '0021601091': datetime.datetime(2017, 3, 26, 0, 0), '0021600581': datetime.datetime(2017, 1, 11, 0, 0), '0021600621': datetime.datetime(2017, 1, 16, 0, 0), '0021600610': datetime.datetime(2017, 1, 15, 0, 0), '0021600487': datetime.datetime(2016, 12, 29, 0, 0), '0021600301': datetime.datetime(2016, 12, 4, 0, 0), '0021600242': datetime.datetime(2016, 11, 26, 0, 0), '0021601225': datetime.datetime(2017, 4, 12, 0, 0), '0021600569': datetime.datetime(2017, 1, 9, 0, 0), '0021601198': datetime.datetime(2017, 4, 9, 0, 0), '0021600040': datetime.datetime(2016, 10, 30, 0, 0), '0021600147': datetime.datetime(2016, 11, 14, 0, 0), '0021600097': datetime.datetime(2016, 11, 7, 0, 0), '0021600382': datetime.datetime(2016, 12, 14, 0, 0), '0021600767': datetime.datetime(2017, 2, 5, 0, 0), '0021600021': datetime.datetime(2016, 10, 28, 0, 0), '0021601062': datetime.datetime(2017, 3, 22, 0, 0), '0021600224': datetime.datetime(2016, 11, 23, 0, 0), '0021600141': datetime.datetime(2016, 11, 13, 0, 0), '0021600069': datetime.datetime(2016, 11, 3, 0, 0), '0021600540': datetime.datetime(2017, 1, 5, 0, 0), '0021600796': datetime.datetime(2017, 2, 9, 0, 0), '0021600845': datetime.datetime(2017, 2, 15, 0, 0), '0021600962': datetime.datetime(2017, 3, 9, 0, 0), '0021601186': datetime.datetime(2017, 4, 7, 0, 0), '0021600880': datetime.datetime(2017, 2, 26, 0, 0), '0021601015': datetime.datetime(2017, 3, 16, 0, 0), '0021600673': datetime.datetime(2017, 1, 23, 0, 0), '0021601049': datetime.datetime(2017, 3, 20, 0, 0), '0021600686': datetime.datetime(2017, 1, 25, 0, 0), '0021601167': datetime.datetime(2017, 4, 5, 0, 0), '0021600126': datetime.datetime(2016, 11, 11, 0, 0), '0021600770': datetime.datetime(2017, 2, 6, 0, 0)}

def get_game_date_from_box(game_id):
    box_url = 'http://stats.nba.com/stats/boxscoresummaryv2?GameID='+ str(game_id) #
    u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
    headers = {'User-Agent': u_a}#'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'}
    box_response = requests.get(box_url, headers=headers)
    data = box_response.json()
    for row in data['resultSets'][0]['rowSet']:
        datestring = row[0]
        print(datestring[0:10])
        date = datetime.datetime.strptime(datestring[0:10], '%Y-%m-%d')

    return date

def create_date_dict(fc):
    values = [row[0] for row in arcpy.da.SearchCursor(fc, "GAME_ID")]
    unique_game_ids = list(set(values))
    game_dict = {}

    print(unique_game_ids)
    count = 0
    for val in unique_game_ids:
        print(count)
        count=count+1
        date = get_game_date_from_box(val)
        print(date)
        game_dict[str(val)] =  date
        time.sleep(5)


    print(game_dict)
    return game_dict

def get_last_game(player_id, season, playoffs, away):

    master_shots=[]
    coords = []
    if playoffs:
        seasontype="Playoffs"
    else:
        seasontype="Regular+Season"
    seasonindicator=0
    #nba_call_url = 'http://stats.nba.com/stats/shotchartdetail?Season=%s&SeasonType=%s&TeamID=0&PlayerID=%s&GameID=&Outcome=&Location=&Month=0&SeasonSegment=&DateFrom=&Dateto=&OpponentTeamID=0&VsConference=&VsDivision=&Position=&RookieYear=&GameSegment=&Period=0&LastNGames=0&ContextMeasure=FGA' % (season,seasontype, player_id)
    nba_call_url = 'http://stats.nba.com/stats/shotchartdetail?AheadBehind=&CFID=&CFPARAMS=&ClutchTime=&Conference=&ContextFilter=&ContextMeasure=FGM&DateFrom=&DateTo=&Division=&EndPeriod=10&EndRange=28800&GameEventID=&GameID=&GameSegment=&GroupID=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&Period=0&PlayerID=%s&PlayerPosition=&PointDiff=&Position=&RangeType=0&RookieYear=&Season=%s&SeasonSegment=&SeasonType=%s&ShotClockRange=&StartPeriod=1&StartRange=0&StarterBench=&TeamID=0&VsConference=&VsDivision=' % (player_id, season, seasontype)
    print(nba_call_url)
    #ua = UserAgent()
    #print(ua.chrome)
    u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
    headers = {'User-Agent': u_a}#'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'}
    response = requests.get(nba_call_url, headers=headers)
    data = response.json()
    print(data)

    for row in data['resultSets'][0]['rowSet']:
        three=0
        if row[12]=='3PT Field Goal':
            three=1
        temp=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                row[8], row[9], row[10],row[11], row[12], row[13], row[14],
                row[15], row[16], row[17],row[18], row[19], row[20], three, season[:4], datetime.datetime(int(season[:4])+1, 1, 1))
        if away:
            coord = ([row[17],((470-52.5)-row[18])+(470-52.5)])
        else:
            coord = ([-row[17],row[18]])
        coords.append((coord,)+temp)

    print("Done processing")
    return master_shots, coords

def create_feature_class(output_gdb, output_feature_class):
    feature_class = os.path.basename(output_feature_class)
    if not arcpy.Exists(output_gdb):
        arcpy.CreateFileGDB_management(os.path.dirname(output_gdb),os.path.basename(output_gdb))

    if not arcpy.Exists(output_feature_class):
        #"PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", transform_method="", in_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
        arcpy.CreateFeatureclass_management(output_gdb,feature_class,"POINT","#","DISABLED","DISABLED", "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]","#","0","0","0")
        arcpy.AddField_management(output_feature_class, "GRID_TYPE","TEXT", "", "", 100)
        arcpy.AddField_management(output_feature_class, "GAME_ID","TEXT", "", "", 100)
        arcpy.AddField_management(output_feature_class, "GAME_EVENT_ID","TEXT", "", "", 100)
        arcpy.AddField_management(output_feature_class, "PLAYER_ID","TEXT", "", "", 100)
        arcpy.AddField_management(output_feature_class, "PLAYER_NAME","TEXT", "", "", 100)
        arcpy.AddField_management(output_feature_class, "TEAM_ID","TEXT", "", "", 100)
        arcpy.AddField_management(output_feature_class, "TEAM_NAME","TEXT", "", "", 100)
        arcpy.AddField_management(output_feature_class,"PERIOD","SHORT", "", "", "")
        arcpy.AddField_management(output_feature_class,"MINUTES_REMAINING","SHORT", "", "", "")
        arcpy.AddField_management(output_feature_class,"SECONDS_REMAINING","SHORT", "", "", "")
        arcpy.AddField_management(output_feature_class,"EVENT_TYPE","TEXT", "", "", 100)
        arcpy.AddField_management(output_feature_class,"ACTION_TYPE","TEXT", "", "", 100)
        arcpy.AddField_management(output_feature_class,"SHOT_TYPE","TEXT", "", "", 100)
        arcpy.AddField_management(output_feature_class,"SHOT_ZONE_BASIC","TEXT", "", "", 100)
        arcpy.AddField_management(output_feature_class,"SHOT_ZONE_AREA","TEXT", "", "", 100)
        arcpy.AddField_management(output_feature_class,"SHOT_ZONE_RANGE","TEXT", "", "", 100)
        arcpy.AddField_management(output_feature_class,"SHOT_DISTANCE","SHORT", "", "", "")
        arcpy.AddField_management(output_feature_class,"LOC_X","DOUBLE", "", "", "")
        arcpy.AddField_management(output_feature_class,"LOC_Y","DOUBLE", "", "", "")
        arcpy.AddField_management(output_feature_class,"SHOT_ATTEMPTED_FLAG","SHORT", "", "", "")
        arcpy.AddField_management(output_feature_class,"SHOT_MADE_FLAG","SHORT", "", "", "")
        arcpy.AddField_management(output_feature_class,"THREE","SHORT", "", "", "")
        arcpy.AddField_management(output_feature_class,"GAME_DATE", "TEXT", "", "", 30)
        arcpy.AddField_management(output_feature_class,"SEASON_DATE", "DATE")

def populate_feature_class(rowValues, output_feature_class):
    #rowValues = [('Anderson', (1409934.4442000017, 1076766.8192000017))]
    c = arcpy.da.InsertCursor(output_feature_class,fc_fields)
    for row in rowValues:
        print(row)
        c.insertRow(row)
    del c

def add_player_movement(fc):
    field_to_add = ('MOVEMENT')
    arcpy.AddField_management(fc, field_to_add, "TEXT", "", "", 255)
    print("Creating game dict")
    game_dict = create_date_dict(fc)
    print("Done Creating Game Dict")
    fields = ('GAME_ID','GAME_EVENT_ID',field_to_add, 'GAME_DATE')

    with arcpy.da.UpdateCursor(fc, fields) as cursor:
        for row in cursor:
            gameid = row[0]
            eventid = row[1]
            row[2] = 'http://stats.nba.com/movement/#!/?GameID=%s&GameEventID=%s' % (gameid, eventid)
            row[3] = game_dict[gameid]
            cursor.updateRow(row)

    print('Done')

def append_seasons(gdb, output_fc):
    arcpy.env.workspace = gdb
    fc_list = arcpy.ListFeatureClasses('*',"Point")
    arcpy.CreateFeatureclass_management(gdb, os.path.basename(output_fc), "POINT", fc_list[0],"DISABLED","DISABLED","PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]];-20037700 -30241100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision","#","0","0","0")
    arcpy.Append_management(fc_list, output_fc, 'NO_TEST', '', '')
##    for fc in fc_list:
##        arcpy.Delete_management(fc)

def create_hex_layers(hexagon_features, shots, output_gdb, name):
    print('Shots Made Hexagons')
    made_shots_layer = 'in_memory\\made_shots_layer'
    query = '"SHOT_MADE_FLAG" = 1'
    arcpy.MakeFeatureLayer_management(shots,made_shots_layer,query,"#","#")
    arcpy.analysis.SummarizeWithin(hexagon_features, made_shots_layer, os.path.join(output_gdb, name+"_shots_made_hexbins"), "ONLY_INTERSECTING", "SHOT_MADE_FLAG Sum", "ADD_SHAPE_SUM", None, None, "NO_MIN_MAJ", "NO_PERCENT", None)

    print('Shots Missed Hexagons')
    missed_shots_layer = 'in_memory\\missed_shots_layer'
    query = '"SHOT_MADE_FLAG" = 0'
    arcpy.MakeFeatureLayer_management(shots,missed_shots_layer,query,"#","#")
    arcpy.analysis.SummarizeWithin(hexagon_features, missed_shots_layer, os.path.join(output_gdb, name+"_shots_missed_hexbins"), "ONLY_INTERSECTING", "SHOT_MADE_FLAG Sum", "ADD_SHAPE_SUM", None, None, "NO_MIN_MAJ", "NO_PERCENT", None)

    print('Total Shots Hexagons')
    arcpy.analysis.SummarizeWithin(hexagon_features, shots, os.path.join(output_gdb, name+"_total_shots_hexbins"), "ONLY_INTERSECTING", "SHOT_MADE_FLAG Sum", "ADD_SHAPE_SUM", None, None, "NO_MIN_MAJ", "NO_PERCENT", None)


if __name__ == '__main__':

##    players = {'Kobe Bryant': '977' }
##    seasons = ['2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08',
##            '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']
##    gdb = "C:/PROJECTS/R&D/NBA/Kobe_Bryants_Career.gdb"

    #players = {'Kevin Durant': '201142'}
    #seasons = ['2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']
    #gdb = "C:/PROJECTS/R&D/NBA/Kevin_Durant_Career.gdb"
    players = {'Stephen Curry': '201939'}
    #seasons = ['2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']
    #gdb = "C:/PROJECTS/R&D/NBA/Steph_Curry.gdb"
    #players = {'Stephen Curry': '201939'}#,
    #players = {'Kevin Durant': '201142',
    #        'Russell Westbrook': '201566',
    #        'Steven Adams': '203500',
    #        'Serge Ibaka' : '201586',
    #        'Enes Kanter' : '202683',
    #        'Victor Oladipo': '203506'}


    #players = {'Russell Westbrook': '201566'}
    seasons = ['2016-17']
    playoffs = False
    away = False #True
    #hexbins = "C:/PROJECTS/R&D/NBA/Part_II.gdb/Court_Hexibins"
    gdb = r"C:\PROJECTS\BASKETBALL\RW_2016_17\stats_sc.gdb"

    #season= '2014-15'
    for player in players:
        for season in seasons:
            print('Looking at ' + str(season) + ' season')
            player_name = player
            print('Looking at ' + player_name)
            player_id = players[player_name]
            output_feature_class = os.path.join(gdb, player_name.replace(' ', '_') + '_' + season.replace('-','_'))
            output_gdb = os.path.dirname(output_feature_class)
            print('Processing feature data')
            #feature_data, coords = get_last_game(player_id, season, playoffs, away)
            print('Creating output features')
            #create_feature_class(output_gdb, output_feature_class)
            print('Populating features')
            #populate_feature_class(coords, output_feature_class)
            print('Adding Player Movement')
            add_player_movement(output_feature_class)
            #print('Creating Hexbin Shotchart')
            #create_hex_layers(hexbins, output_feature_class, output_gdb, player_name.replace(' ', '_'))

    if len(seasons) > 1:
        print('Appending all data to one feature class.')
        append_seasons(gdb, 'all_shots')

    print('Done.')