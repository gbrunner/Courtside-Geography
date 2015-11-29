#-------------------------------------------------------------------------------
# Name:     map_player_movement.py
# Purpose:  This script creates maps of NBA player movement given a gameid and
#           series of events.  These maps will be analagous to terrain maps of
#           road density maps that are layers common to GIS.
#
# Author:   Gregory Brunner, gregbrunn@gmail.com, gbrunner@esri.com
#
# Created:  10/11/2015
# Copyright:(c) Gregory Brunner, 2015
# Licence:  What do I put here?
#-------------------------------------------------------------------------------
from __future__ import division

import requests
import os
import datetime
import math
import time

import arcpy

fields = ('SHAPE@XY', 'TEAM_ID', 'PLAYER_ID', 'EVENT_ID','LOC_X', 'LOC_Y',
           'RADIUS', 'MOMENT', 'GAME_CLOCK', 'SHOT_CLOCK', 'GAME_TIME', 'UNIX_TIME', 'QUARTER','VELOCITY')

def main(gameid, eventid):
    event_url = 'http://stats.nba.com/stats/locations_getmoments/?eventid=%s&gameid=%s' % (eventid, gameid)

    response = requests.get(event_url)
    if response.status_code == 400:
        print('Data not available for this filter.')
        return -1,-1,-1,-1

    response.json().keys()

    home = response.json()["home"]
    visitor = response.json()["visitor"]
    moments = response.json()["moments"]
    gamedate = response.json()['gamedate']

    date = create_datestamp(gamedate)

    team_dict = {}
    team_dict[home['teamid']] = home['name']
    team_dict[visitor['teamid']] = visitor['name']
    team_dict[1] = 'Basketball'

    d = {}
    player_team_dict = {}
    d[1] = 'Basketball'
    player_team_dict[1] = 1
    for h in home['players']:
        d[h['playerid']] = h['firstname'] + ' ' + h['lastname']
        player_team_dict[h['playerid']] = home['teamid']

    for v in visitor['players']:
        d[v['playerid']] = v['firstname'] + ' ' + v['lastname']
        player_team_dict[v['playerid']] = visitor['teamid']

    coords = []
    for moment in moments:
        quarter = moment[0]
        comp_time = moment[1]
        for player in moment[5]:
            player.extend((moments.index(moment), moment[2], moment[3]))
            clock_time = create_timestamp(quarter, date, player[6])
            ct = datetime.datetime.strftime(clock_time, '%Y/%m/%d %H:%M:%S.%f')[:-5]
            comp_time_string = datetime.datetime.fromtimestamp(comp_time/1000.0).strftime('%Y/%m/%d %H:%M:%S.%f')[:-5]
            velocty = 1.00 #placeholder for velocity (ft/s) calculations
            if player[1] == -1:
                player_data = (1, 1, eventid, player[2], player[3], player[4], player[5], player[6], player[7], ct, comp_time_string, quarter, velocty)
            else:
                player_data = (player[0], player[1], eventid, player[2], player[3], player[4], player[5], player[6], player[7], ct, comp_time_string, quarter, velocty)
            if quarter <= 2:
                coord = ([10*(player[3]-25), 10*(player[2]-5.25)])
            else:
                coord = ([-10*(player[3]-25), 10*(83.5 -(player[2]-5.25))])
            coords.append((coord,)+player_data)

    return coords, d, team_dict, player_team_dict

def create_feature_class(output_gdb, output_feature_class):
    feature_class = os.path.basename(output_feature_class)
    if not arcpy.Exists(output_gdb):
        arcpy.CreateFileGDB_management(os.path.dirname(output_gdb),os.path.basename(output_gdb))

    if not arcpy.Exists(output_feature_class):
        #"PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", transform_method="", in_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
        arcpy.CreateFeatureclass_management(output_gdb,feature_class,"POINT","#","DISABLED","DISABLED", "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]","#","0","0","0")
        arcpy.AddField_management(output_feature_class,"TEAM_ID","LONG", "", "", "")
        arcpy.AddField_management(output_feature_class,"PLAYER_ID","LONG", "", "", "")
        arcpy.AddField_management(output_feature_class,"EVENT_ID","SHORT", "", "", "")
        arcpy.AddField_management(output_feature_class,"LOC_X","DOUBLE", "", "", "")
        arcpy.AddField_management(output_feature_class,"LOC_Y","DOUBLE", "", "", "")
        arcpy.AddField_management(output_feature_class,"RADIUS","DOUBLE", "", "", "")
        arcpy.AddField_management(output_feature_class,"MOMENT","LONG", "", "", "")
        arcpy.AddField_management(output_feature_class,"GAME_CLOCK","DOUBLE", "", "", "")
        arcpy.AddField_management(output_feature_class,"SHOT_CLOCK","DOUBLE", "", "", "")
        #arcpy.AddField_management(output_feature_class,"TIME", "DATE")
        arcpy.AddField_management(output_feature_class,"GAME_TIME", "TEXT", "", "", 30)
        arcpy.AddField_management(output_feature_class,"UNIX_TIME", "TEXT", "", "", 30)
        arcpy.AddField_management(output_feature_class,"QUARTER","SHORT", "", "", "")
        arcpy.AddField_management(output_feature_class,"VELOCITY","DOUBLE", "", "", "")

def populate_feature_class(rowValues, output_feature_class):
    c = arcpy.da.InsertCursor(output_feature_class,fields)
    for row in rowValues:
        c.insertRow(row)
    del c

def create_team_subtype(gdb, fc, subtype_dict):
    # Process: Set Subtype Field...
    arcpy.SetSubtypeField_management(os.path.join(gdb,fc), "TEAM_ID")

    # use a for loop to cycle through the dictionary
    for code in subtype_dict:
        arcpy.AddSubtype_management(os.path.join(gdb,fc), code, subtype_dict[code])

def create_player_domain(gdb, fc, player_dict):
    domName = "Players"
    inField = "PLAYER_ID"

    # Process: Create the coded value domain
    arcpy.CreateDomain_management(gdb, domName, "Player Names", "TEXT", "CODED")

    # Process: Add valid material types to the domain
    #use a for loop to cycle through all the domain codes in the dictionary
    for code in player_dict:
        arcpy.AddCodedValueToDomain_management(gdb, domName, code, player_dict[code])

    # Process: Constrain the material value of distribution mains
    arcpy.AssignDomainToField_management(fc, inField, domName)

def create_datestamp(gamedate):
    date = datetime.datetime.strptime(gamedate,'%Y-%m-%d')
    return date

def create_timestamp(quarter, gamedate, seconds):
    m,s = divmod(720-seconds, 60)
    ms = round((s-int(s))*100)
    t = datetime.time(int(quarter), int(m), math.floor(s), ms*10000)
    dt = datetime.datetime.combine(gamedate, t)
    return dt

def unique(lst):
    return set(lst)

def get_unique_events(fc):
    init_event_num = -1
    events = []
    with arcpy.da.SearchCursor(fc, 'EVENT_ID') as cursor:
        for row in cursor:
            if row[0] != init_event_num:
                events.append(row[0])
                init_event_num = row[0]

    unique_events = unique(events)

    return unique_events

def create_line_features(in_fc, gdb, unique_event_list, dictionary):

    for event in unique_event_list:
        print('Creating lines for event ' + str(event))
        layer = 'in_memory\\event_lyr_' + str(event)
        query = '"EVENT_ID" = ' + str(event)
        arcpy.MakeFeatureLayer_management(in_fc,layer,query,"#","#")
        arcpy.PointsToLine_management(layer, os.path.join(gdb, 'event_'+str(event)), "PLAYER_ID", "GAME_TIME", "NO_CLOSE")
        arcpy.AddField_management(os.path.join(gdb, 'event_'+str(event)),"TEAM_ID","LONG", "", "", "")
        arcpy.AddField_management(os.path.join(gdb, 'event_'+str(event)),"QUARTER","SHORT", "", "", "")
        arcpy.AddField_management(os.path.join(gdb, 'event_'+str(event)), "START_TIME", "TEXT", "", "", 30)

        #Get Start time of lines
        with arcpy.da.SearchCursor(layer, ('GAME_TIME', 'QUARTER')) as cursor:
            first_time = cursor.next()

        print(first_time[0])
        #Add start time of lines to line features
        with arcpy.da.UpdateCursor(os.path.join(gdb, 'event_'+str(event)), ('START_TIME', 'PLAYER_ID','TEAM_ID', 'QUARTER')) as cursor:
            for row in cursor:
                row[0] = first_time[0]
                row[2] = dictionary[row[1]]
                row[3] = first_time[1]
                cursor.updateRow(row)

def append_lines(gdb, output_line_fc):
    arcpy.env.workspace = gdb
    fc_list = arcpy.ListFeatureClasses('*',"Polyline")
    arcpy.CreateFeatureclass_management(gdb, output_line_fc, "POLYLINE", fc_list[0])
    arcpy.Append_management(fc_list, os.path.join(gdb, output_line_fc), 'NO_TEST', '', '')
    for fc in fc_list:
        arcpy.Delete_management(fc)

def create_line_density_raster(gdb, in_fc, team_dict):
    for team in team_dict:
        t = team_dict[team]
        t.replace(' ', '_')
        print('Creating line density raster for ' + t)
        layer = 'in_memory\\team_lyr_' + str(t)
        query = '"TEAM_ID" = ' + str(team)
        arcpy.MakeFeatureLayer_management(os.path.join(gdb,in_fc),layer,query,"#","#")
        arcpy.gp.LineDensity_sa(layer, "NONE", os.path.join(gdb, t), "5", "5", "SQUARE_MAP_UNITS")

def create_line_density_raster_per_quarter(gdb, in_fc, team_dict, quarters):
    for team in team_dict:
        for quarter in quarters:
            t = team_dict[team]
            t.replace(' ', '_')
            print('Creating line density raster for ' + t + ' during quarter ' + str(quarter))
            layer = 'in_memory\\team_lyr_' + str(t)+ str(quarter)
            query = '"TEAM_ID" = ' + str(team) + 'AND "QUARTER" = ' + str(quarter)
            arcpy.MakeFeatureLayer_management(os.path.join(gdb,in_fc),layer,query,"#","#")
            arcpy.gp.LineDensity_sa(layer, "NONE", os.path.join(gdb, t + '_Quarter_'+ str(quarter)), "5", "5", "SQUARE_MAP_UNITS")

def find_mean_center_of_movement(gdb, in_fc, team_dict):
    print('Creating mean center of movement for entire game')
    layer = 'in_memory\\mean_center_team_lyr'
    #query = '"TEAM_ID" = ' + str(team)
    arcpy.MakeFeatureLayer_management(in_fc,layer,"#","#","#")
    arcpy.MeanCenter_stats(layer, os.path.join(gdb, 'MeanCenterOfAction'), '#','#','#')

def find_mean_center_of_movement_per_quarter(gdb, in_fc, team_dict, quarters):
    for quarter in quarters:
        print('Creating mean center of movement for quarter ' + str(quarter))
        layer = 'in_memory\\mean_center_team_lyr_' + str(quarter)
        query = '"QUARTER" = ' + str(quarter)
        arcpy.MakeFeatureLayer_management(in_fc,layer,query,"#","#")
        arcpy.MeanCenter_stats(layer,os.path.join(gdb, 'MeanCenterOfAction_Quarter_'+ str(quarter)), '#', '#', '#')

if __name__ == '__main__':

    t0 = time.clock()

    game_id = '0021500234'#'0021500177'#'0021400015'
    first_event_num = 1 #346 #1
    last_event_num = 550 #564 #350 #122
    output_line_fc =  'Entire_Game'
    output_feature_class = os.path.join("C:/PROJECTS/R&D/NBA/Part_III_OKC_DET.gdb", 'Game_' + game_id + '_Event_' + str(first_event_num) + '_' + str(last_event_num))
    output_gdb = os.path.dirname(output_feature_class)
    first_event_data, player_dictionary, team_dictionary, player_team_dictionary = main(game_id, first_event_num)
##    print('Creating feature class.')
##    create_feature_class(output_gdb, output_feature_class)
##
##    for event in range(first_event_num, last_event_num+1):
##        print('Getting Event ' + str(event))
##        print('Getting data.')
##        event_data, player_dict, team_dict, player_team_dict = main(game_id, event)
##        if event_data != -1:
##            print('Populating features.')
##            populate_feature_class(event_data, output_feature_class)
##
##    print('Creating player name domain.')
##    create_player_domain(output_gdb, output_feature_class, player_dictionary)
##    print('Creating team subtype.')
##    create_team_subtype(output_gdb, output_feature_class, team_dictionary)

    print('Deleting Identical Records.')
    #arcpy.DeleteIdentical_management(output_feature_class, "Shape;TEAM_ID;PLAYER_ID;LOC_X;LOC_Y;RADIUS;GAME_CLOCK;SHOT_CLOCK;TIME", "", "0")
    arcpy.DeleteIdentical_management(output_feature_class, "TEAM_ID;PLAYER_ID;GAME_CLOCK;GAME_TIME", "", "0")

    event_list = get_unique_events(output_feature_class)

    print('Creating Line Features')
    create_line_features(output_feature_class, output_gdb, event_list, player_team_dictionary)

    print('Putting all the lines in one feature class.')
    append_lines(output_gdb, output_line_fc)

    print('Creating team subtype for line features.')
    create_team_subtype(output_gdb, output_line_fc, team_dict)

    print('Running line density analysis.')
    create_line_density_raster(output_gdb, output_line_fc, team_dict)

    print('Running line density analysis per quarter.')
    create_line_density_raster_per_quarter(output_gdb, output_line_fc, team_dict, [1,2,3,4])

    print('Finding mean center of action.')
    find_mean_center_of_movement(output_gdb, output_feature_class, team_dict)

    print('Finding mean center per quarter.')
    find_mean_center_of_movement_per_quarter(output_gdb, output_feature_class, team_dict, [1,2,3,4])

    t1 = (time.clock() - t0)/60
    print("This process took " + str(t1) + " minutes to run.")