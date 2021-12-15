# mis-bom

This repository hosts the parts list (BOM = Bill of Materials) for the Modular
Insertion System (MIS) framework. The BOM for any instance of the MIS depends
on the configuration (how many arcs, how many cameras, etc.), so this repo is
intended to be a "single source of truth" for the parts list, while also
enabling flexibility with respect to different configurations.

Sub-assemblies (subAssy's) are stored in bom/ as CSV files. See the README
there for more details.

To generate a new BOM for your configuration:

```
cd util/
python config.py
```

and enter your configuration details. This will generate a new CSV file with
the collated quantities for each part.

