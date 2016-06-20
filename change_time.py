#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      greg6750
#
# Created:     17/06/2016
# Copyright:   (c) greg6750 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import datetime

def change_time(fc):
    print('running')
    field_to_add = 'SEQUENCE_TIME'
    field_to_mod = 'FAKE_DATE'
    game_id = 'GAME_ID'
    arcpy.AddField_management(fc, field_to_add, "DATE",)

    games = ['0041500401', '0041500402','0041500403', '0041500404', '0041500405', '0041500406']

    fields = (game_id, field_to_mod, field_to_add)

    with arcpy.da.UpdateCursor(fc, fields) as cursor:
        for row in cursor:
            hms = row[1]
            if row[0] == games[0]:
                time = datetime.datetime(2016,6,2,hms.hour,hms.minute, hms.second)
            if row[0] == games[1]:
                time = datetime.datetime(2016,6,5,hms.hour,hms.minute, hms.second)
            if row[0] == games[2]:
                time = datetime.datetime(2016,6,8,hms.hour,hms.minute, hms.second)
            if row[0] == games[3]:
                time = datetime.datetime(2016,6,10,hms.hour,hms.minute, hms.second)
            if row[0] == games[4]:
                time = datetime.datetime(2016,6,13,hms.hour,hms.minute, hms.second)
            if row[0] == games[5]:
                time = datetime.datetime(2016,6,16,hms.hour,hms.minute, hms.second)

            row[2] = time

            cursor.updateRow(row)

    print('Done')

if __name__ == '__main__':
    fc = r'C:\Users\greg6750\Documents\ArcGIS\Projects\LeBron James\LeBron James.gdb\LBJ_Game_1_6'
    change_time(fc)
