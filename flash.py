'''from flask import Flask, render_template,request, url_for, redirect, session, flash, jsonify
import bcrypt
from datetime import timedelta
import sql_db


def encrpt(password):
   passwd = password.encode()
   salt = bcrypt.gensalt()
   hashed = bcrypt.hashpw(passwd, salt)
   return hashed
   

app = Flask(__name__)
app.secret_key = 'random string'
app.permanent_session_lifetime = timedelta(hours = 5) #save section for x mins/hours

#index_page

@app.route('/')
@app.route('/home')
def index():
   return render_template('index.html')

@app.route("/check_otp", methods = ['GET', 'POST'])
def check_otp():
   if request.method == 'POST':
      code = int(request.form['otp'])
      if EMAIL is not None:         
         if VARIFICATION_CODE==code:
            response = sql_db.enter_to_db2(EMAIL, PASSWORD, AGE)
            if response[0]:
               session["email"] = EMAIL
               flash(response[1])
               return redirect(url_for("index"))
            else:
               flash(response[1])
               return redirect(url_for('register'))
         else:
            flash("invalid OTP")
            return redirect(url_for('register'))

#register_page

@app.route("/register", methods = ['GET', 'POST'])
def register():
   #error = None
   
   if request.method == 'POST':
      #session.permanent = True
      email = request.form['email']
      password = encrpt(request.form['password'])
      age = request.form['age']
      msg = sql_db.enter_to_db(email, password, age)
      if msg[0]:
         #flash(msg[1])
         global VARIFICATION_CODE
         VARIFICATION_CODE = msg[3]
         #EMAIL, PASSWORD, AGE = email, password, age
         return redirect(url_for('register'))
      else:
         flash(msg[1])
         if msg[2]:
            return redirect(url_for('login'))
         else:
            return render_template("register.html")
      #return render_template('login.html', error = error)
   else:
      if "email" in session:
         flash("You have been already logged in!")
         return redirect(url_for("index"))
      else:
         return render_template("register2.html")
   
#login_page

@app.route('/login', methods = ['GET', 'POST'])
def login():
   error = None
   
   if request.method == 'POST':
      session.permanent = True
      email = request.form['email']
      password = request.form['password'] #generate_password_hash(request.form['password'])
      msg = sql_db.check_if_exist(email, password)
      if msg[0]:         
         session["email"] = email
         flash(msg[1])
         return redirect(url_for('index'))
      else:
         error = msg[1]
         return render_template('login2.html', error = error)
      flash('You were successfully logged in')
      return redirect(url_for('index'))
		#return render_template('login.html', error = error)
   else:
      if "email" in session:
         flash("You have been already logged in!")
         return redirect(url_for("index"))
      else:
         return render_template("login2.html")

#logout

@app.route("/logout")
def logout():
   if "email" in session:
      flash("You have been logged out!!", "info")
      session.pop("email", None)
   else:
      flash("You have not logged in!!", "info")
   return redirect(url_for("login"))

#team_page

@app.route("/team")
def team():
   return render_template('team.html')

#profile_page
@app.route("/profile")
def profile():
   if "email" in session:
      return render_template('profile.html')
   else:
      flash("You have not logged in!!", "info")
   return redirect(url_for("login"))

#seeking_for_details
@app.route("/give_details", methods=['GET'])
def give_details():
   if "email" in session:
      email = session["email"]
      response = jsonify(sql_db.give_details(email))

      response.headers.add('Access-Control-Allow-Origin', '*')

      return response
   else:
      response = jsonify(None)
      return response

#updating_the_profile
@app.route("/update_details", methods=['GET', 'POST'])
def update_details():
   if "email" in session:
      name = request.form['name']
      dp = request.form['profile']
      email = session['email']
      saved = sql_db.update_profile(name, email, dp)
      if saved:
         flash("Profile Updated")
         return redirect(url_for('index'))
      else:
         flash("unfortunately Profile not updated")
         return redirect(url_for('index'))
   else:
      response = jsonify({"error": "didn't login"})
      response.headers.add('Access-Control-Allow-Origin', '*')
      return response

@app.route("/post")
def post():
   return render_template("posts.html")

#adding_ post
@app.route("/add_post", methods=['GET', 'POST'])
def add_post():
   if "email" in session:   
      post = request.form['profile']
      email = session['email']
      saved = sql_db.add_post(email, post)
      if saved:
         return jsonify(True)
      else:
         return jsonify(False)
   else:
      return jsonify(False)

#seeking_for_details
@app.route("/get_post", methods=['GET', 'POST'])
def get_post():
   p_id = int(float(request.form['p_idx']))
   response = jsonify(sql_db.get_post(p_id))
   response.headers.add('Access-Control-Allow-Origin', '*')
   return response



if __name__ == "__main__":
   sql_db.create_db()
   print("hai")
   app.run(debug = True)
   print(VARIFICATION_CODE==3)'''



from flask import Flask, render_template,request, url_for, redirect, session, flash, jsonify
import bcrypt
from datetime import timedelta
import sql_db

VARIFICATION_CODE = 1

def encrpt(password):
   passwd = password.encode()
   salt = bcrypt.gensalt()
   hashed = bcrypt.hashpw(passwd, salt)
   return hashed
   

app = Flask(__name__)
app.secret_key = 'random string'
app.permanent_session_lifetime = timedelta(hours = 5) #save section for x mins/hours

#index_page

@app.route('/')
@app.route('/home')
def index():
   return render_template('index.html')

@app.route("/check_otp", methods = ['GET', 'POST'])
def check_otp():
   if request.method == 'POST':
      email = request.form['email']
      password = encrpt(request.form['password'])
      age = request.form['age']
      code = int(request.form['otp'])      
      if VARIFICATION_CODE==code:
         response = sql_db.enter_to_db(email, password, age)
         if response[0]:
            session["email"] = email
            flash(response[1])
            response = jsonify({
               "status": True,
               "redirect": True,
               "msg":"Registered Successfully"
               })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
         else:
            response = jsonify({
               "status": False,
               "redirect": False,
               "msg":response[1]
               })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
      else:
         response = jsonify({
            "status": False,
            "redirect": False,
            "msg": "Wrong OTP entered"
            })
         response.headers.add('Access-Control-Allow-Origin', '*')
         return response

#register_page

@app.route("/register", methods = ['GET', 'POST'])
def register():   
   if request.method == 'POST':
      #session.permanent = True
      email = request.form['email']
      password = encrpt(request.form['password'])
      age = request.form['age']
      msg = sql_db.check_from_db(email, password, age)
      if msg[0]:
         global VARIFICATION_CODE
         VARIFICATION_CODE = msg[3]
         print(VARIFICATION_CODE)
         response = jsonify({
            "status": True,
            "redirect": False,
            "msg":"Enter the VARIFICATION CODE"
            })
         response.headers.add('Access-Control-Allow-Origin', '*')
         return response
      else:
         if msg[2]:
            flash(msg[1])
            response = jsonify({
            "status": False,
            "redirect": True,
            "msg":"EMAIL already registered"
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
         else:
            response = jsonify({
            "status": False,
            "redirect": False,
            "msg": msg[1]
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
      #return render_template('login.html', error = error)
   else:
      if "email" in session:
         flash("You have been already logged in!")
         return redirect(url_for("index"))
      else:
         return render_template("register2.html")
   
#login_page

@app.route('/login', methods = ['GET', 'POST'])
def login():
   error = None
   
   if request.method == 'POST':
      session.permanent = True
      email = request.form['email']
      password = request.form['password'] #generate_password_hash(request.form['password'])
      msg = sql_db.check_if_exist(email, password)
      if msg[0]:         
         session["email"] = email
         flash(msg[1])
         return redirect(url_for('index'))
      else:
         error = msg[1]
         return render_template('login2.html', error = error)
      flash('You were successfully logged in')
      return redirect(url_for('index'))
      #return render_template('login.html', error = error)
   else:
      if "email" in session:
         flash("You have been already logged in!")
         return redirect(url_for("index"))
      else:
         return render_template("login2.html")

#logout

@app.route("/logout")
def logout():
   if "email" in session:
      flash("You have been logged out!!", "info")
      session.pop("email", None)
   else:
      flash("You have not logged in!!", "info")
   return redirect(url_for("login"))

#team_page

@app.route("/team")
def team():
   return render_template('team.html')

#profile_page
@app.route("/profile")
def profile():
   if "email" in session:
      return render_template('profile.html')
   else:
      flash("You have not logged in!!", "info")
      session['back'] = "profile"
   return redirect(url_for("login"))

#seeking_for_details
@app.route("/give_details", methods=['GET'])
def give_details():
   if "email" in session:
      email = session["email"]
      response = jsonify(sql_db.give_details(email))

      response.headers.add('Access-Control-Allow-Origin', '*')

      return response
   else:
      response = jsonify(None)
      return response

#updating_the_profile
@app.route("/update_details", methods=['GET', 'POST'])
def update_details():
   if "email" in session:
      name = request.form['name']
      dp = request.form['profile']
      email = session['email']
      saved = sql_db.update_profile(name, email, dp)
      if saved:
         flash("Profile Updated")
         return redirect(url_for('index'))
      else:
         flash("unfortunately Profile not updated")
         return redirect(url_for('index'))
   else:
      response = jsonify({"error": "didn't login"})
      response.headers.add('Access-Control-Allow-Origin', '*')
      return response

@app.route("/post")
def post():
   if "email" in session:
      return render_template("posts.html")
   else:
      flash("You have not logged in!!", "info")
      session['back'] = "post"
      return redirect(url_for("login"))


#adding_ post
@app.route("/add_post", methods=['GET', 'POST'])
def add_post():
   if "email" in session:   
      post = request.form['profile']
      email = session['email']
      saved = sql_db.add_post(email, post)
      if saved:
         return jsonify(True)
      else:
         return jsonify(False)
   else:
      return jsonify(False)

#seeking_for_details
@app.route("/get_post", methods=['GET', 'POST'])
def get_post():
   p_id = int(float(request.form['p_idx']))
   response = jsonify(sql_db.get_post(p_id))
   response.headers.add('Access-Control-Allow-Origin', '*')
   return response



if __name__ == "__main__":
   sql_db.create_db()
   print("hai")
   app.run(debug = True)
   print(VARIFICATION_CODE)