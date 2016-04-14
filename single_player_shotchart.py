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

import arcpy

arcpy.env.overwriteOutput = True

fc_fields = ("SHAPE@XY","GRID_TYPE","GAME_ID","GAME_EVENT_ID","PLAYER_ID","PLAYER_NAME","TEAM_ID",
    "TEAM_NAME","PERIOD","MINUTES_REMAINING","SECONDS_REMAINING","EVENT_TYPE",
    "ACTION_TYPE","SHOT_TYPE","SHOT_ZONE_BASIC","SHOT_ZONE_AREA",
    "SHOT_ZONE_RANGE","SHOT_DISTANCE","LOC_X","LOC_Y","SHOT_ATTEMPTED_FLAG",
    "SHOT_MADE_FLAG", "THREE", "GAME_DATE")

def get_last_game(player_id, season):

    master_shots=[]
    coords = []
    seasontype="Regular%20Season"
    seasonindicator=0
    nba_call_url='http://stats.nba.com/stats/shotchartdetail?Season=%s&SeasonType=%s&TeamID=0&PlayerID=%s&GameID=&Outcome=&Location=&Month=0&SeasonSegment=&DateFrom=&Dateto=&OpponentTeamID=0&VsConference=&VsDivision=&Position=&RookieYear=&GameSegment=&Period=0&LastNGames=0&ContextMeasure=FGA' % (season,seasontype, player_id)
    response = requests.get(nba_call_url)
    data = response.json()
    #plays=urllib2.urlopen(nba_call_url)
    #data=json.load(plays)

    for row in data['resultSets'][0]['rowSet']:
        three=0
        if row[12]=='3PT Field Goal':
            three=1
        temp=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                row[8], row[9], row[10],row[11], row[12], row[13], row[14],
                row[15], row[16], row[17],row[18], row[19], row[20], three, season[:4])
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

def populate_feature_class(rowValues, output_feature_class):
    #rowValues = [('Anderson', (1409934.4442000017, 1076766.8192000017))]
    c = arcpy.da.InsertCursor(output_feature_class,fc_fields)
    for row in rowValues:
        #print(row)
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

##def write_to_csv(fc, csv_file):
##    data_set = fc
##    output = csv_file
##    fieldnames = ("SHAPE@X","SHAPE@Y","SHOT_MADE_FLAG")
##    rows = get_rows(data_set, fieldnames)
##    f = open(output,'wt')
##    out_writer = csv.writer(f)
##    out_writer.writerow(fieldnames)
##    for row in rows:
##        out_writer.writerow(row)


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

    players = {'Kobe Bryant': '977' }
    seasons = ['2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08',
            '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15']
    gdb = "C:/PROJECTS/R&D/NBA/Mamba.gdb"

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
            feature_data, coords = get_last_game(player_id, season)
            print('Creating output features')
            create_feature_class(output_gdb, output_feature_class)
            print('Populating features')
            populate_feature_class(coords, output_feature_class)
            print('Adding Player Movement')
            add_player_movement(output_feature_class)

    if len(seasons) > 1:
        print('Appending all data to one feature class.')
        append_seasons(gdb, 'all_shots')

    print('Done.')