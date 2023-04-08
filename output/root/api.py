from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import psycopg2
from scraper import scrape_forex_prices

app = Flask(__name__)
api = Api(app)

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Set up database connection
connection = psycopg2.connect(user="user",
                              password="password",
                              host="127.0.0.1",
                              port="5432",
                              database="forex_db")
cursor = connection.cursor()

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

class Login(Resource):
    def get(self):
        if current_user.is_authenticated:
            return {'status': 'success', 'message': 'User is already logged in'}

        return {'status': 'fail', 'message': 'User is not logged in'}

    def post(self):
        data = request.get_json()

        if data['username'] != 'admin' or data['password'] != 'password':
            return {'status': 'fail', 'message': 'Incorrect username or password'}

        user = User(id=data['username'])
        login_user(user)

        return {'status': 'success', 'message': 'User successfully logged in'}

class Logout(Resource):
    @login_required
    def post(self):
        logout_user()
        return {'status': 'success', 'message': 'User successfully logged out'}

class Forex(Resource):
    @login_required
    def get(self):
        cursor.execute("SELECT * FROM forex_prices")
        data = cursor.fetchall()

        results = []

        for row in data:
            result = {'date': row[0], 'currency': row[1], 'bid': row[2], 'ask': row[3]}
            results.append(result)

        return jsonify(results)

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('date', required=True, help='Date cannot be blank')
        parser.add_argument('currency', required=True, help='Currency cannot be blank')
        parser.add_argument('bid', required=True, help='Bid cannot be blank')
        parser.add_argument('ask', required=True, help='Ask cannot be blank')
        data = parser.parse_args()

        try:
            cursor.execute("INSERT INTO forex_prices (date, currency, bid, ask) VALUES (%s, %s, %s, %s)",
                           (data['date'], data['currency'], data['bid'], data['ask']))
            connection.commit()
            return {'status': 'success', 'message': 'Forex data added successfully'}
        except Exception as e:
            connection.rollback()
            return {'status': 'fail', 'message': 'Error adding forex data: {}'.format(str(e))}

class Prediction(Resource):
    @login_required
    def get(self):
        return {'status': 'success', 'message': 'Predicted forex prices will be added soon'}

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Forex, '/forex')
api.add_resource(Prediction, '/prediction') 

if __name__ == '__main__':
    app.run() 

##JOB_COMPLETE##