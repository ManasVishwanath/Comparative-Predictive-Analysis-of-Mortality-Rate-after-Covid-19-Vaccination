from flask import Flask, render_template, redirect, url_for, request,session, flash
from flask import jsonify
import numpy as np
import flask
import pickle
from jinja2 import Template



#Lodding the model
forest = pickle.load(open('code.pkl', 'rb'))


#data base connection 
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost", user="root", password="password", database="ml08db")
# =============================================================================
# if mydb.is_connected():
#     print("Database connection established successfully.")
# else:
#     print("Failed to connect to database.")
# =============================================================================
#print(mydb)

mycursor = mydb.cursor()


app = Flask(__name__)
app.secret_key = 'your secret key'

@app.route('/')
def main():
    return render_template('main.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/aregister', methods=['GET', 'POST'])
def aregister():
    msg = ''
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']

        cursor = mydb.cursor()
        val = (username, email, phone, password)
        cursor.execute('INSERT INTO student values(0,%s,%s,%s,%s)', val)
        mydb.commit()
        msg = 'You have successfully registered !'
        return render_template('login.html', msg=msg)
    else:
        msg = 'Please fill out the form !'
        return render_template('register.html', msg=msg)
 

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    return redirect(url_for('login'))    

    
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/alogin', methods=['POST'])
def alogin():
    # Get the user's login data from the form
    email = request.form['email']
    password = request.form['password']
    
    # Check the user's data against the data in the database
    cursor = mydb.cursor()
    sql = "SELECT * FROM student WHERE email = %s AND password = %s"
    values = (email, password)
    cursor.execute(sql, values)
    user = cursor.fetchone()
    
    if user:
        testEmail = user[2]
        testPwd = user[4]
        msg = ""
        return render_template('prediction.html', msg=msg, testEmail=testEmail , testPwd=testPwd)
    else:
       msg = "No User/ go for Registration"
       return render_template('login.html', msg=msg)


@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/lgout')
def lgout():
    return render_template('main.html')




@app.route('/predict', methods=['GET','POST'] ) 
def predict():
    if request.method == 'POST':
        
        Cases= float(request.form['Cases'])
        Deaths = float(request.form['Deaths'])
        Total_Vaccinations = float(request.form['Total_Vaccinations'])
        Vaccinated = float(request.form['Vaccinated'])
        Fully_Vaccinated = float(request.form['Fully_Vaccinated'])   
        data = np.array([[Cases, Deaths,Total_Vaccinations,Vaccinated,Fully_Vaccinated]])
        # data = np.array([temp_array])
        my_prediction = forest.predict(data)
        print("my_prediction:", my_prediction)
        
        if my_prediction == 0:
            result = "5%"
        elif my_prediction == 1:
            result = "10%"
        elif my_prediction == 2:
            result = "20%"
        elif my_prediction == 3:
            result = "30%"
        elif my_prediction == 4:
            result = "40%"
        elif my_prediction == 5:
            result = "50%"
        elif my_prediction == 6:
            result = "60%"
        elif my_prediction == 7:
            result = "70%"
        elif my_prediction == 8:
            result = "80%"
        elif my_prediction == 9:
            result = "90%"
            
        else:
            res = "No Data "
       
        return render_template('prediction.html', result = result)



@app.route('/performance')
def performance():
    return render_template('performance.html')

if __name__ == '__main__':
    app.run()