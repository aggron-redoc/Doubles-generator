from replit import db

for key in db.keys():
  del db[key]

# print(db['abc'])