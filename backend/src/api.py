import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


# manager jwt token
# eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imp6dkJsM20wN19SVVFSZTdTcElBYiJ9.eyJpc3MiOiJodHRwczovL2Rldi1wZTkzdGxyby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE4YjZmMDE5M2Q1NDAwMDY5YmZiYzRiIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNjM2NzE4MDY1LCJleHAiOjE2MzY3MjUyNjUsImF6cCI6IkFQbjh0bWZxcFh3N0ZCVkl4ajhHTmlqaHYwdmd2WDROIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.hNnCyHkIb1cXIKkjjR5MA44a7gi8vyjB4p2WuQlcuVY0veAKUxbt2_JSXFt1ZacjdP_csLdJRlo55-ETa-ZgAxkIbovrhERB5nfr1Dxy2Zx02xMeZzrHFCRCL6Nk_wma_XP2hi4srd-6X6LL1Mgamx64vthxhubshPdS3Jzi9rX2eV3pqSsvHywSk42R3PWvHUNDs3X2S-vwIQpmfCCQ4RlBYUP03Qkiht_F_eB-FiSKRUOrAeM7q7UGaX4MCzxszNrK7hAlQLkuYu10lueHf0QMLtsnb2a2TaGj8smhRQvQCnLF0AMT9YwPe2SZYFKNxUxEfnh3WnzNxB5edtJjJw
'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
@requires_auth('get:drinks')
def drinks(payload): # need to pass payload
    try:
        # get all drinks
        # I have a question here if I use the code below it will automatically delete the drink I create.
        # if I use order by all drink, I get 400 error I don't know why
        # drink_list = Drink.query.order_by.all()
        drink_list = Drink.query.all()
        # use short representation as required
        drinks = [ drink.short() for drink in drink_list ]
        
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except:

        abort(400)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(payload): # need to pass payload
    try:
        # get all drinks
        drink_list = Drink.query.order_by(Drink.id).all()
        # use long representation as required
        drinks = [ drink.long() for drink in drink_list ]
        
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except:

        abort(400)
'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
# guidance from API Development and Documentation lesson 3 endpoints and payloads
# learn from teacher's video, and read the auth.py and models.py doc
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def new_drinks(payload): # need to pass payload
    try:
        new_drink = request.get_json()
        # get title and recipe from new drink
        new_title = new_drink.get('title')
        new_recipe = new_drink.get('recipe')

        # if 'recipe' and 'title' in new_drink:
        if 'recipe' and 'title' in new_drink:
        # create new drink object, convert recipe json object to string 
            drink = Drink(title = new_title, recipe = json.dumps(new_recipe))
        
        # insert a new drink
        drink.insert()
         # use long representation as required
        d = [drink.long()]
        # return status code and json information
        return jsonify({
            'success': True,
            'drinks': d
        }), 200


    except:
        
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(payload,id): # need to pass payload and id to identify the drink to update
    try:
        drink_toUpdate = request.get_json()
        # find the drink with id and then delete
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        drink_title = drink_toUpdate.get('title')
        drink_recipe = drink_toUpdate.get('recipe')
        # if there are title and recipe in drinktoUpdate, convert recipe object to string
        if 'recipe' and 'title' in drink_toUpdate:
            drink.title = drink_title
            drink.recipe = json.dumps(drink_recipe)

        drink.update()
        # use long representation as required
        d = [drink.long()]
        # return status code and json information
        return jsonify({
            'success': True,
            'drinks': d,
            'updated_title': drink_title
        }), 200
    except:
        # couldnot find that drink
        abort(404)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload,id): # need to pass payload and id to identify the drink to delete
    try:
        drink_toDelete = request.get_json()
        # find the drink with id and then delete
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        drink.delete()
        # return status code and json information
        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except:
        # couldnot find that drink

        abort(404)

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def handle_not_found_error(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def handle_auth_error(e):
    return jsonify({
        "success": False,
        "error": e.status_code,
        "message": e.error['description']
    }), e.status_code

# We need more error handler for this app like 400, 401, 403
@app.errorhandler(400)
def handle_validation_error(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Invalid"
    }), 400

@app.errorhandler(401)
def handle_unauthorized_error(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@app.errorhandler(403)
def handle_permission_error(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "No pemission"
    }), 403