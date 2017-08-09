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
                           description="A football, soccer ball, or association football ball is the ball "
                                       "used in the sport of association football. The name of the ball "
                                       "varies according to whether the sport is called 'football', "
                                       "'soccer', or 'association football'",
                           catalog=catalog2)
session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Goal Post",
                           description="Hurling and Gaelic football use the same goal structure. ... "
                                       "The goal posts are at least 6 meters high, and the crossbar is 2.44 "
                                       "meters above the ground. A goal is scored when the "
                                       "ball crosses below the crossbar and a point "
                                       "is scored when the ball passes above it.", catalog=catalog2)
session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Soccer Jersey",
                           description="While the replica jersey is made of 100 percent polyester, "
                                       "the authentic incorporates lycra that allows it to stretch "
                                       "around your muscles like a compression shirt. PUMA authentic "
                                       "jerseys feature a technology called powerCELL, while the "
                                       "replica fabric is made with dryCELL", catalog=catalog2)
session.add(catalog_item)
session.commit()

# Catalog Tennis
catalog3 = Catalog(name="Tennis")

session.add(catalog3)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Tennis Ball",
                           description="A tennis ball is a ball designed for the sport of tennis. "
                                       "Tennis balls are fluorescent yellow at major sporting events,"
                                       " but in recreational play can be virtually any color. "
                                       "Tennis balls are covered in a fibrous felt which "
                                       "modifies their aerodynamic properties, and each has a "
                                       "white curvilinear oval covering it", catalog=catalog3)
session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Tennis Racket",
                           description="A racket or racquet is a sports implement consisting of a "
                                       "handled frame with an open hoop across which a network of"
                                       " strings or catgut is stretched tightly. It is used for striking "
                                       "a ball or shuttlecock in games such as squash, tennis, racquetball, "
                                       "and badminton. ... Wood is still used for real tennis, rackets,"
                                       " and xare", catalog=catalog3)
session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Tennis Net",
                           description="If a doubles net is used, then the net shall be supported,"
                                       " at a height of 3 ½ feet (1.07 m), "
                                       "by two singles sticks, the centres of which shall be 3 feet (0.914 m) "
                                       "outside the singles court on each side. "
                                       "The net posts shall not be more than 6 inches (15 cm) "
                                       "square or 6 inches (15 cm) n diameter.", catalog=catalog3)
session.add(catalog_item)
session.commit()

# Catalog Batmenton
catalog4 = Catalog(name="Badminton")

session.add(catalog4)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Badminton Shuttle",
                           description="A shuttlecock (often abbreviated to shuttle; also called a birdie)"
                                       " is a high-drag projectile, with an open conical shape: the cone is "
                                       "formed from sixteen overlapping feathers embedded into a rounded cork base. "
                                       "The cork is covered with thin leather or synthetic material.", catalog=catalog4)
session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Badminton Racket",
                           description="A racket or racquet is a sports implement consisting of a "
                                       "handled frame with an open hoop across which a network of"
                                       " strings or catgut is stretched tightly. It is used for striking "
                                       "a ball or shuttlecock in games such as squash, tennis, racquetball, "
                                       "and badminton. ... Wood is still used for real tennis, rackets,"
                                       " and xare", catalog=catalog4)
session.add(catalog_item)
session.commit()

catalog_item = CatalogItem(user_id=1, name="Badminton Net",
                           description="If a doubles net is used, then the net shall be supported,"
                                       " at a height of 3 ½ feet (1.07 m), "
                                       "by two singles sticks, the centres of which shall be 3 feet (0.914 m) "
                                       "outside the singles court on each side. "
                                       "The net posts shall not be more than 6 inches (15 cm) "
                                       "square or 6 inches (15 cm) n diameter.", catalog=catalog4)
session.add(catalog_item)
session.commit()

print("Records Inserted")
