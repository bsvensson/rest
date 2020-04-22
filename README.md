# Run Every Street and Trail (REST)

## Data

### Getting the streets dataset from OSM

1. At https://overpass-turbo.eu/#, run the following command:

```
[out:json][timeout:500];
{{geocodeArea:Redlands}}->.searchArea;
(
  way["highway"]
  	 ["highway"!~"motorway|motorway_link|rest_area|platform|services"]
     ["foot"!~"no|private"]
     ["access"!~"no|private"]
  	 ["service"!~"parking_aisle|driveway"]
 	   ["footway"!~"."]
     (area.searchArea);
     // or specify area by coordinates
     // (34.004, -117.278, 34.101, -117.051);
);
out body;
>;
out skel qt;
```

Then use `Export -> download/copy as GeoJSON` to export to a GeoJSON file.

### Import GeoJSON to ArcGIS

#### Use arcpy or ArcGIS Online

* In ArcGIS Online, import it to a hosted feature service: `Add item` -> `From your computer`
* In Pro / with arcpy, convert it using `arcpy.conversion.JSONToFeatures(geojson, layer, "POLYLINE")`

Clean up the fields a bit

```
    arcpy.management.DeleteField(layer, 'tiger_cfcc;tiger_county;tiger_name_base;tiger_name_type;tiger_reviewed')   
    arcpy.management.AddFields(layer, [
      ['Meters', 'FLOAT'],
      ['Miles', 'FLOAT'],
      ['Runners', 'TEXT', '#', '#', 256],
      ['StravaIds', 'TEXT', '#', '#', 2000]])
```

### Split the data into smaller segments for improved details

* Split long lines into smaller segments into e.g. 25 meter segments: `arcpy.management.SplitLine()`

### Get GPX data from the running activities

* Once you have the GPX data locally, you can use them to figure out which segments you've run.

### Dissolve the data for better performance when visualizing

* `arcpy.management.Dissolve(mainlayer, dissLayer, 'Runners;name;highway', None, 'MULTI_PART')`

## Web maps and Applications

* Web map shared to group used by UltraMarathon app
* Web map in a template app
* Web map in Map Viewer
