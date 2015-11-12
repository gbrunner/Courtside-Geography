#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      greg6750
#
# Created:     10/11/2015
# Copyright:   (c) greg6750 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from __future__ import division

import requests
##import urllib2
##import json
import os
import datetime
import math

import arcpy

fields = ('SHAPE@XY', 'TEAM_ID', 'PLAYER_ID', 'LOC_X', 'LOC_Y',
           'RADIUS', 'MOMENT', 'GAME_CLOCK', 'SHOT_CLOCK', 'TIME')

def main(gameid, eventid):
    event_url = 'http://stats.nba.com/stats/locations_getmoments/?eventid=%s&gameid=%s' % (eventid, gameid)

##    plays=urllib2.urlopen(event_url)
##    data=json.load(plays)
##    print(data)

    response = requests.get(event_url)

    response.json().keys()

    home = response.json()["home"]
    visitor = response.json()["visitor"]
    moments = response.json()["moments"]
    gamedate = response.json()['gamedate']

    date = create_datestamp(gamedate)

    team_dict = {}
    team_dict[home['teamid']] = home['name']
    team_dict[visitor['teamid']] = visitor['name']
    team_dict[-1] = 'Baseketball'

    d = {}
    d[-1] = 'Basketball'
    for h in home['players']:
        d[h['playerid']] = h['firstname'] + ' ' + h['lastname']

    for v in visitor['players']:
         d[v['playerid']] = v['firstname'] + ' ' + v['lastname']

    coords = []
    for moment in moments:
        quarter = moment[0]
        for player in moment[5]:
            player.extend((moments.index(moment), moment[2], moment[3]))
            clock_time = create_timestamp(quarter, date, player[6])
            #print(player[6])
            #print(clock_time)
            ct = datetime.datetime.strftime(clock_time, '%Y/%m/%d %H:%M:%S.%f')[:-5]
            print(ct)

            player_data = (player[0], player[1], player[2], player[3], player[4], player[5], player[6], player[7], ct)
            coord = ([10*(player[3]-25), 10*(player[2]-5.25)])
            coords.append((coord,)+player_data)
##            if player[1] == playerid:
##
##            elif player[1] == -1:
##                ball.append(player)

    #print(coords)
    return coords, d, team_dict

def create_feature_class(output_gdb, output_feature_class):
    feature_class = os.path.basename(output_feature_class)
    if not arcpy.Exists(output_gdb):
        arcpy.CreateFileGDB_management(os.path.dirname(output_gdb),os.path.basename(output_gdb))

    if not arcpy.Exists(output_feature_class):
        #"PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", transform_method="", in_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
        arcpy.CreateFeatureclass_management(output_gdb,feature_class,"POINT","#","DISABLED","DISABLED", "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]","#","0","0","0")
        arcpy.AddField_management(output_feature_class,"TEAM_ID","LONG", "", "", "")
        arcpy.AddField_management(output_feature_class,"PLAYER_ID","LONG", "", "", "")
        arcpy.AddField_management(output_feature_class,"LOC_X","DOUBLE", "", "", "")
        arcpy.AddField_management(output_feature_class,"LOC_Y","DOUBLE", "", "", "")
        arcpy.AddField_management(output_feature_class,"RADIUS","DOUBLE", "", "", "")
        arcpy.AddField_management(output_feature_class,"MOMENT","LONG", "", "", "")
        arcpy.AddField_management(output_feature_class,"GAME_CLOCK","DOUBLE", "", "", "")
        arcpy.AddField_management(output_feature_class,"SHOT_CLOCK","DOUBLE", "", "", "")
        #arcpy.AddField_management(output_feature_class,"TIME", "DATE")
        arcpy.AddField_management(output_feature_class, "TIME", "TEXT", "", "", 30)

def populate_feature_class(rowValues, output_feature_class):
    #rowValues = [('Anderson', (1409934.4442000017, 1076766.8192000017))]
    c = arcpy.da.InsertCursor(output_feature_class,fields)
    for row in rowValues:
        #print(row)
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


if __name__ == '__main__':
    game_id = '0021400015'
    event_id = '346'
    output_feature_class = os.path.join("C:/PROJECTS/R&D/NBA/Part_II_v2.gdb", 'Game_' + game_id + '_Event_' + '1_10')
    output_gdb = os.path.dirname(output_feature_class)
    print('Creating feature class.')
    create_feature_class(output_gdb, output_feature_class)

    event_id = ['1','2','3','4','5','6','7','8','9','10']
    for event in event_id:
        print('Getting data.')
        event_data, player_dict, team_dict = main(game_id, event)
        print('Populating features.')
        populate_feature_class(event_data, output_feature_class)

    print('Creating player name domain.')
    create_player_domain(output_gdb, output_feature_class, player_dict)
    print('Craeting team subtype.')
    create_team_subtype(output_gdb, output_feature_class, team_dict)
