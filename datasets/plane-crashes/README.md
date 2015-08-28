Below is a report from the collector of the data set, Hassan Jannah.

#### Cleaning

I had to do a lot of cleaning in Excel. Some data is very old and has not been curated. Also some airlines and manufacturers changed names, models, etc.

Some of the things I did:

1. Split city and country.
2. Fill some missing data (in casualties especially because some numbers didn't add up).
3. Fix date formats.
4. Fix airplane make and model.

#### Data Source

The data was collected from aviation-safety.net (ASN).
More information about the data can be found in [this Microsoft Word document](http://aviation-safety.net/about/ASN-standards.doc) from the site.

The original NTSB data dump was full of mission values and inconsistencies. The [Aviation Safety Network database](http://aviation-safety.net/database/>) provided a much cleaner and data set, which contains all the values, required for our targeted visualization elements. The only drawback was that the database was actually a set of tabular web pages. To prepare the data, we used a combination of tools and techniques:

1. Using Beautiful Soup, we generated a list of the entire page URLs that needed to be scraped.

2. We used Kimono Labs web scraping tool in order to scrape the entire list of URLs

3. Used python to download the data from Kimono Labs because the API only retrieves 2500 records at a time. The script also converted the output from JSON to CSV

4. Used excel extensively to extract quantitative data values from the data (e.g. occupants and fatalities) and to clean up some inconsistencies in the numbers. We also used excel to extract additional textual information such as departure, arrival and accident location countries, and airplane manufacturers.

For the 100 worst accidents, we ranked the accidents by the number of air and ground fatalities.
For the unusual lists, cross-matched our list with a [list on PlaneCrashesinfo.com](http://www.planecrashinfo.com/unusual.htm).
