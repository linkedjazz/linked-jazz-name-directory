# Linked Jazz

![Mou icon](http://linkedjazz.org/image/jl_logo_small.png)

## Name Directory Creation

These set of scripts are a functional approach to creating a domain specific LOD name directory. It works with extract files that are sequentially processed, no DB interface needed just the extracts and the scripts. The scripts uses keywords to build our Jazz directory but the keywords could easily be replaced to create a name directory for other domains. A lot of the process it designed so it will work on a VPS but some parts (filterLOCskos.py) needed to be done locally.

### Installing:

Requires osx/linux command line tools, grep, wget, etc..

####Extracts Needed:

The process requires a number of extract files from dbpedia and the Library of Congress

**DBpedia:**

(When a new version of dbpedia extract comes you would need to change the urls below)

* Articles Categories
  * Contains all the article categories in wikipedia
	http://downloads.dbpedia.org/3.9/en/article_categories_en.nt.bz2
	
* Persondata
  * FOAF representation of persons 
   http://downloads.dbpedia.org/3.9/en/persondata_en.nt.bz2
   
* Ontology Infobox Types
  * Types of DBpedia entities
	http://downloads.dbpedia.org/3.9/en/instance_types_en.nt.bz2
	
* Short Abstracts
  * The short abstract used to find birth/death dates not in the data
	http://downloads.dbpedia.org/3.9/en/short_abstracts_en.nt.bz2
	
	
* Images
  * Optional, if you want to make a extra file with images/bios for each person.
	http://downloads.dbpedia.org/3.9/en/images_en.nt.bz2


**Library of Congress:**

* LC Name Authority File (MADS/RDF only)
  * http://id.loc.gov/static/data/authoritiesnames.nt.madsrdf.gz
	
* LC Name Authority File (SKOS/RDF only)
  * http://id.loc.gov/static/data/authoritiesnames.nt.skos.gz
  We need both to mashup and create a new person only authority lookup with the data we want.

	
Extract these files into the data directory (you are going to need a lot of space)


#### Running:
Building the directory is just running the scripts in order.

	python filterDBpediaJazzFile.py 	
	
This takes a article category approach to everything related to jazz and filters it down to people. It is diagramed in filterDBpediaJazzFile.pdf	
	
	python filterLOCskos.py
	
Takes the enormous LC data file and creates a new LC lookup that is more manageable. The first step it does it create personURIs.nt, this could be done locally and added to the extract data on a server to reduce the space needed. Making this file will take a long time as its greping a 30GB extract. The process is in filter_LOC_filterLOCskos.pdf.

	python addDatesToJazzPeople.py

This adds birth and death dates to the name directory for people who don't have that data structured but it is in their abstract. Just cares about the year.


	python mergeLOCandDBpedia.py

This attempts to merge the two authorities based on name and dates, it makes a number of final name directory sameAs_*.nt files based on the confidence of the match. Documented in mergeLOCandDBpedia.pdf
	

	python filterToJazzData.py
	
Optional, this script creates an auxiliary file for the sameAs files which has the person image if in wikipedia and their short abstract.	
	
	
	
	
The MIT License (MIT)

Copyright (c) 2015 Matt Miller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
	
	
