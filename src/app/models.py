from app import db
import datetime

db.connect('microblog')


class User(db.Document):
	nickname = db.StringField( max_length=64 )
	email = db.StringField( max_length=120, unique=True, required=True )
	created = db.DateTimeField( default=datetime.datetime.utcnow ) # utc to keep it universal

	meta = {
		'indexes' : [
			('email', '-created')
		]
	}

	def __repr__(self):
		return '<User %r>' % ( self.nickname )

class Post(db.Document):
	body = db.StringField( max_length=140 )
	timestamp = db.DateTimeField( default=datetime.datetime.utcnow )
	author = db.ReferenceField( User )

	meta = { 'allow_inheritance' : True }

	def __repr__(self):
		return '<Post %r>' % (self.body)
	

