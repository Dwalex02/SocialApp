from flask import Flask
from flask_restx import Api, reqparse, Resource
from Encoder import JsonEncoder
import sqlite3
import uuid
from datetime import date


social_app = Flask(__name__)
social_app.json_encoder = JsonEncoder
social_api = Api(social_app)


registration_parser = reqparse.RequestParser()
registration_parser.add_argument('username', type=str, required=True)
registration_parser.add_argument('year of birth', type=int, required=True, help='There is age restriction')
registration_parser.add_argument('month of birth', type=int, required=True, help='As a number')
registration_parser.add_argument('day of birth', type=int, required=True)
registration_parser.add_argument('password', type=str, required=True)
registration_parser.add_argument('email', type=str, required=True)
registration_parser.add_argument('gender', type=str, required=False, help='M/F/""')

changePassword_parser = reqparse.RequestParser()
changePassword_parser.add_argument('id', type=str, required=True)
changePassword_parser.add_argument('new password', type=str, required=True)
changePassword_parser.add_argument('repeat new password', type=str, required=True)



@social_api.route('/user')
class Registration(Resource):
    @social_api.doc(parser=registration_parser)
    def post(self):
        args = registration_parser.parse_args()
        id = str(uuid.uuid4())
        username = args['username']
        yob = args['year of birth']
        mob = args['month of birth']
        dob = args['day of birth']
        password = args['password']
        email = args['email']
        gender = args['gender']
        today = date.today()
        age = int(today.year) - yob - ((today.month, today.day) < (mob, dob))
        if age >= 18:
            adult = True
        else:
            adult = False
        if adult == True:
            conn = sqlite3.connect('social.db')
            cursorObj = conn.cursor()
            cursorObj.execute (
                "INSERT INTO social (id, username, yearOfBirth, monthOfBirth, DayOfBirth, password, email, gender) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",\
            [id, username, yob, mob, dob, password, email, gender,]
            )
            conn.commit()
            print("You have successfully registered.")
            return("You have successfully registered.")
        else:
            print("Access denied. You must be 18+")
            return("Access denied. You must be 18+")


@social_api.route('/user/<id>')
class GetTheAccount(Resource):
    def get(self, id):
        conn = sqlite3.connect('social.db')
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT * FROM social WHERE id = ?', (id,))
        all_rows=cursorObj.fetchall()
        return all_rows
    def delete(self, id):
        conn = sqlite3.connect('social.db')
        cursorObj = conn.cursor()
        cursorObj.execute('DELETE FROM social WHERE id = ?', (id,))
        conn.commit()
        print("The account was deleted successfully.")
        return ("The account was deleted successfully.")

@social_api.route('/user/change_password')
class ChangePassword(Resource):
    @social_api.doc(parser=changePassword_parser)
    def put(self):
        args = changePassword_parser.parse_args()
        id2 = args['id']
        np= args['new password']
        rnp= args['repeat new password']
        if np == rnp:
            conn = sqlite3.connect('social.db')
            cursorObj = conn.cursor()
            cursorObj.execute('UPDATE social SET password=? WHERE id=?', (np,id2,))
            conn.commit()
            print("The password is successfully changed.")
            return("The password is successfully changed.")
        else:
            print("The password does not match. Try again")
            return("The password does not match. Try again")

@social_api.route('/user/stats')
class userStats(Resource):
    def get(self):
        conn = sqlite3.connect('social.db')
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT count(*) FROM social')
        result=cursorObj.fetchone()
        return result

@social_api.route('/user/gstats')
class userGenStats(Resource):
    def get(self):
        conn = sqlite3.connect('social.db')
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT count(*) FROM social WHERE gender = "M"')
        result=cursorObj.fetchone()
        conn2 = sqlite3.connect('social.db')
        cursorObj2 = conn2.cursor()
        cursorObj2.execute('SELECT count(*) FROM social WHERE gender = "F"')
        result2 = cursorObj2.fetchone()
        conn3 = sqlite3.connect('social.db')
        cursorObj3 = conn3.cursor()
        cursorObj3.execute('SELECT count(*) FROM social WHERE gender IS NULL')
        result3 = cursorObj3.fetchone()
        my_str = f"Males:{result[0]}, Females:{result2[0]}, Unspecified:{result3[0]}"
        print(my_str)
        return my_str

@social_api.route('/user/<username>/finder')
class Finder(Resource):
    def get(self, username):
        conn = sqlite3.connect('social.db')
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT username FROM social WHERE username=?',(username,))
        result = cursorObj.fetchone()
        if result:
            print(f"The username {username} is already taken.")
            return f"The username {username} is already taken."
        else:
            print(f"The username {username} is not taken")
            return f"The username {username} is not taken"

@social_api.route('/user/<username>/<password>/matcher')
class Matcher(Resource):
    def get(self, username, password):
        conn = sqlite3.connect('social.db')
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT username FROM social WHERE username=? AND password=?',(username, password,))
        result = cursorObj.fetchone()
        if result:
            print("There is a match.")
            return "There is a match."
        else:
            print("There isn't match.")
            return "There isn't match."




if __name__ == '__main__':
    social_app.run(debug = False, port = 7890)