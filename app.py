# import the Flask class from the flask module
from flask import Flask, render_template, request, json, redirect, url_for
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash,check_password_hash
from flask import session

#from flask_mysqldb import MySQL



# create the application object or defining my app
app = Flask(__name__)
app.secret_key = '1pe14is087'
mysql = MySQL()


#MySQL configs
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '81473@Arbz'
app.config['MYSQL_DATABASE_DB'] = 'db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



# use decorators to link the function to a url
@app.route("/")
def main():
	return render_template('index.html')

@app.route('/showSignUp')
def showsignup():
	return render_template('signup.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
	#reading posted values from ui
	try:
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		_guardianname = request.form['inputGuardian']
		_guardiannumber = request.form['inputGuardianno']
		_doctorname = request.form['doctorname']
		_doctorno = request.form['doctorno']

		if _name and _email and _password and _guardianname and _guardiannumber and _doctorname and _doctorno:
		#if _name and _email and _password:
			#return json.dumps({'html':'<span>All fields are good !</span>'})
			# else:
			# 	return json.dumps({'html':'<span>Enter the required fields</span>'})	

			#crerating mysql connection
			conn = mysql.connect()
			cursor = conn.cursor()
			####cur = mysql.connection.cursor()

			#use salting module from werkzeug, create hashed password
			_hashed_password = generate_password_hash(_password)

			#call stored proc from mysql
			cursor.callproc('sp_createUser',(_name,_email,_hashed_password,_guardianname,_guardiannumber,_doctorname,_doctorno))

			#if proc is successfl,commit changes and return success mesg
			data = cursor.fetchall()
				
			if len(data) is 0:
			    conn.commit()
			    return json.dumps({'message':'User created successfully !'})
			else:
			    return json.dumps({'error':str(data[0])})
			    #return json.dumps({'message':'mushtaq failed !'})
		else:
			return json.dumps({'html':'<span>Enter reuquired fields</span>'})	    
	
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close()
		conn.close()









@app.route('/showSignin')
def showSignin():
	return render_template('signin.html')


@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        
        #connect to mysql
        con = mysql.connect()
        cursor = con.cursor()
        ###cur = mysql.connection.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()

        if len(data) > 0:  #true
            if check_password_hash(str(data[0][3]),_password)==0: ##i have tweeked this one not working
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email 00000address or Password.')
            

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/userHome')
def userHome():
	if session.get('user'):
		return render_template('userHome.html')
	else:
		return render_template('error.html',error='UNauthorized access')	

@app.route('/logout')
def logout():
	session.pop('user',None)  #am making the session variable "user" as null
	return redirect('/')



# start the server with the 'run()' method
if __name__ == '__main__':
   app.run(debug=True)









