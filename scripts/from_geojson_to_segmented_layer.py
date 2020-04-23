# SET YOUR OWN VARIABLES

geojson = "./MyHighways20200422.geojson"
filegdb = "./../ArcGIS/Projects/RedlandsRoads/RedlandsRoads.gdb"
outLayer = 'REST2020_segments'
highwaystosplitQ = "\"METERS\" > 30"
densifyDistance ='25 Meters'

# GENERIC VARIABLES

tempLayer = "in_memory/G2A"

########################
#
# Gotchas
#
# # Q. What if the outLayer doesn't have a "name" field with the street names?
# A. If the first (or first few) features in geojson don't have a name field, the layer will not have (street) names at all. You can manually add a "name" property to first feature in GeoJSON to hack that. 
#
######################## SCRIPT

import time

startsec = time.perf_counter()

import arcpy

try:
    print("Step 1a. Convert geojson to feature class:", tempLayer) 

    arcpy.env.workspace = filegdb

    if arcpy.Exists(outLayer):
      print("\tDeleting existing outLayer:", outLayer)
      arcpy.management.Delete(outLayer)

    print("Step 1b. Convert geojson to in_memory feature class:", tempLayer, end =" ") 

    arcpy.conversion.JSONToFeatures(geojson, tempLayer, "POLYLINE")
    print("with", arcpy.management.GetCount(tempLayer), "features.")

    print("Step 1c. Add & delete fields") 

    # TODO - get a list of all fields, then delete all except the once to keep
    arcpy.management.DeleteField(tempLayer, 'tiger_cfcc;tiger_county;tiger_name_base;tiger_name_type;tiger_reviewed;tiger_separated;tiger_source;tiger_tlid;tiger_upload_uuid;')
    arcpy.management.AddFields(tempLayer, [
      ['Meters', 'FLOAT'],
      ['Miles', 'FLOAT'],
      ['Runners', 'TEXT'],
      ['StravaIds', 'TEXT', '#', 2000]])

    print("Step 1d. Calculating line lengths...") 

    arcpy.management.CalculateField(tempLayer, 'METERS', "LengthGeodetic($feature)", 'ARCADE');
    
    print("Step 1e. Selecting the long highways...", end =" ")
    
    arcpy.management.SelectLayerByAttribute(tempLayer, 'NEW_SELECTION', highwaystosplitQ)
    print(arcpy.management.GetCount(tempLayer), "features.")
        
    print("Step 1f. Densifying the selected long lines...")
    arcpy.edit.Densify(tempLayer, 'DISTANCE', densifyDistance)

    print("Step 1g. Splitting into", outLayer, "...", end =" ")
    arcpy.management.SplitLine(tempLayer, outLayer)
    print(arcpy.management.GetCount(outLayer), "features.")

    print("Step 1h. Calculating distances (just for fun)")
    arcpy.management.CalculateField(outLayer, 'Meters', "!shape.length@meters!", 'PYTHON3')
    arcpy.management.CalculateField(outLayer, 'Miles', "!shape.length@miles!", 'PYTHON3')

finally:
    print("Done - start using:", outLayer)

######################## SCRIPT END

print(f"INFO: Total script time: {time.perf_counter()-startsec:0.1f} seconds.")
