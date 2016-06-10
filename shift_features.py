#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      greg6750
#
# Created:     08/06/2016
# Copyright:   (c) greg6750 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import arcpy

def duplicate_court(in_gdb, out_gdb, wildcard):

    arcpy.env.workspace = in_gdb
    fc_list = arcpy.ListFeatureClasses(wildcard)
    print(fc_list)
    iterations = 1
    counter = 0
    for i in range(0,iterations):
        for fc in fc_list:
            print(fc)
            duplicate_features(fc, out_gdb, counter)
            counter = counter+1

def duplicate_features(in_fc, out_gdb, counter):

    print('Duplicating Features: ')
    print(str(counter))

    # Set some variables
    feat_name= output_fc = os.path.basename(in_fc)
    out_fc = os.path.join(out_gdb, feat_name + str(counter))
    #for val in range(1,6):
    scale_factor = counter
    xOffset = scale_factor*510
    yOffset = 0
    # Code to make a copy which will have its coordinates moved (and can be compared with original)
    if arcpy.Exists(out_fc):
        arcpy.Delete_management(out_fc)
    arcpy.Copy_management(in_fc,out_fc)
    # Perform the move
    with arcpy.da.UpdateCursor(out_fc, ["SHAPE@XY"]) as cursor:
        for row in cursor:
            cursor.updateRow([[row[0][0] + xOffset,row[0][1] + yOffset]])

def append_polylines(gdb, output_fc):
    arcpy.env.workspace = gdb
    fc_list = arcpy.ListFeatureClasses('*',"Polyline")
    arcpy.CreateFeatureclass_management(gdb, os.path.basename(output_fc), "POLYLINE", fc_list[0],"DISABLED","DISABLED","PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]];-20037700 -30241100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision","#","0","0","0")
    arcpy.Append_management(fc_list, output_fc, 'NO_TEST', '', '')

def append_polygons(gdb, output_fc):
    arcpy.env.workspace = gdb
    fc_list = arcpy.ListFeatureClasses('*',"Polygon")
    arcpy.CreateFeatureclass_management(gdb, os.path.basename(output_fc), "POLYGON", fc_list[0],"DISABLED","DISABLED","PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]];-20037700 -30241100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision","#","0","0","0")
    arcpy.Append_management(fc_list, output_fc, 'NO_TEST', '', '')

if __name__ == '__main__':
##    in_gdb = r'C:\PROJECTS\R&D\NBA\court.gdb'
##    out_gdb = r'C:\PROJECTS\R&D\NBA\Courts.gdb'
##    wildcard = "total_shots_hexbins"
##    duplicate_court(in_gdb, out_gdb, wildcard)
##    append_polygons(out_gdb, 'multicourts')
##    append_polylines(out_gdb, 'milticourt_lines')

    in_gdb = r'C:\PROJECTS\R&D\NBA\GSW_DeathLineup_RegSeason_2015_16.gdb'
    out_gdb = r'C:\PROJECTS\R&D\NBA\Death_Lineup.gdb'
    wildcard = "*total_shots_hexbins"
    duplicate_court(in_gdb, out_gdb, wildcard)
    append_polygons(out_gdb, "total_shots_hexbins")
    #append_polylines(out_gdb, 'milticourt_lines')
