from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Catalog, Base, CatalogItem, User

engine = create_engine('sqlite:///itemsCatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

User1 = User(name="Chilukuri Sundeep", email="sandychowdary.535@gmail.com", password="Sandymask35",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

User2 = User(name="John miller", email="john@gmail.com", password="1234",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User2)
session.commit()

# Catalog cricket

catalog1 = Catalog(name="Cricket")

session.add(catalog1)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Cricket Ball",
                           description="A cricket ball is a hard, solid ball used to play cricket. "
                                       "A cricket ball consists of cork covered by leather, "
                                       "and manufacture is regulated by cricket law at first-class level",
                           catalog=catalog1)

session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Cricket Bat",
                           description="A cricket bat is a specialised piece of "
                                       "equipment used by batsmen in the sport of cricket to hit the ball, "
                                       "typically consisting of a cane handle "
                                       "attached to a flat-fronted willow-wood blade",
                           catalog=catalog1)

session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Cricket Gloves",
                           description="Batting gloves are a component in Bat-and-ball games sportswear. "
                                       "Typically consisting of a leather palm and back "
                                       "made of nylon or another synthetic fabric, "
                                       "the glove covers one or both hands of a batter, "
                                       "providing comfort, prevention of blisters, "
                                       "warmth, improved grip, and shock absorption when hitting the ball",
                           catalog=catalog1)

session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Cricket Pads",
                           description="Pads (also called leg guards) are protective equipment "
                                       "used by batters in the sports of cricket and baseball, "
                                       "and by goaltenders in hockey, bandy and lacrosse. "
                                       "They serve to protect the legs "
                                       "from impact by a hard ball or puck at high speed "
                                       "which could otherwise cause injuries to the lower leg", catalog=catalog1)

session.add(catalog_item)
session.commit()

# Catalog Soccer

catalog2 = Catalog(name="Soccer")

session.add(catalog2)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Soccer Ball",
                           description="", catalog=catalog2)
session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Goal Post",
                           description="", catalog=catalog2)
session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Goal Jersy",
                           description="", catalog=catalog2)
session.add(catalog_item)
session.commit()

# Catalog Tennis
catalog3 = Catalog(name="Tennis")

session.add(catalog3)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Tennis Ball",
                           description="", catalog=catalog3)
session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Tennis Racket",
                           description="", catalog=catalog3)
session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Tennis Net",
                           description="", catalog=catalog3)
session.add(catalog_item)
session.commit()

# Catalog Batmenton
catalog4 = Catalog(name="Batmenton")

session.add(catalog4)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Batmenton Ball",
                           description="", catalog=catalog4)
session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Batmenton Racket",
                           description="", catalog=catalog4)
session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Batmenton Net",
                           description="", catalog=catalog4)
session.add(catalog_item)
session.commit()

print("Records Inserted")
