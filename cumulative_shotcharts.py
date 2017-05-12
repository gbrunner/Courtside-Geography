import arcpy
import os

#input point fc
fc = r'C:\PROJECTS\BASKETBALL\RW_2016_17\stats_sc.gdb\Stephen_Curry_2016_17'#'C:\PROJECTS\BASKETBALL\RW_2016_17\stats.gdb\Russell_Westbrook_2016_17'

cum_point_gdb = r'C:\PROJECTS\BASKETBALL\RW_2016_17\stats_sc_cum.gdb'
cum_hex_gdb = r'C:\PROJECTS\BASKETBALL\RW_2016_17\stats_sc_cum_hex.gdb'
cum_raster_gdb = r'C:\PROJECTS\BASKETBALL\RW_2016_17\stats_sc_cum_raster.gdb'
cum_md_gdb = r'C:\PROJECTS\BASKETBALL\RW_2016_17\stats_sc_cum_mosaic.gdb'
cum_md_name = "cumulative_shots_merged"

if not arcpy.Exists(cum_point_gdb):
    arcpy.CreateFileGDB_management(os.path.dirname(cum_point_gdb),os.path.basename(cum_point_gdb))

if not arcpy.Exists(cum_hex_gdb):
    arcpy.CreateFileGDB_management(os.path.dirname(cum_hex_gdb),os.path.basename(cum_hex_gdb))

if not arcpy.Exists(cum_raster_gdb):
    arcpy.CreateFileGDB_management(os.path.dirname(cum_raster_gdb),os.path.basename(cum_raster_gdb))

if not arcpy.Exists(cum_md_gdb):
    arcpy.CreateFileGDB_management(os.path.dirname(cum_md_gdb),os.path.basename(cum_md_gdb))

out_cum_merge =  os.path.join(cum_point_gdb, "cumulative_points_merged")
out_hexbin_merge = os.path.join(cum_hex_gdb, "cumulative_hexbins_merged")
out_md = os.path.join(cum_md_gdb, cum_md_name)

prj = arcpy.SpatialReference(102100)

#Add pdate Field to feature class so I can create space-time-ripple
arcpy.management.AddField(fc, "pdate", "DATE", None, None, None, "pdate", "NULLABLE", "NON_REQUIRED", None)
arcpy.management.CalculateField(fc, "pdate", "datetime.datetime.strptime(!GAME_DATE!, '%m/%d/%Y')", "PYTHON", None)

#Get unique game dates
values = [row[0] for row in arcpy.da.SearchCursor(fc, "pdate")]
unique_game_dates = list(set(values))
print(unique_game_dates)

#create mosaic dataset for 2D space-time analysis
arcpy.CreateMosaicDataset_management(cum_md_gdb, cum_md_name, prj)
arcpy.AddField_management(out_md, "GAME_DATE", "DATE", None, None, None, "pdate", "NULLABLE", "NON_REQUIRED", None)

#For every game, create feature classes that look at that game and all previous games
for date in unique_game_dates:
    print("selecting")
    out_fc_name = 'game_'+str(date.year)+'_'+str(date.month)+'_'+str(date.day)
    out_raster_name = out_fc_name+'_raster'
    out_hexbin_name = out_fc_name+'_hexbin'
    out_fc = os.path.join(out_gdb, out_fc_name)
    out_hex_fc = os.path.join(out_gdb, out_hexbin_name)
    out_raster = os.path.join(out_gdb, out_raster_name)
    wc = "pdate <= date '%s'" % (date) #
    print(wc)
    arcpy.Select_analysis(fc, out_fc, where_clause=wc)

    print("created "+ outfile)
    with arcpy.da.UpdateCursor(out_fc, "pdate") as cursor:
        for row in cursor:
            row[0]=date
            cursor.updateRow(row)

    #Create Hexbins
    print('Total Shots Hexagons')
    arcpy.analysis.SummarizeWithin(hexagon_features,
        out_fc,
        out_hex_fc,
        "ONLY_INTERSECTING", "SHOT_MADE_FLAG Sum", "ADD_SHAPE_SUM", None, None, "NO_MIN_MAJ", "NO_PERCENT", None)


    #Feature to Raster
    arcpy.FeatureToRaster_conversion(out_hex_fc, "COUNT", out_raster, 0.1)


arcpy.env.workspace = cum_point_gdb
fcs = arcpy.ListFeatureClasses()
print("Merging Cumulative Point Feature Classes")
arcpy.Merge_management(fcs, out_memrge)

arcpy.env.workspace = cum_hex_gdb
fcs = arcpy.ListFeatureClasses()
print("Merging Cumulative Hexbin Feature Classes")
arcpy.Merge_management(fcs, out_memrge)

arcpy.env.workspace = cum_raster_gdb
rasters = arcpy.ListRasters()
#Add Raster to Mosaic
arcpy.AddRastersToMosaicDataset_management(mdname, "Raster Dataset", rasters)
#Field Calculation to add dates to rasters in mosaic dataset
with arcpy.da.UpdateCursor(out_md, ("","GAME_DATE")) as cursor:
        for row in cursor:
            game_date = row[0] #and some manipulatioj
            row[1]=datetime.datetime.strptime(game_date, '%m/%d/%Y')
            cursor.updateRow(row)

