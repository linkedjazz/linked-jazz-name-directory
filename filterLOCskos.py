import sys
import os



def main():


	try:
		with open('data/personURIs.nt'): pass
	except IOError:
   		print "Building personURIs.nt"
		os.system('grep "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.loc.gov/mads/rdf/v1#PersonalName>" data/authoritiesnames.nt.madsrdf > data/personURIs.nt')


	personNames = {}
	
	peopleFile = open("data/personURIs.nt", 'r')
	print "building name list"
	for line in peopleFile:
	
		quad = line.split();
		
		
		if quad[0].find('authorities/names') != -1:
			personNames[quad[0]] = 0 

	peopleFile.close()			
		
	
	print len(personNames)
	 
	
	#holds all the unique individals
	nodes = []
	nodes_rdf = []
	edges = []
	nodesNames = []
	
	data_string = open('data/authoritiesnames.nt.skos', 'r')
	output = open('data/personauthoritiesnames.nt.skos', 'w')
	
	counter = 0
	added = 0
	
	for line in data_string:	
		
		
		counter = counter + 1 
		if counter % 1000000 == 0:
			print counter, '(',added,')'
			
		quad = line.split();
		
	 
		if personNames.has_key(quad[0]):
		
			if line.find('#prefLabel') != -1 or line.find('#altLabel') != -1:
			
				#see if it has unicode stuff, we are not dealing with that right now
				try:
					line.encode('ascii')
				except UnicodeDecodeError:					
					#print "Not",line
					continue			 

					
				if line.find('\u') == -1:	
					added = added + 1
					output.writelines(line)	
		 

 
	


 













if __name__ == '__main__':
        main()