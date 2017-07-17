from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Catalog, CatalogItem, User

engine = create_engine('sqlite:///itemsCatalog.db', echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def verify_credentials(user_name, password):
    return True


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def get_catalogs():
    categories = session.query(Catalog)
    return categories


def get_catolog_by_name(catalog_name):
    category = session.query(Catalog).filter_by(name=catalog_name).one()
    return category


def get_latest_items():
    items = session.query(CatalogItem).order_by(CatalogItem.created_date.desc()).limit(10).all()
    return items


def get_catalog_item_by_name(item_name):
    item = session.query(CatalogItem).filter_by(name=item_name).one()
    return item


def get_items_by_catalog(catalog_id):
    items = session.query(CatalogItem).filter_by(catalog_id=catalog_id).all()
    return items


def persist_catalog_items(catalog_item):
    session.add(catalog_item)
    session.commit()


def delete_catalog_item(catalog_item):
    session.delete(catalog_item)
    session.commit()
