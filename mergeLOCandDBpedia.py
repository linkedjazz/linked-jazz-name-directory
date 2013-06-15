import sys, os, re, urllib, time


def main():


	if not os.path.exists('data/loc_single'):
   		os.makedirs('data/loc_single')

 
	dbData = open('data/jazzPeople.nt', 'r')
	personNames = {}
	personBirthDates = {}
	personDeathDates = {}
	nameCollisons = {}
	matchesBothDate = []
	matchesBothDateURIs = []	
	matchesSingleDate = []
	
	foundCheckList = []
	possibleLOC={}
	allLOC = {}
	
	for line in dbData:
		
		quad = line.split()
		if quad[1] == '<http://xmlns.com/foaf/0.1/name>':
			name = ''
			name = " ".join(quad[2:])
			name = name[1:name[1:].find('@en')]	
			
			if len(name) < 5:
				print name, line
			
			name = name.replace('\\','')
			
			if personNames.has_key(name) == False:
			
				personNames[name] = quad[0]
				
			else:
			
				if personNames[name] != quad[0]:
					if nameCollisons.has_key(name):
					
						if quad[0] not in nameCollisons[name]:
							nameCollisons[name].append(quad[0])
					else:
						nameCollisons[name]=[quad[0]]			
						
					print "1Name collision", name, line		
					print personNames[name], nameCollisons[name]
				
			addNames = []
			
			if name.find('"') != -1:
				 
				print name
				name = name.split('"')[0].strip() + ' ' + name.split('"')[2].strip()
				addNames.append(name)
			
			#we also want to pull their name from the URL, because that is often the most common variant of their name
			uri = quad[0]
			
			name = formatName(quad[0].split('/resource/')[len(quad[0].split('/resource/'))-1])			
			
			name = name.replace('\\','')
			
			addNames.append(name)
			#print name
			
			
			

			
			#remove any nick name and add that as well
			if name.find('"') != -1:

				
							
				print name
				 
				name = name.split('"')[0].strip() + ' ' + name.split('"')[2].strip()
				addNames.append(name)
			
	
			
			
			for aName in addNames:
				#is this name already in the lookup:
				print aName
				if personNames.has_key(aName):
					
					
					print "\t Name already in personNames"
					
					#yes, is it the same uir as this one?
					if personNames[aName] != quad[0]:
						
						print "\t Name Has Diffrent URI Attached"
						
						#no, it is a new UIR, is it aleady in the collision lookup?
						if nameCollisons.has_key(aName):
							
							print "\t Name already in collission"
							
							#yes, is this URI already in it?
							if quad[0] not in nameCollisons[aName]:
								
								print "\t Diffrent Name, adding to it"
								#no, add it
								nameCollisons[aName].appen(quad[0])
						
						else:
						
							#no, add a new array to the collison with it
							nameCollisons[aName] = [quad[0]]
							print "\t Creating new collission record"
				
				else:
					print "\t not yet in personNames, adding it"
					personNames[aName] = quad[0]
			

		
		if quad[1] == '<http://dbpedia.org/ontology/deathDate>':
			deathDate = ''
			deathDate = " ".join(quad[2:])
			deathDate = deathDate[1:deathDate[1:].find('-')+1]				
			
			if len(deathDate) != 4:
				print "Error death date: ", line
			else:
				personDeathDates[quad[0]] = deathDate
			
			#print deathDate
			
		if quad[1] == '<http://dbpedia.org/ontology/birthDate>':
			birthDate = ''
			birthDate = " ".join(quad[2:])
			birthDate = birthDate[1:birthDate[1:].find('-')+1]				
			if len(birthDate) != 4:
				print "Error birth date: ", line
			else:
				personBirthDates[quad[0]] = birthDate
			
 


 
	print len(personNames), len(personBirthDates), len(personDeathDates)
 
	
 
	temp = open("db_tmp.txt","w")
 	for key, value in personNames.iteritems():

			 
			
		line = key + ' ' + value
		
		if personBirthDates.has_key(value):
			line = line + ' ' + personBirthDates[value]
		if personDeathDates.has_key(value):
			line = line + ' ' + personDeathDates[value]				
		
		temp.writelines(line + "\n")
 
 
	
	for key, value in nameCollisons.iteritems():
		
 		
		for x in value:
		
			line = key + ' ' + x
		
			if personBirthDates.has_key(x):
				line = line + ' ' + personBirthDates[x]
			if personDeathDates.has_key(x):
				line = line + ' ' + personDeathDates[x]				
		
			temp.writelines(line + "\n")			
			print line
			

  
	locFile = open('data/personauthoritiesnames.nt.skos', 'r')
	

	
	counter = 0
	counterMatched = 0
	
 	print "building name list"
	locDebug = open("loc_tmp.txt","w")
	for line in locFile:
		
		counter = counter+1
		
		
		#if counter % 100000 == 0:
		#	print "procssed " +  str(counter / 100000)  + "00k names"
		
		if counter % 1000000 == 0:
			print "procssed ", counter / 1000000,"Million names!"
 
			
		quad = line.split();
		name = " ".join(quad[2:])
		name = name[1:name[1:].find('@EN')]			
		
		name = name.replace('?','')
		
		year = re.findall(r'\d{4}', name)
	
		born = 0
		died = 0
		possibleNames = []
		
		if len(year) != 0:
			
			if len(year) == 1 and name[len(name)-1:] != '-':
				

				
				
				if name.find(' b.') != -1:
					born = year[0]
					#print "Born : ",year[0]
				elif name.find(' d.') != -1:
					died = year[0]
					#print "died : ",year[0]
				elif name.find(' fl.') != -1:
					born = year[0]
					#print "born(flourished) : ",year[0]		
				elif name.find('jin shi') != -1:
					born = year[0]
					#print "born(third stage) : ",year[0]							
				elif name.find('ju ren') != -1:
					born = year[0]
					#print "born(second stage) : ",year[0]	
				elif len(re.findall(r'\d{3}\-', name)) != 0:
					
					
					year = re.findall(r'\d{3}\-', name)					
					born = year[0][0:3]
					#print "born : ", year[0][0:3]	
					#now get the death year
					died = re.findall(r'\d{4}', name)[0]
					
				elif len(re.findall(r'\-\d{4}', name)) != 0:
					died = re.findall(r'\-\d{4}', name)[0][1:]

				elif name.find(' ca. ') != -1 or name.find(' ca ') != -1:
					born = year[0]
					#print "born(ca) : ",year[0]	
				elif name.find(' b ') != -1:
					born = year[0]
					#print "Born : ",year[0]
				elif name.find(' d ') != -1:
					died = year[0]
					#print "died : ",year[0]
				elif name.find(' born ') != -1:
					born = year[0]
					#print "Born : ",year[0]
				elif name.find(' died ') != -1:
					died = year[0]
					#print "died : ",year[0]					
				else:
					#print name, "\n"
					#print "error: cannot figure out this date, update the regex"
					#we have hit like 90% of the cases here, now just stright up weird sutff, so just grab the date
					born = year[0]
					
				#print len(year)
				
			elif len(year) == 1 and name[len(name)-1:] == '-':	
				born = year[0]
				
			elif len(year) == 2:
				born = year[0]
				died = year[1]
			elif len(year) == 3:
				#they are doing "1999 or 2000 - blah blah blah"  take first and last
				born = year[0]
				died = year[2]				
			elif len(year) == 4:
				#they are doing "1999 or 2000 - blah blah blah"  take first and last
				born = year[0]
				died = year[3]				
				
			else:
				print name, "Coluld not process date \n"
				sys.exit()
		
		
			#print name, born, died
		
		
		#else:
		
			#these people would have lived < 0 bce - 999 AD, we currently do not care about them.
			#if len(re.findall(r'\d{3}', name)) != 0:
				#print name
		
		#personDates[quad[0]] = [born,died]
			
		
		#now process the name part 
		
		#chop off the rest where a number is detected to get rid of any date
		if re.search(r'\d{1}',name) != None:			
			name = name[0:name.find(re.search(r'\d{1}',name).group())]			
			name=name.strip()
		
		#now chop off anything past the second comma, it is not name stuff afterwards, also with 3 commas are a lot of "sir" and "duke of earl" etc, dont care about that stuff
		if len(re.findall(',', name)) == 2 or len(re.findall(',', name)) == 3:			
			name = name.split(',')[0] + ', ' + name.split(',')[1]
			#print name, '|', newname
			
		
		if name.find('\"') != -1:
			name = name.replace("\\",'')
		
		if len(re.findall(',', name)) == 1:
		
			if name.find('(') == -1:
				#there is no pranthetical name
				
				newname = name.split(',')
				newname = newname[1] + ' ' + newname[0]
				#print name, '|', newname
				possibleNames.append(newname.strip())
				
				
				#we want to add that name, but also add a version with out a middle intial, if that it is present
				if len(newname.split()) == 3 and (newname.split()[1][len(newname.split()[1])-1] == '.' or len(newname.split()[1]) == 1):								
					newname = newname.split()[0] + ' ' + newname.split()[2]			
					#print "\t" + newname
					possibleNames.append(newname.strip())

					
						
				
				
				#we also want to add a name, that if they only have an inital for the first part and a full middle name drop the first intital
				if len(newname.split()) == 3 and len(newname.split()[1]) > 2 and (newname.split()[0][len(newname.split()[0])-1] == '.' or len(newname.split()[1]) == 1):
					newname = newname.split()[1] + ' ' + newname.split()[2]			
					#print "\t" + newname
					possibleNames.append(newname.strip())
						
		
			
			else:
				
				#they have prenthasis in their name meaning that their long form of the name is contained in the pranthesis
				newname = name.split(',')
				newname = newname[1] + ' ' + newname[0]
				
				#cut out the stuff before the pran
				newname = newname[newname.find('(')+1:]
				newname = newname.replace(')','')
				#print name, '|', newname
				possibleNames.append(newname.strip())
				
	
				
				
				
				#now also cut out the middle inital if it is there and add that version
				if len(newname.split()) == 3 and (newname.split()[1][len(newname.split()[1])-1] == '.' or len(newname.split()[1]) == 1):								
					newname = newname.split()[0] + ' ' + newname.split()[2]			
					#print "\t" + newname
					possibleNames.append(newname.strip())

						
				
						

		else:
		
			#so here we are... the depths of the quirks
			if name.find('(') != -1:
			
				#if the very first thing is a inital, it is likely a abrrivated name and the full name is in the prans
				if len(name.split()[0])==2:
					if name.split()[0][1] == '.':
						newname = name.split('(')[1]
						newname = newname.replace(')','')
						possibleNames.append(newname.strip())
							
						#print name, '|', newname
				
				#if len(name.split()[len(name.split())-1])==2:
				#	if name.split()[len(name.split())-1][1] == '.':				
				#		print name, '|'
		
				else:
					#this will be stuff like P-King (Musician), or Shyne (Rapper), stuff we are intrested in, nicknames, so cut out the descriptor
					newname = name.split('(')[0].strip()
					
					#TODO: if we really care to take this further here is a spot where we will lose some names
					#the quirks get very specific and would need a lot more rules
					
					#print name, '|', newname
					possibleNames.append(newname.strip())
					
			else:
				#print name, '|'
				newname = name.strip()
				
				#single names here, add them in
				possibleNames.append(newname.strip())
					
	
		#print possibleNames
		
		
		
		#skip logic:
		if int(born) != 0 and int(born) < 1875:
			continue
		
		
		 
		
		for aPossible in possibleNames:
		
			 
		
			if personNames.has_key(aPossible):
			
				#we have a match (!)
				
				#add all the Ids we are going to check into a list
				useURIs = []			
				
				#the main one
				useURIs.append(personNames[aPossible])
				
				#check for collision names, names that are the same but reflect diffrent URIs
				if nameCollisons.has_key(aPossible):
					for collison in nameCollisons[aPossible]:
						useURIs.append(collison)
				
				
				
				for useURI in useURIs:
			
					
				
					locDebug.writelines(aPossible + ' ' + str(born) + ' ' + str(died) + "\n")
				
					if allLOC.has_key(aPossible):				
						#it is in here already, see if it has this URI
						if quad[0] not in allLOC[aPossible]:
							allLOC[aPossible].append(quad[0])
					
					else:
						allLOC[aPossible] = [quad[0]]
				
				
					
					
					didMatched = False
				
					
					if personBirthDates.has_key(useURI) and personDeathDates.has_key(useURI):
						
						if int(born) != 0 and int(died) != 0 and int(personBirthDates[useURI]) != 0 and int(personDeathDates[useURI]) != 0:
							
							if (int(personBirthDates[useURI]) == int(born)) and (int(died) == int(personDeathDates[useURI])):
								
								if [useURI, quad[0]] not in matchesBothDate:
								
									didMatched=True
									counterMatched = counterMatched + 1
									matchesBothDate.append([useURI, quad[0]])
									foundCheckList.append(useURI)
									
									matchesBothDateURIs.append(useURI)
							
									#print aPossible, quad[0], born, died
									#print aPossible, useURI, personBirthDates[useURI],  personDeathDates[useURI]												
							
									continue
					
					
					


					#see if birth years match
					if personBirthDates.has_key(useURI):				
						if int(personBirthDates[useURI]) == int(born) and int(personBirthDates[useURI]) != 0 and int(born) != 0:					
						
							if [useURI, quad[0]] not in matchesSingleDate:
								#print personNames[aPossible], '=', quad[0]
								didMatched=True
								counterMatched = counterMatched + 1
								matchesSingleDate.append([useURI, quad[0]])
								foundCheckList.append(useURI)

								#print aPossible, quad[0], born, "born match"
								#print aPossible, useURI, personBirthDates[useURI]
								
								continue


								
					#does it have a death date match?					
					if personDeathDates.has_key(useURI):				
						if int(personDeathDates[useURI]) == int(died) and int(personDeathDates[useURI]) != 0 and int(died) != 0:					

						
							if [useURI, quad[0]] not in matchesSingleDate:
								#print personNames[aPossible], '=', quad[0]
								matchesSingleDate.append([useURI, quad[0]])
								didMatched=True
								counterMatched = counterMatched + 1		
								foundCheckList.append(useURI)
								
								#print aPossible, quad[0], died, "death match"
								#print aPossible, useURI, personDeathDates[useURI]	
								
								continue								
						
								 
 
 
	#we are now going to remove any matches from matchesSingleDate where there is a perfect date match already
	temp  = []
	
	for aSingleDateMatch in matchesSingleDate:
	
		if aSingleDateMatch[0] not in matchesBothDateURIs:
			temp.append(aSingleDateMatch)
		else:
			
			for x in matchesBothDate:
				if x[0] == aSingleDateMatch[0]: 
					print "Attempted Dupe", aSingleDateMatch
					print "With", x
	
	
	
	
	matchesSingleDate = list(temp)
	
	
	matchedSingle = []
	matchedMany = []
	matchedNone = []
	
	for key, value in personNames.iteritems():
		
		if value not in foundCheckList:
			#print "Not matched " + value  + ' ' +  key
			
			if allLOC.has_key(key):
				
				if len(allLOC[key]) == 1:
					#print "\tOnly one possible LOC match:" + allLOC[key][0]
					matchedSingle.append([value,allLOC[key][0]])
				else:
					#print "\t 1+ possible LOC match:", allLOC[key]
					matchedMany.append([value,allLOC[key]])
					
			else:
					matchedNone.append(value)
					
					

	print "	\n****Collision***\n"
	
	for key, value in nameCollisons.iteritems():
		
		
		for x in value:
		
			if x not in foundCheckList:
				#print "Not matched " + x  + ' ' +  key
				
				if allLOC.has_key(key):
					
					if len(allLOC[key]) == 1:
						#print "\tOnly one possible LOC match:" + allLOC[key][0]
						matchedSingle.append([x,allLOC[key][0]])
					else:
						#print "\t 1+ possible LOC match:", allLOC[key]
						matchedMany.append([x,allLOC[key]])						
				
				else:
					matchedNone.append(x)
	
	#for key, value in possibleLOC.iteritems():

		#if len(value) == 1:
		
			#if value not in matches:
			#	matches.append(value)
		
			#print key, '=', value
		 
	
	
	#make sure there are no duplicates, as in same DB to LOC records in the singles
	tempCopy = []
	
	for aSingle in matchedSingle:
	
		add = True
	
		for anotherSingle in tempCopy:
		
			if aSingle[0] == anotherSingle[0] and aSingle[1] == anotherSingle[1]:
				add = False
	
		if add:
			tempCopy.append(aSingle)
			
	
	matchedSingle = list(tempCopy)
	
	#now we are going to go through the singles and pull out anyone that has been added twice
	#this can happen for common names born in the same year, move them to the 1->many list
	matchedSingleCheck = []
	matchedSingleDupes = []
	for aSingle in matchedSingle:
		
		if aSingle[0] not in matchedSingleCheck:
			matchedSingleCheck.append(aSingle[0])
		else:		
		
			print "Dupe in singles found:", aSingle
			matchedSingleDupes.append(aSingle[0])
	
	
	singleDupes = {}
	tempCopy = []
	print len(matchedSingle)
	for aSingle in matchedSingle:
	
		if aSingle[0] in matchedSingleDupes:
			
			if singleDupes.has_key(aSingle[0]):
				singleDupes[aSingle[0]].append(aSingle[1])
			else:
				singleDupes[aSingle[0]] = [aSingle[1]]
	
		else:
			tempCopy.append(aSingle)
	
	matchedSingle = list(tempCopy)
	
	print len(matchedSingle)
	print singleDupes
	
	#add them to the matchedmany list
	for key, value in singleDupes.iteritems():
		matchedMany.append([key,value])
	


	#we now need to do the same for matchesSingleDate, they could have matched a single date true, but it could  matched to other people
	matchesSingleDateCheck = []
	matchesSingleDateDupes = []
	for aSingle in matchesSingleDate:
		
		if aSingle[0] not in matchesSingleDateCheck:
			matchesSingleDateCheck.append(aSingle[0])
		else:		
		
			print "Dupe in single date found:", aSingle
			matchesSingleDateDupes.append(aSingle[0])		

			
	singleDateDupes = {}
	tempCopy = []
	print len(matchesSingleDate)
	for aSingle in matchesSingleDate:
	
		if aSingle[0] in matchesSingleDateDupes:
			
			if singleDateDupes.has_key(aSingle[0]):
				singleDateDupes[aSingle[0]].append(aSingle[1])
			else:
				singleDateDupes[aSingle[0]] = [aSingle[1]]
	
		else:
			tempCopy.append(aSingle)
	
	matchesSingleDate = list(tempCopy)
	print len(matchesSingleDate)
	
	#add them to the matchedmany list
	for key, value in singleDateDupes.iteritems():
		matchedMany.append([key,value])	
	
	
	print singleDateDupes
 
	#TODO: This part needs to be fixed so the call to the LOC site is syncrounous, and wait for the file to be ready...
	
	machtedSingleJazz = []
	machtedSingleNoJazz = []
	
	machtedSingleNoJazzLOC = []
	
	for x in matchedSingle:
	
		url = x[1]
		id = formatName(url.split('/names/')[len(url.split('/names/'))-1])
		foundJazz = False
		
		if os.path.exists('data/loc_single/' + id + '.nt') == False:
			os.system('wget --output-document="data/loc_single/' + id + '.nt" "http://id.loc.gov/authorities/names/' + id + '.nt"')

			#sleep as a TODO fix, 
			time.sleep( 1.5 )

		
		if os.path.exists('data/loc_single/' + id + '.nt'):
			
			f = open('data/loc_single/' + id + '.nt', 'r')
			
			for line in f:
				line = line.lower()
				if line.find('jazz') != -1 or line.find('music') != -1 or line.find('blues') != -1 or line.find('jazz') != -1 or line.find('vocal') != -1:
					print line
					foundJazz = True
					
			
			
			f.close()
			 

		else:
			print 'data/loc_single/' + id + '.nt does not exist'
 
		if id in machtedSingleNoJazzLOC:
			foundJazz = False
			print "Dupe detected trying to assign" ,x
	
	
		if foundJazz:
			machtedSingleJazz.append(x)
			machtedSingleNoJazzLOC.append(id)
			
			
		else:
			machtedSingleNoJazz.append(x)
			
	

	
	
	
	
	print len(matchesBothDate), " BothDate Matches", len(matchesSingleDate), " Single Date Matches", len(matchedSingle), "Single LOC", len(matchedMany), "Multiple LOC matches", len(matchedNone), "No Matches"
	#print len(matches)+ len(matchedSingle)+len(matchedMany) , " matched out of Total of about ", len(personNames)
 
	print len(matchedSingle) , " = " , len(machtedSingleJazz) , " keyword found and ", len(machtedSingleNoJazz), " no keyword found"

	
	
	#make the sameas files
	
	allLines=[]
	
	temp = open("data/sameAs_perfect.nt","w")
 	for value in matchesBothDate:		
	
		line = value[0] + ' <http://www.w3.org/2002/07/owl#sameAs> ' + value[1] + " . \n";
		if line not in allLines:
			temp.writelines(line)
			allLines.append(line)
	
	temp = open("data/sameAs_high.nt","w")
 	for value in matchesSingleDate:		
	
		line = value[0] + ' <http://www.w3.org/2002/07/owl#sameAs> ' + value[1] + " . \n";
		if line not in allLines:
			temp.writelines(line)
			allLines.append(line)

	
	temp = open("data/sameAs_medium.nt","w")
 	for value in machtedSingleJazz:		

		line = value[0] + ' <http://www.w3.org/2002/07/owl#sameAs> ' + value[1] + " . \n";
		if line not in allLines:
			temp.writelines(line)
			allLines.append(line)
	
	temp = open("data/sameAs_low.nt","w")
	for value in machtedSingleNoJazz:	
	
		line = value[0] + ' <http://www.w3.org/2002/07/owl#sameAs> ' + value[1] + " . \n";
		if line not in allLines:
			temp.writelines(line)
			allLines.append(line)	
		
	temp = open("data/sameAs_many.nt","w")
 	for value in matchedMany:		
	
		for x in value[1]:
			temp.writelines(value[0] + ' <http://www.w3.org/2004/02/skos/core#closeMatch> ' + x + " . \n") 	
		
	temp = open("data/sameAs_none.nt","w")
 	for value in matchedNone:		
		temp.writelines(value + ' <http://www.w3.org/2002/07/owl#sameAs> ' + '<none>' + " . \n") 		
		
 
def formatName(name):
	
	#decode it to get rid of URL char codes 
 	
	name = urllib.unquote(name)
	
	#stop at the first pranathesis, so we dont get things like (jazz_player)
	name = name[0:name.rfind('(')]
	
	name = name.replace('_',' ').replace('>','').strip()

	name = name.replace(",","")
	name = name.replace("Jr.","Jr")				
	name = name.replace("Sr.","Sr")	 
 
	return name












if __name__ == '__main__':
        main()