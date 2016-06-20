#-------------------------------------------------------------------------------
# Name:        single_player_shotchart.py
# Purpose:     This script creates an NBA shot chart that can be visualized in
#              ArcGIS.
#
# Author:      Gregory Brunner
#
# Created:     01/10/2015
# Copyright:
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from __future__ import division

#import urllib2
#import json
import requests
import os
import datetime

import arcpy

arcpy.env.overwriteOutput = True

fc_fields = ("SHAPE@XY","GRID_TYPE","GAME_ID","GAME_EVENT_ID","PLAYER_ID","PLAYER_NAME","TEAM_ID",
    "TEAM_NAME","PERIOD","MINUTES_REMAINING","SECONDS_REMAINING","EVENT_TYPE",
    "ACTION_TYPE","SHOT_TYPE","SHOT_ZONE_BASIC","SHOT_ZONE_AREA",
    "SHOT_ZONE_RANGE","SHOT_DISTANCE","LOC_X","LOC_Y","SHOT_ATTEMPTED_FLAG",
    "SHOT_MADE_FLAG", "THREE", "GAME_DATE", "SEASON_DATE", "FAKE_DATE")


def append_shots(gdb, output_line_fc):
    arcpy.env.workspace = gdb
    fc_list = arcpy.ListFeatureClasses('*',"Point")
    arcpy.CreateFeatureclass_management(gdb, os.path.basename(output_line_fc), "POINT", fc_list[0],"DISABLED","DISABLED",arcpy.SpatialReference(3857),"#","0","0","0")
    arcpy.Append_management(fc_list, output_line_fc, 'NO_TEST', '', '')
    #for fc in fc_list:
        #arcpy.Delete_management(fc)

def get_last_game(player_id, season, playoffs, away):

    master_shots=[]
    coords = []
    if playoffs:
        seasontype="Playoffs"
    else:
        seasontype="Regular%20Season"
    seasonindicator=0
    nba_call_url='http://stats.nba.com/stats/shotchartdetail?Season=%s&SeasonType=%s&TeamID=0&PlayerID=%s&GameID=&Outcome=&Location=&Month=0&SeasonSegment=&DateFrom=&Dateto=&OpponentTeamID=0&VsConference=&VsDivision=&Position=&RookieYear=&GameSegment=&Period=0&LastNGames=1&ContextMeasure=FGA' % (season,seasontype, player_id)
    #nba_call_url='http://stats.nba.com/stats/shotchartdetail?Season=%s&SeasonType=%s&TeamID=0&PlayerID=&GameID=&Outcome=&Location=&Month=0&SeasonSegment=&DateFrom=&Dateto=&OpponentTeamID=0&VsConference=&VsDivision=&Position=&RookieYear=&GameSegment=&Period=0&LastNGames=0&ContextMeasure=FGA' % (season,seasontype)
    print(nba_call_url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'}
    response = requests.get(nba_call_url, headers=headers)
    #print(response)
    data = response.json()
    #req = urllib2.Request(nba_call_url)
    #plays=urllib2.urlopen(req) #nba_call_url)
    #data=json.load(plays)

    for row in data['resultSets'][0]['rowSet']:

        three=0
        if row[12]=='3PT Field Goal':
            three=1
        temp=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                row[8], row[9], row[10],row[11], row[12], row[13], row[14],
                row[15], row[16], row[17],row[18], row[19], row[20], three, season[:4], datetime.datetime(int(season[:4])+1, 5, 26, row[7], 11-row[8], 59-row[9]),
                datetime.datetime.fromtimestamp((row[7]-1)*720+(11-row[8])*60+(59-row[9])))
        if away:
            coord = ([row[17],((470-52.5)-row[18])+(470-52.5)])
        else:
            coord = ([-row[17],row[18]])
        coords.append((coord,)+temp)

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
        arcpy.AddField_management(output_feature_class,"FAKE_DATE", "DATE")

def populate_feature_class(rowValues, output_feature_class):
    #rowValues = [('Anderson', (1409934.4442000017, 1076766.8192000017))]
    c = arcpy.da.InsertCursor(output_feature_class,fc_fields)
    for row in rowValues:
        print(row)
        c.insertRow(row)
    del c

##def copy_to_shapefile(in_fc, out_fc):
##    #arcpy.Project_management(in_fc, in_fc+'_proj', out_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", transform_method="", in_coor_system="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="")
##    arcpy.Project_management(in_fc, in_fc+'_proj', out_coor_system="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", transform_method="", in_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="")
##    #arcpy.Project_management(in_fc, in_fc+'_proj', )
##    #arcpy.CopyFeatures_management(in_fc, out_fc)

def get_rows(data_set, fields):
    with arcpy.da.SearchCursor(data_set, fields) as cursor:
        for row in cursor:
            yield row

def add_player_movement(fc):
    field_to_add = ('MOVEMENT')
    arcpy.AddField_management(fc, field_to_add, "TEXT", "", "", 255)

    fields = ('GAME_ID','GAME_EVENT_ID',field_to_add)

    with arcpy.da.UpdateCursor(fc, fields) as cursor:
        for row in cursor:
            gameid = row[0]
            eventid = row[1]
            row[2] = 'http://stats.nba.com/movement/#!/?GameID=%s&GameEventID=%s' % (gameid, eventid)
            cursor.updateRow(row)

    print('Done')

def append_seasons(gdb, output_fc):
    arcpy.env.workspace = gdb
    fc_list = arcpy.ListFeatureClasses('*',"Point")
    arcpy.CreateFeatureclass_management(gdb, os.path.basename(output_fc), "POINT", fc_list[0],"DISABLED","DISABLED","PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]];-20037700 -30241100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision","#","0","0","0")
    arcpy.Append_management(fc_list, output_fc, 'NO_TEST', '', '')
##    for fc in fc_list:
##        arcpy.Delete_management(fc)

def create_hex_layers(hexagon_features, shots, output_gdb):
    print('Shots Made Hexagons')
    made_shots_layer = 'in_memory\\made_shots_layer'
    query = '"SHOT_MADE_FLAG" = 1'
    arcpy.MakeFeatureLayer_management(shots,made_shots_layer,query,"#","#")
    arcpy.analysis.SummarizeWithin(hexagon_features, made_shots_layer, os.path.join(output_gdb, "shots_made_hexbins"), "ONLY_INTERSECTING", "SHOT_MADE_FLAG Sum", "ADD_SHAPE_SUM", None, None, "NO_MIN_MAJ", "NO_PERCENT", None)

    print('Shots Missed Hexagons')
    missed_shots_layer = 'in_memory\\missed_shots_layer'
    query = '"SHOT_MADE_FLAG" = 0'
    arcpy.MakeFeatureLayer_management(shots,missed_shots_layer,query,"#","#")
    arcpy.analysis.SummarizeWithin(hexagon_features, missed_shots_layer, os.path.join(output_gdb, "shots_missed_hexbins"), "ONLY_INTERSECTING", "SHOT_MADE_FLAG Sum", "ADD_SHAPE_SUM", None, None, "NO_MIN_MAJ", "NO_PERCENT", None)

    print('Total Shots Hexagons')
    arcpy.analysis.SummarizeWithin(hexagon_features, shots, os.path.join(output_gdb, "total_shots_hexbins"), "ONLY_INTERSECTING", "SHOT_MADE_FLAG Sum", "ADD_SHAPE_SUM", None, None, "NO_MIN_MAJ", "NO_PERCENT", None)



##players = {'lebron james': '2544',
##    'kevin durant': '201142',
##    'anthony davis': '203076',
##    'stephen curry': '201939',
##    'james harden': '201935',
##    'chris paul': '101108',
##    'russel westbrook': '201566',
##    'blake griffin': '201933',
##    'marc gasol': '201188',
##    'kawhi leonard': '202695'}



if __name__ == '__main__':

##    players = {'Kobe Bryant': '977' }
##    seasons = ['2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08',
##            '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']
##    gdb = "C:/PROJECTS/R&D/NBA/Kobe_Bryants_Career.gdb"

    #players = {'Kevin Durant': '201142'}
    #seasons = ['2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']

##    players = {'Russell Westbrook': '201566',
##                'Kevin Durant': '201142',
##                'Steven Adams': '203500',
##                #'Nick Collison' : '2555',
##                'Randy Foye' : '200751',
##                'Serge Ibaka' : '201586',
##                'Enes Kanter' : '202683',
##                #'Nazr Mohammed' : '1737',
##                #'Anthony Morrow' : '201627',
##                #'Cameron Payne' : '1626166',
##                'Andre Roberson' : '203460',
##                #'Kyle Singler' : '202713',
##                #'Josh Huestis' : '203962',
##                'Dion Waiters' : '203079'
##                }

    players = {
                'Draymond Green': '203110',
                'Harrison Barnes': '203084',
                'Stephen Curry' : '201939',
                'Klay Thompson' : '202691',
                'Andre Iguodala' : '2738',
                'Shaun Livingston' : '2733',
                'Marreese Speights' : '201578',
                'Leandro Barbosa' : '2571',
                'James Michael McAdoo': '203949',
                'Anderson Varejao' : '2760',
                'Festus Ezeli' : '203105',
                'Ian Clark':'203546',
                'Brandon Rush':'201575'
                }
    #'Andrew Bogut': '101106',

##    players = {'LeBron James': '2544',
##                'Kevin Love' : '201567',
##                'Tristan Thompson' : '202684',
##                'JR Smith' : '2747',
##                'Kyrie Irving' : '202681',
##                #'Channing Frye' : '101112',
##                'Iman Shumpert' : '202697',
##                'Richard Jefferson' : '2210',
##                'Matthew Dellavedova' : '203521',
##                'Dahntay Jones' : '2563',
##                'James Jones' : '2592',
##                'Timofey Mozgov' :'202389',
##                'Maurice Williams' :'2590',
##                #'Jordan McRae' : '203895'
##                }

    seasons = ['2015-16']
    playoffs = True
    away = False
    hexbins = "C:\\PROJECTS\\R&D\\NBA\\Part_II.gdb\\Court_Hexibins"

    gdb = "C:/PROJECTS/R&D/NBA/Game6____GoldenState_06162016.gdb"

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
            feature_data, coords = get_last_game(player_id, season, playoffs, away)
            print('Creating output features')
            create_feature_class(output_gdb, output_feature_class)
            print('Populating features')
            populate_feature_class(coords, output_feature_class)
            print('Adding Player Movement')
            add_player_movement(output_feature_class)
            print('Creating Hexbin Shotchart')
            #create_hex_layers(hexbins, output_feature_class, output_gdb)

    append_shots(gdb, os.path.join(gdb, 'game'))

    if len(seasons) > 1:
        print('Appending all data to one feature class.')
        append_seasons(gdb, 'all_shots')

    print('Done.')