from app import db,User
db.create_all()
user = User(username='LPAdmin009182',password='00LP2022adminP')
db.session.add(user) 
db.session.commit()