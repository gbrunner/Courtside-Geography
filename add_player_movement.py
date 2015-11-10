#-------------------------------------------------------------------------------
# Name:        add_player_movement
# Purpose:     Add the player movement link to the data
#
# Author:      Gregory Brunner, Esri
#
# Created:     10/11/2015
# Copyright:   (c) greg6750 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy

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

if __name__ == '__main__':
    fc = r'C:\PROJECTS\R&D\NBA\RusselWestbrook.gdb\rw_2014_2015_Complete_10x'
    add_player_movement(fc)
