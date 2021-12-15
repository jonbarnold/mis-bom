# mis-bom/bom

The files in this directory are CSV files (RFC 4180) which contain the bill of
materials (BOM) for each sub-assembly. The first row should be the header:

```
Description,Item Type,Janelia Part #,Manufacturer,Manufacturer Part #,Vendor,Vendor Part #,Quantity Per SubAssy
```

and the second row should be empty data (spacer), e.g.:

```
,,,,,,,
```
