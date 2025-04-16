import datetime

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime
cluster = MongoClient("mongodb+srv://seydou:passer@cluster0.3h4iw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["bakery"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)

@app.route("/", methods=["get","post"])
def reply():
   # response = MessagingResponse()
   # msg = response.message("bonjour le monde ")
   text = request.form.get("Body")
   number = request.form.get("From")
   response = MessagingResponse()
   user = users.find_one({"number": number})
   if bool(user) == False:
       response.message("Bonjour, Merci et bien venue a Ocasebebe.\nFaire un choix en suivant le menu Proposer\n1 Contacter nous \n2 Passer une commande")
       users.insert_one({"number": number, "status":"main","messages":[]})
   elif user["status"] =="main":
       try:
           option = int(text)
       except:
           response.message("Please entrer une reponse valide")
           return str(response)
       if option == 1:
           response.message("vous pouvez nous contacter sur le 4564656")
       elif option == 2:
           response.message("cas ou le client prend loption 2 commande")
           users.update_one({"number": number},{"$set": {"status": "ordering"}})
           response.message("\n1 Red velve \n2 Dark cake\n3 Red velve \n4 Dark cake\n5 Red velve \n6 Dark cake\n7 Red velve \n8 Dark cake\n9 Red velve ")
       elif option == 3:
           response.message("Nous somme ouvert 24/24")
       else:
           response.message('Entrer une reponse valide')
   elif user["status"] == "ordering":
       try:
           option = int(text)
       except:
           response.message("Please entrer une reponse valide")
           return str(response)
       if option == 0:
           users.update_one({"number":number},{"$set": {"status": "main"}})
           response.message(
               "Bonjour, Merci et bien venue a Ocasebebe.\nFaire un choix en suivant le menu Proposer\n1 Contacter nous \n2 Passer une commande")
       elif 1 <= option <= 9:
           cakes = ["red velvet cake","dark cake","ice cream",
                    "plum cake", "sponge cake","Genoise cake", "Angel Cake", "Carrat Cake", "fruit"]
           selected = cakes[option -1]
           users.update_one(
               {"number":number},{"$set": {"status": "address"}}
           )
           users.update_one(
               {"number": number}, {"$set": {"item": selected}}
           )
           response.message("Excellent choix entrer votre address")
       else:
           response.message("Entrer une reponse valide")
   elif user["status"] == "address":
       selected = user["item"]
       response.message("merci d'avoir commander")
       response.message(f"merci d'avoir commander {selected}")
       orders.insert_one({"number":number},{"$push":{"messages":{"text":text, "date":datetime.now()}}})
       users.update_one({"number":number},{"$set": {"status": "ordered"}})
   elif user["status"] == "ordered":
       response.message(
           "Bonjour, Merci voulez vous encore autre chose.\nFaire un choix en suivant le menu Proposer\n1 Contacter nous \n2 Passer une commande")
       users.update_one({"number": number}, {"$set": {"status": "main"}})

   users.update_one({"number": number}, {"$push": {"message": {"test": text , "date": datetime.now()}}})
   return str(response)

if __name__ == "__main__":
    app.run()
