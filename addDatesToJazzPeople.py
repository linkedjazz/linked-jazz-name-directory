import sys, os, re

def main():

	
	  
	#load all the people, we need  to know if a abstract object is a person or not
	peopleNames = {}
	
	counter = 0
	hasDate = 0
	
	
	people = open("data/jazzPeople.nt", 'r')
	print "Figuring out who has birth/death dates"
	for line in people:

		counter = counter+1
		 
		if counter % 100000 == 0:
			print "procssed " +  str(counter / 100000)  + "00k lines"
		
		if counter % 1000000 == 0:
			print "procssed ", counter / 1000000,"Million lines!"
 	
		quad = line.split();
		
		
		
		
		
		if peopleNames.has_key(quad[0]):
		
			if quad[1] == "<http://dbpedia.org/ontology/birthDate>" or quad[1] == "<http://dbpedia.org/ontology/deathDate>":
				peopleNames[quad[0]] = True
				hasDate=hasDate+1
			
		else:
		
			if quad[1] == "<http://dbpedia.org/ontology/birthDate>" or quad[1] == "<http://dbpedia.org/ontology/deathDate>":
				peopleNames[quad[0]] = True
				hasDate=hasDate+1
			else:
				peopleNames[quad[0]] = False
		
	people.close()
	
	
	print hasDate, "people have some date", hasDate - len(peopleNames), " have no date"
	
	#for key, value in peopleNames.iteritems():
	#	print key, value

 	people = open("data/short_abstracts_en.nt", 'r')
	
	append = open("data/jazzPeople.nt", "a")
	
	for line in people:	
		quad = line.split();
		
		born = 0
		died = 0
		
		if peopleNames.has_key(quad[0]):
			if peopleNames[quad[0]] == False:
				
					
				desc = ''
				desc = " ".join(quad[2:])
				desc = desc[1:desc[1:].find('@en')]			

				 
				if len(re.findall(r'\d{4}.*&ndash;.*\d{4}',desc))!=0:
				
					dateStr = re.findall(r'\d{4}.*&ndash;.*\d{4}',desc)[0]
					
					dateStr = re.findall(r'\d{4}',desc)
					born = dateStr[0]
					died = dateStr[1]
					
				elif len(re.findall(r'\d{4}.*&mdash;.*\d{4}',desc))!=0:
				
					dateStr = re.findall(r'\d{4}.*&mdash;.*\d{4}',desc)[0]
					
					dateStr = re.findall(r'\d{4}',desc)
					born = dateStr[0]
					died = dateStr[1]					

				elif len(re.findall(r'\d{4}.*\\u2013.*\d{4}',desc))!=0:
				
					dateStr = re.findall(r'\d{4}.*\\u2013.*\d{4}',desc)[0]
					
					dateStr = re.findall(r'\d{4}',desc)
					born = dateStr[0]
					died = dateStr[2]					
				
				elif len(re.findall(r'\d{4}.*\\u2014.*\d{4}',desc))!=0:
				
					dateStr = re.findall(r'\d{4}.*\\u2014.*\d{4}',desc)[0]
					
					dateStr = re.findall(r'\d{4}',desc)
					born = dateStr[0]
					died = dateStr[2]					
				elif len(re.findall(r'\d{4}.*\\u2020.*\d{4}',desc))!=0:
				
					dateStr = re.findall(r'\d{4}.*\\u2020.*\d{4}',desc)[0]
					
					dateStr = re.findall(r'\d{4}',desc)
					born = dateStr[0]
					died = dateStr[2]						
				
				elif len(re.findall(r'\d{4}.*-.*\d{4}',desc))!=0:
				
					dateStr = re.findall(r'\d{4}.*-.*\d{4}',desc)[0]
					
					dateStr = re.findall(r'\d{4}',desc)
					born = dateStr[0]
					died = dateStr[1]	
					
				elif len(re.findall(r'.*born.*\d{4}',desc))!=0:
				
					dateStr = re.findall(r'.*born.*\d{4}',desc)[0]
					
					dateStr = re.findall(r'\d{4}',desc)
					born = dateStr[0]
					
				elif len(re.findall(r'.*Born.*\d{4}',desc))!=0:
				
					dateStr = re.findall(r'.*Born.*\d{4}',desc)[0]
					
					dateStr = re.findall(r'\d{4}',desc)
					born = dateStr[0]
					
				elif len(re.findall(r'.*died.*\d{4}',desc))!=0:
				
					dateStr = re.findall(r'.*died.*\d{4}',desc)[0]
					
					dateStr = re.findall(r'\d{4}',desc)
					died = dateStr[0]	

				elif len(re.findall(r'\(b.*\d{4}\)',desc))!=0:
				
					dateStr = re.findall(r'\(b.*\d{4}\)',desc)[0]
					
					dateStr = re.findall(r'\d{4}',desc)
									
 					born = dateStr[0]					
				elif len(re.findall(r'b.*\d{4}\,',desc))!=0:
				
					dateStr = re.findall(r'b.*\d{4}\,',desc)[0]
					
					dateStr = re.findall(r'\d{4}',desc)
									
 					born = dateStr[0]						
				
				#else:
				
					#if len(re.findall(r'\d{4}',desc)) != -1:
					#	print desc, born, died, "\n"
					

				
				
				if born != 0 or died != 0:
					hasDate=hasDate+1
				
	
				if died != 0:
					append.writelines(quad[0] + ' ' + '<http://dbpedia.org/ontology/deathDate> "' + died + '-01-01"^^<http://www.w3.org/2001/XMLSchema#date> .' + "\n")
				
				if born != 0:
					append.writelines(quad[0] + ' ' + '<http://dbpedia.org/ontology/birthDate> "' + born + '-01-01"^^<http://www.w3.org/2001/XMLSchema#date> .' + "\n")
	
	
	
	
	
	print hasDate, 'of', len(peopleNames)
	
	 



 


if __name__ == '__main__':
        main()