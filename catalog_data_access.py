from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Catalog, CatalogItem, User

engine = create_engine('sqlite:///itemsCatalog.db', echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def verify_credentials(user_name, password):
    users = session.query(User)
    for user in users:
        if user.name == user_name and user.password == password:
            return user
    return None


def createUser(login_session, password=None):
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'], password=password)
    try:
        session.add(newUser)
        session.commit()
        user = session.query(User).filter_by(email=login_session['email']).one()
        return user.id
    except Exception as e:
        return None


def getUserInfo(user_id):
    try:
        user = session.query(User).filter_by(id=user_id).one()
        return user
    except Exception as e:
        return None


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as e:
        return None


def get_catalogs():
    try:
        categories = session.query(Catalog)
        return categories
    except Exception as e:
        return None


def get_catolog_by_name(catalog_name):
    try:
        category = session.query(Catalog).filter_by(name=catalog_name).one()
        return category
    except Exception as e:
        return None


def get_latest_items():
    try:
        items = session.query(CatalogItem).order_by(CatalogItem.created_date.desc()).limit(10).all()
        return items
    except Exception as e:
        return None


def get_catalog_item_by_name(item_name):
    try:
        item = session.query(CatalogItem).filter_by(name=item_name).one()
        return item
    except Exception as e:
        return None


def get_items_by_catalog(catalog_id):
    try:
        items = session.query(CatalogItem).filter_by(catalog_id=catalog_id).all()
        return items
    except Exception as e:
        return None


def persist_catalog_items(catalog_item):
    try:
        session.add(catalog_item)
        session.commit()
    except Exception as e:
        return None


def delete_catalog_item(catalog_item):
    try:
        session.delete(catalog_item)
        session.commit()
    except Exception as e:
        return None
