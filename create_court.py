#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      greg6750
#
# Created:     26/04/2016
# Copyright:   (c) greg6750 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import arcpy

def build_basketball_court(output_gdb, output_feature_class):
    print('Creating basketball court.')
    fields = ('SHAPE@', 'NAME')
    fc = os.path.join(output_gdb, output_feature_class)
    if not arcpy.Exists(os.path.join(output_gdb, output_feature_class)):
        arcpy.CreateFeatureclass_management(
            output_gdb, output_feature_class, "POLYGON", "#", "DISABLED",
            "DISABLED", arcpy.SpatialReference(3857))
        arcpy.AddField_management(fc, fields[1], "TEXT",
                                  field_length=20)

    cursor = arcpy.da.InsertCursor(fc, fields)



    field = [(-250, -52.5),
             (250, -52.5),
             (250, 940-52.5),
             (-250, 940-52.5)]
    cursor.insertRow([field, "Court"])

    pt_geometry = arcpy.PointGeometry(arcpy.Point(0,190-52.5))
    arcpy.Buffer_analysis(pt_geometry, "in_memory\\key1", 60)
    arcpy.Append_management("in_memory\\key1", fc, "NO_TEST","","")

    pt_geometry = arcpy.PointGeometry(arcpy.Point(0,940-(190+52.5)))
    arcpy.Buffer_analysis(pt_geometry, "in_memory\\key2", 60)
    arcpy.Append_management("in_memory\\key2", fc, "NO_TEST","","")

    whole_key = [(-80, -52.5),
             (80, -52.5),
             (80, 190-52.5),
             (-80, 190-52.5)]
    cursor.insertRow([whole_key, "Paint Extended"])



    whole_key = [(-80, 940-52.5),
             (80, 940-52.5),
             (80, 940-(190+52.5)),
             (-80, 940-(190+52.5))]
    cursor.insertRow([whole_key, "Paint Extended"])

    paint = [(-60, 940-52.5),
             (60, 940-52.5),
             (60, 940-(190+52.5)),
             (-60, 940-(190+52.5))]
    cursor.insertRow([paint, "Paint"])

    paint = [(-60, -52.5),
             (60, -52.5),
             (60, 190-52.5),
             (-60, 190-52.5)]
    cursor.insertRow([paint, "Paint"])

##    rim = [(-60, -5.5),
##             (60, -5.5),
##             (60, 19-5.5),
##             (-60, 19-5.5)]

    pt_geometry = arcpy.PointGeometry(arcpy.Point(0,0))
    arcpy.Buffer_analysis(pt_geometry, "in_memory\\rim1", 12.5)
    arcpy.Append_management("in_memory\\rim1", fc, "NO_TEST","","")

    pt_geometry = arcpy.PointGeometry(arcpy.Point(0,835))
    arcpy.Buffer_analysis(pt_geometry, "in_memory\\rim2", 12.5)
    arcpy.Append_management("in_memory\\rim2", fc, "NO_TEST","","")

    pt_geometry = arcpy.PointGeometry(arcpy.Point(0,470-52.5))
    arcpy.Buffer_analysis(pt_geometry, "in_memory\\midcourt", 60)
    arcpy.Append_management("in_memory\\midcourt", fc, "NO_TEST","","")

    #pt_geometry = arcpy.PointGeometry(arcpy.Point(0,470-55))
    arcpy.Buffer_analysis(pt_geometry, "in_memory\\midcourt_inner", 20)
    arcpy.Append_management("in_memory\\midcourt_inner", fc, "NO_TEST","","")
    #cursor.insertRow([paint, "Rim"])

    print("Done.")

def build_court_markers(output_gdb, output_feature_class):
    print('Creating basketball court markers.')
    fields = ('SHAPE@', 'NAME')
    fc = os.path.join(output_gdb, output_feature_class)
    if not arcpy.Exists(os.path.join(output_gdb, output_feature_class)):
        arcpy.CreateFeatureclass_management(
            output_gdb, output_feature_class, "POLYLINE", "#", "DISABLED",
            "DISABLED", arcpy.SpatialReference(3857))
        arcpy.AddField_management(fc, fields[1], "TEXT",
                                  field_length=20)

    cursor = arcpy.da.InsertCursor(fc, fields)

    back_board = [(-30, -12.5),
             (30, -12.5)]
    cursor.insertRow([back_board, "Backboard"])

    back_board = [(-30, 847.5),
             (30, 847.5)]
    cursor.insertRow([back_board, "Backboard"])

    half_court = [(-250, 470-52.5),
             (250, 470-52.5)]
    cursor.insertRow([half_court, "Half Court"])

    three = [(-220+(1/12)*10, -52.5),
             (-220+(1/12)*10, 140-52.5)]
    cursor.insertRow([three, "Three Point Line"])

    three = [(220-(1/12)*10, -52.5),
             (220-(1/12)*10, 140-52.5)]
    cursor.insertRow([three, "Three Point Line"])

    three = [(-220+(1/12)*10, 940-52.5),
             (-220+(1/12)*10, 940-(140+52.5))]
    cursor.insertRow([three, "Three Point Line"])

    three = [(220-(1/12)*10, 940-52.5),
             (220-(1/12)*10, 940-(140+52.5))]
    cursor.insertRow([three, "Three Point Line"])

    #Create 3Point Arc
    pt_geometry = arcpy.PointGeometry(arcpy.Point(0,0))
    arcpy.Buffer_analysis(pt_geometry, "in_memory\\arc", 235.833) #237.5)#

    pt_geometry = arcpy.PointGeometry(arcpy.Point(0,835))
    arcpy.Buffer_analysis(pt_geometry, "in_memory\\arc2", 235.833) #237.5)#


    arcpy.CreateFeatureclass_management(
            "in_memory", "clipper", "POLYGON", "#", "DISABLED",
            "DISABLED", arcpy.SpatialReference(3857))
    arcpy.AddField_management("in_memory\\clipper", fields[1], "TEXT",
                                  field_length=20)
    clip_cursor = arcpy.da.InsertCursor("in_memory\\clipper", fields)
    clip_poly = [(-250, 940-(140+52.5)),
             (250, 940-(140+52.5)),
             (250, 140-52.5),
             (-250, 140-52.5)]
    clip_cursor.insertRow([clip_poly, "Three Point Line"])

##    clip_poly = [(-250, 940-52.5),
##             (250, 940-52.5),
##             (250, 140-52.5),
##             (-250, 140-52.5)]
##    clip_cursor.insertRow([clip_poly, "Three Point Line"])

    arcpy.PolygonToLine_management("in_memory\\arc","in_memory\\line_arc")
    arcpy.PolygonToLine_management("in_memory\\arc2","in_memory\\line_arc2")

    arcpy.Clip_analysis("in_memory\\line_arc", "in_memory\\clipper", "in_memory\\clip_res")
    arcpy.Clip_analysis("in_memory\\line_arc2", "in_memory\\clipper", "in_memory\\clip_res2")
    arcpy.Append_management("in_memory\\clip_res", fc, "NO_TEST","","")
    arcpy.Append_management("in_memory\\clip_res2", fc, "NO_TEST","","")

    print("Done.")

if __name__ == '__main__':
    out_gdb = r"C:\PROJECTS\R&D\NBA\court.gdb"
    out_fc = "court_poly"
    #build_basketball_court(out_gdb, out_fc)
    build_court_markers(out_gdb, "court_markers")
