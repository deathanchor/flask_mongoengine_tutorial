# Flask MongoEngine Tutorial, Part IV: Database

## Databases in Flask
We'll be using MongoDB as our db server and using [MongoEngine](mongoengine.org) python package to interact with our DB. MongoEngine is a _Object Relation Mapper_ or **ORM** this allows us to interact with objects instead of having to directly interact with DB writing queries and managing settings.

## Setup
For the setup, all you need to do is startup mongod. Yep that's it. For the remainder we'll assume you are running the server on the localhost on the default port.

## Configuration
We need to initialize the app with mongoengine and define a db object that we can use in the models.

Update the `app/__init__.py` file:
```
from flask import Flask
import mongoengine

app = Flask(__name__)
app.config.from_object("config")
db = mongoengine
db.connect('microblog') # connects to database named microblog

from app import views, models
```

We'll used the `db` object along with the flask.models to design our object models.

# The database model

For the DB model, we don't need to get into details about how to manage things in the DB, but you should be aware that you can customize the data model to optimize for queries and data storage options.

The basic model of a user would be `nickname` and `email` both which are basically strings. The beauty with MongoDB is you aren't required to specify the size of the values, but it is possible to have the data model enforce size limits.
We'll also add a `created` field containing a timestamp of when the document was created and we'll have it default to the current UTC time when the document gets created.
Also the `id` field is automatically created by mongodb, and it will be the `primary_key` unless we choose soemthing else. MongoDB will guarantee the `id` `ObjectId` will be unique within the collection automatically.

Create the `app/models.py` file:
```
from app import db
import datetime


class User(db.Document):
    nickname = db.StringField( max_length=64 )
	email = db.StringField( max_length=120, unique=True, required=True )
	created = db.DateTimeField( default=datetime.datetime.utcnow ) # utc to keep it universal

    def __repr__(self):
		return '<User %r>' % ( self.nickname )

```

For posts, we'll want to store `body`, `timestamp`, and of course the `user` associated with the post which we'll store as `author`, but will only contain the DBReference to `user` document. So this is appeneded to the `app/models.py` file:

```
class Post(db.Document):
    body = db.StringField( max_length=140 )
    timestamp = db.DateTimeField( default=datetime.datetime.utcnow )
    author = db.ReferenceField( User )

    meta = { 'allow_inheritance' : True }

    def __repr__(self):
        return '<Post %r>' % (self.body)

```

# Play Time

That's right, there is no initializing of the DB. MongoDB creates database, collections, indexes all on the fly, and MongoEngine setups indexes based on the document object definitions and the `meta` settings.

So while in the parent directory of the `app/` you can start up python so it will use relative paths for library imports of the application:

```
>>> from app import db, models
```

Loads the db and models so we can use them directly.

Let's create a new user:

```
>>> u = models.User(nickname='susan', email='susan@email.com')
>>> u.save()
<User u'susan'>
```

The user isn't written to the DB until we perform the `u.save()` but we can do any updates to the object and it won't be reflective in the DB until we preform the `u.save()` call.

And let's add another user:
```
>>> u = models.User(nickname='john', email='john@email.com')
>>> u.save()
<User u'john'>
```

Now let's query our users:
```
>>> users = models.User.objects()
>>> for u in users:
...    print(u.id, u.nickname, u.email, str(u.created))
...
(ObjectId('575222c29da88d086012aad7'), u'susan', u'susan@email.com', '2016-06-03 20:55:55.361000')
(ObjectId('575227629da88d088a7c0000'), u'john', u'john@email.com', '2016-06-03 20:56:51.860000')
```

Here's how we can get a full `ListResult` return from MongoEngine first unsorted, then sorted by nickname:
```
>>> models.User.objects.all()
[<User u'susan'>, <User u'john'>]
>>> models.User.objects.all().order_by('nickname')
[<User u'john'>, <User u'susan'>]
```

Now let's grab one user and we'll make a post:
```
>>> u = models.User.objects( nickname='susan' )[0]
>>> u
<User u'susan'>

>>> import datetime
>>> p = models.Post(body='my first post!', author=u)
>>> p.save()
<Post u'my first post!'>
```

Now we can query the posts and access the `user` object directly from the post's `author` field:

```
>>> posts = models.Post.objects.all()
>>> for p in posts:
...  print(p.id,p.author.nickname,p.body)
...
(ObjectId('575234b69da88d089312e069'), u'susan', u'my first post!')
```

## Final cleanup

Let's cleanup the db of all the data we created:
```
>>> models.User.objects.delete()
2
>>> models.Post.objects.delete()
1
```


