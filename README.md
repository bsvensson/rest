# Run Every Street and Trail (REST)

## Getting the streets dataset

1. At https://overpass-turbo.eu/#, run the following command:

```
[out:json][timeout:500];
{{geocodeArea:Redlands}}->.searchArea;
(
  way["highway"~"secondary|secondary_link|tertiary|residential"]
     ["access"!="no"]["access"!="private"](area.searchArea);
);
out body;
>;
out skel qt;
```

Then use `Export -> download/copy as GeoJSON` to save the 1,969 lines to a GeoJSON file.

2. In ArcGIS Online, import it to a hosted feature service.

`Add item` -> `From your computer`

