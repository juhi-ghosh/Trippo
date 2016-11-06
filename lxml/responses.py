#!/usr/bin/python
from api_ai_request import api_request as api_request
import pymongo
from random import randint

client = pymongo.MongoClient()
db = client.traveldata

"""class Response_Functions:
	member-variables : self, data=[]
	member-functions : get_description,get_destination, get_review, ...
	one function againsta each intent. Fetches result from database, and formulates response
"""
class Response_Functions:
    def __init__(self):
    	self.data = []

    #Function called when intent is description
    def get_description(self,ids):
    	#print ids
	counter=(randint(0,3))
	res_list=["Hola!\n Let me guide your Travel,\n\n", "Well,\n\n", "Let me give you some details,\n\n", "Your Travel guide says,\n\n"]
    	print res_list[counter]+db.destinations.find({"name":ids.lower()})[0]["details"]

    #function called when intent is destination
    def get_destination(self,ids):
    	print db.destinations.find({"name":ids.lower()})[0]["places"]

    #function called when intent is rating
    def get_rating(self,ids):
	counter=(randint(0,3))
	res_list=["According to Traveller feedback,\n", "Suggested by Travellers,\n", "Several Travellers have given,\n", "Travellers say,\n"]
    	print res_list[counter]+db.destinations.find({"name":ids.lower()})[0]["ratings"] + ", for " +ids.title()
	print "You may also like to see this video review from a traveller,\n" + db.destinations.find({"name":ids.lower()})[0]["video_review"]

    #function called when intent is review
    def get_review(self,ids):
	print "Dear Traveller "+ ids.title()+" Reviews are as follows,\n"
    	print ">> " +str(db.destinations.find({"name":ids.lower()})[0]["reviews"][0])
	print "\n\n>> " +str(db.destinations.find({"name":ids.lower()})[0]["reviews"][1])


#main body
while(1):
	user_query = []
	query = raw_input("User : ")			#take query input from user
	user_query.append(query.split(".")) 	        #if query is seperated by full stop. send as 'n' diffrent queries to api.ai
	response = api_request(user_query)		#send query to api_ai and retrive a response dictionary

	if response["status"]["code"]!=200:
		print "Sorry. Server cannot be contacted."
		exit

	obj = Response_Functions()
	
	if response["result"]["action"]!="smalltalk.greetings":
		key1=response["result"]["parameters"]["place_name"].lower()
		key2=response["result"]["parameters"]["place_namecontext"].lower()

	#Matching action name with function call from Response_Functions call
	if response["result"]["action"]=="get_description":
		if key1:
			obj.get_description(key1)
		elif key2:
			obj.get_description(key2)
		else :
			print "Sorry we have'nt got any response for you"

	elif response["result"]["action"]=="get_destination":
		if key1:
			obj.get_destination(key1)
		elif key2:
			obj.get_destination(key2)
		else :
			print "Sorry we have'nt got any response for you"

	elif response["result"]["action"]=="get_rating":
		if key1:
			obj.get_rating(key1)
		elif key2:
			obj.get_rating(key2)
		else :
			print "Sorry we have'nt got any response for you"

	elif response["result"]["action"]=="get_review":
		if key1:
			obj.get_review(key1)
		elif key2:
			obj.get_review(key2)
		else :
			print "Sorry we have'nt got any response for you"

	elif response["result"]["action"]=="smalltalk.greetings":
		print response["result"]["fulfillment"]["speech"]





