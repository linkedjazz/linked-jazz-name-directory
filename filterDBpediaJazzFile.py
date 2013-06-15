import sys
import os



def main():

	
	print "Extacting music related catagories.."
	os.system('grep "Jazz\|jazz\|blues\|swing\|bop" data/article_categories_en.nt > data/allJazz.nt')

	#this can be modified to get more expected results
	os.system('grep -v "rhythm_and_blues\|Rhythm_and_blues" data/allJazz.nt > data/allJazz.tmp.nt')
	os.system('rm data/allJazz.nt')
	os.system('mv data/allJazz.tmp.nt data/allJazz.nt')

	 
	
	#print "Extacting artists"
	#os.system('grep "<http://dbpedia.org/ontology/MusicalArtist>\|<http://dbpedia.org/ontology/Artist>" data/instance_types_en.nt > data/allArtists.nt')
	
	  
	#load all the people, we need  to know if a abstract object is a person or not
	peopleNames = {}
	
	counter = 0
	
	people = open("data/persondata_en.nt", 'r')
	print "building name list"
	for line in people:

		counter = counter+1
		 
		if counter % 100000 == 0:
			print "procssed " +  str(counter / 100000)  + "00k lines"
		
		if counter % 1000000 == 0:
			print "procssed ", counter / 1000000,"Million lines!"
 	
		quad = line.split();
		
		if peopleNames.has_key(quad[0]):
			peopleNames[quad[0]].append(line)
		else:
			peopleNames[quad[0]] = [line]
		
	people.close()
	
	#load the list of artists
	allTypes = {}
	musicans = {}
 	athletes = {}
	albums = {}
	
	print "Loading rdf:type for people"
	types = open("data/instance_types_en.nt", 'r')
	counter = 0
	
	for line in types:
	
		counter = counter+1
		 
		if counter % 100000 == 0:
			print "procssed " +  str(counter / 100000)  + "00k lines"
		
		if counter % 1000000 == 0:
			print "procssed ", counter / 1000000,"Million lines!"	
	
		quad = line.split()		
		
		if quad[2] == "<http://dbpedia.org/ontology/MusicalArtist>":
			musicans[quad[0]] = 1
		if quad[2] == "<http://dbpedia.org/ontology/Athlete>":
			athletes[quad[0]] = 1			
		if quad[2] == "<http://dbpedia.org/ontology/Album>":
			albums[quad[0]] = 1			
			
			
		else:
			allTypes[quad[0]] = 1
		 
		 
	
	print len(musicans), len(allTypes)
	 
	
	dupeCheck = []
 
	
	data_string = open('data/allJazz.nt', 'r')
	
	output = open('data/jazzPeople.nt', 'w')
	
	for line in data_string:	
		
		quad = line.split();
		
		if quad[0] not in dupeCheck:		
		
			if peopleNames.has_key(quad[0]):
				
				
				
				if allTypes.has_key(quad[0]):
				
					#if they have a key check it
				
					if musicans.has_key(quad[0]):
				
						for x in peopleNames[quad[0]]:
							output.writelines(x)	
							
						dupeCheck.append(quad[0])
					
					else:
					
						if athletes.has_key(quad[0]):
							
							print "Not an musican ", line
						
						
						else:
						
							if albums.has_key(quad[0]):
								print "Not an musican ", line
							
							else:
								line = line.lower()
								#last chance here, it is possible that they have data in instance_type but they are not marked as being a musican... so
								if (line.find('jazz') != -1 or line.find('_music') != -1 or line.find('_blues_') != -1) and line.find('ensembl') == -1 and line.find('_players') == -1:
									for x in peopleNames[quad[0]]:
										output.writelines(x)								
									dupeCheck.append(quad[0])
							
								else:
								
									print "Not an musican ", line

					
				else:
				
					#otherwise, have to add them jsut to be safe
					for x in peopleNames[quad[0]]:
						output.writelines(x)	
						
					dupeCheck.append(quad[0])					








	print "Added " , len (dupeCheck) , " people"



if __name__ == '__main__':
        main()