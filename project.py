import json
import random
import string
import os

import httplib2
import requests
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask import make_response
from flask import session as login_session
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets

from catalog_data_access import (get_catalogs,
                                 get_catolog_by_name,
                                 get_latest_items,
                                 get_catalog_item_by_name,
                                 get_items_by_catalog,
                                 persist_catalog_items,
                                 delete_catalog_item,
                                 verify_credentials,
                                 createUser,
                                 getUserID)
from database_setup import CatalogItem
from functools import wraps

app = Flask(__name__)

app_path = os.path.dirname(os.path.realpath(__file__))

CLIENT_ID = json.loads(
    open(app_path + '/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"


# user registration functionality
@app.route('/registration', methods=['GET', 'POST'])
def showRegistration():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        email = request.form['email']

        login_session['username'] = user_name
        login_session['email'] = email
        login_session['picture'] = None
        print(login_session['email'])

        user_id = createUser(login_session, password)
        print(user_id)
        if user_id:
            login_session['user_id'] = user_id
            print(user_id)
            return redirect('/')
        else:
            del login_session['username']
            del login_session['email']


# user login functionality
@app.route('/login', methods=['GET', 'POST'])
def showLogin():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        print(user_name + " " + password)
        user = verify_credentials(user_name, password)
        if user:
            login_session['username'] = user.name
            login_session['picture'] = user.picture
            login_session['email'] = user.email
            login_session['user_id'] = user.id
            return redirect(url_for('show_latest_items'))
        else:
            error = 'Invalid Credentials. Please try again.'
            return render_template('loginRegistration.html', error=error)
    else:
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in range(32))
        login_session['state'] = state
        # return "The current session state is %s" % login_session['state']
        return render_template('loginRegistration.html', STATE=state)


# Google OAuth connect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    msg = str(code).replace("b'", "")
    msg = msg.replace("'", "")
    code = msg
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(app_path + '/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError as e:
        print(e)
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    # login_session['credentials'] = credentials
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # flash("you are now logged in as %s" % login_session['username'])
    return "success"


# Facebook OAuth connect
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    msg = str(access_token).replace("b'", "")
    msg = msg.replace("'", "")
    access_token = msg
    print("access token received %s " % access_token)

    app_id = json.loads(open(app_path + '/fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open(app_path + '/fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    result = str(result)
    token = result.split(',')[0].split(':')[1].replace('"', '')
    # print(token)
    # msg = str(token).replace("b'", "")
    # msg = msg.replace("'", "")
    # token = msg


    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result.decode('utf-8'))
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result.decode('utf-8'))

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # flash("Now logged in as %s" % login_session['username'])
    return "success"


# logout functionality
@app.route('/logout')
def showLogout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        return redirect(url_for('show_latest_items'))
    else:
        if login_session['username']:
            del login_session['username']
        if login_session['email']:
            del login_session['email']
        if login_session['picture']:
            del login_session['picture']
        if login_session['user_id']:
            del login_session['user_id']
        return redirect(url_for('show_latest_items'))


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session['access_token']
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# functionality to display categories and latest items
@app.route('/')
@app.route('/catalog')
def show_latest_items():
    catalogs = get_catalogs()
    items = get_latest_items()
    return render_template("catalogs.html", catalogs=catalogs, items=items)


# functionality to display categories and there respective items
@app.route('/catalog/<string:catalog_name>/items')
def show_catalog_items(catalog_name):
    catalogs = get_catalogs()
    catalog = get_catolog_by_name(catalog_name)
    items = get_items_by_catalog(catalog.id)
    return render_template("catalogItems.html", catalog=catalog_name,
                           catalogs=catalogs, items=items)


# functionality to display categories item description
@app.route('/catalog/<string:catalog_name>/<string:item_name>')
def show_catalog_item_description(catalog_name, item_name):
    catalog_item = get_catalog_item_by_name(item_name)
    return render_template("itemDescription.html", item=catalog_item)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwrags):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwrags)

    return decorated_function


# functionality to create an item of given category
@app.route('/catalog/new/', methods=['GET', 'POST'])
@login_required
def newItem():
    if request.method == 'POST':
        itemName = request.form['name']
        itemDescription = request.form['description']
        catalog_name = request.form['catalog']
        catalog = get_catolog_by_name(catalog_name)
        catalog_item = CatalogItem(user_id=1, name=itemName,
                                   description=itemDescription, catalog=catalog)

        persist_catalog_items(catalog_item)
        return redirect(url_for('show_latest_items'))
    else:
        catalogs = get_catalogs()
        return render_template('newItem.html', catalogs=catalogs)


# functionality to edit item
@app.route('/catalog/<string:item_name>/edit/', methods=['GET', 'POST'])
@login_required
def editItem(item_name):
    item = get_catalog_item_by_name(item_name)
    if item.user_id != login_session['user_id']:
        return redirect(url_for('show_latest_items'))
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        catalog_name = request.form['catalog']
        item.catalog = get_catolog_by_name(catalog_name)
        persist_catalog_items(item)
        return redirect(url_for('show_latest_items'))
    else:
        catalogs = get_catalogs()
        return render_template('editItem.html', item=item, catalogs=catalogs)


# functionality to delete item
@app.route('/catalog/<string:item_name>/delete/', methods=['GET', 'POST'])
@login_required
def deleteItem(item_name):
    item = get_catalog_item_by_name(item_name)
    if item.user_id != login_session['user_id']:
        return redirect(url_for('show_latest_items'))
    if request.method == 'POST':
        delete_catalog_item(item)
        return redirect(url_for('show_latest_items'))
    else:
        return render_template('deleteItem.html', item=item)


# functionality to display json data of all the information
@app.route('/catalog.json')
def show_all_catalog_items_json():
    catalogs = get_catalogs()
    catalog_serialize = [c.serialize for c in catalogs]
    for catalog in catalog_serialize:
        items = [i.serialize for i in get_items_by_catalog(catalog["id"])]
        if items:
            catalog["Item"] = items
    return jsonify(Catalogs=catalog_serialize)


# functionality to display json data of given category
@app.route('/catalog/<string:catalog_name>/items/json')
def show_catalog_items_json(catalog_name):
    catalog = get_catolog_by_name(catalog_name)
    items = get_items_by_catalog(catalog.id)
    return jsonify(CatalogItems=[i.serialize for i in items])


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'DEV_SECRET_KEY'
    app.run(host='localhost', port=5000)
