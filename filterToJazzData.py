import sys
import os



def main():


	
	locURIs = {}
	DBPURIs = {}
	
	manyDB = []
	manyLOC = []
	
	allLines = []
	
	fileNames = ['sameAs_high.nt', 'sameAs_medium.nt',  'sameAs_low.nt', 'sameAs_perfect.nt', 'sameAs_many.nt', 'sameAs_none.nt']
	
	#'sameAs_many.nt', 
	
	for file in fileNames:
		fileOpen = open("data/" + file, 'r')
		print file
		for line in fileOpen:
			quad = line.split();
			
			
			if locURIs.has_key(quad[2]):
				print quad[2]
				
			locURIs[quad[2]] = quad[2]
			
			if DBPURIs.has_key(quad[0]):
				print quad[0]
				
			DBPURIs[quad[0]] = quad[0]			
			
			
			
		fileOpen.close()
		
	
 	 
	
	print len(locURIs)
	
	
	
	data_string = open('data/personauthoritiesnames.nt.skos', 'r')
	output = open('data/jazzData.nt', 'w')
	
	counter = 0
	added = 0
	
	for line in data_string:	
		
		
		counter = counter + 1 
		if counter % 1000000 == 0:
			print counter, '(',added,')'
			
		quad = line.split();
		
	 
		if locURIs.has_key(quad[0]):
		
			if line.find('#prefLabel') != -1 or line.find('#altLabel') != -1:
			
				#see if it has unicode stuff, we are not dealing with that right now
				try:
					line.encode('ascii')
				except UnicodeDecodeError:					
					#print "Not",line
					continue			 

					
				if line.find('\u') == -1:	
					added = added + 1
					if line not in allLines:
						allLines.append(line)
						output.writelines(line)	
		 

	data_string.close()
		 
 
	data_string = open('data/jazzPeople.nt', 'r')
 	
	counter = 0
	added = 0
	
	for line in data_string:	
		
		
		counter = counter + 1 
		if counter % 1000000 == 0:
			print counter, '(',added,')'
			
		quad = line.split();
		
	 
		if DBPURIs.has_key(quad[0]):
		
			

			
			if quad[1] != '<http://xmlns.com/foaf/0.1/surname>' and quad[1] != '<http://xmlns.com/foaf/0.1/givenName>' and quad[1] != '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>': 
				added = added + 1
				if line not in allLines:
					allLines.append(line)
					output.writelines(line)	


 

	data_string.close()
	
	data_string = open('data/images_en.nt', 'r')
 	
	counter = 0
	added = 0
	
	for line in data_string:	
		
		
		counter = counter + 1 
		if counter % 1000000 == 0:
			print counter, '(',added,')'
			
		quad = line.split();
		
	 
		if DBPURIs.has_key(quad[0]):
		
			

		
			if quad[1] == '<http://dbpedia.org/ontology/thumbnail>':
				added = added + 1
				if line not in allLines:
					allLines.append(line)
					output.writelines(line)	


					
	data_string.close()
	
	data_string = open('data/short_abstracts_en.nt', 'r')
 	
	counter = 0
	added = 0
	
	for line in data_string:	
		
		
		counter = counter + 1 
		if counter % 1000000 == 0:
			print counter, '(',added,')'
			
		quad = line.split();
		
	 
		if DBPURIs.has_key(quad[0]):
		

		
			if quad[1] == '<http://www.w3.org/2000/01/rdf-schema#comment>':
				added = added + 1
				if line not in allLines:
					allLines.append(line)
					output.writelines(line)								
					









if __name__ == '__main__':
        main()