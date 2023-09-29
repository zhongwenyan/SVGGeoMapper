# SVGGeoMapper
Plotting IP addresses from Nginx or Apache log files to SVG map or chart. It uses IP2Location.io API service to lookup for the geolocation information, and then plot to SVG map or chart based on the geolocation information with the help of Pygal library. Free sign up is available through here: https://www.ip2location.io/.

## Requirement
The Pygal library and its world map plugin must be installed before using this script. You can install both via terminal by using these commands:
```bash
pip install pygal
pip install pygal_maps_world
```


## Usage
Just download the script to your choice of directory, and run the script as:
```bash
svg-geo-mapper.py -k your_api_key -f your_log_file -m your_desired_output_mode -o output_svg_filename
```

## Parameters
| parameter   |      Description      |
|----------|:-------------|
| -k, --key |  Your IP2Location.io API key. |
| -f, --file | Your Nginx or Apache log file.   |
| -m, --mode | Mode which decide what kind of SVG map or chart to be generated. Options are world, continent, horizontalbar and piechart. Default value is world. |
| -o, --outputfile | The output filename of the SVG map. |
| -h, -?, --help | Display the help message. |
