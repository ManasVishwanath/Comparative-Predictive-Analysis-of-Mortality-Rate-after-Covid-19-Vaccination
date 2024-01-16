from flask import Flask, render_template, redirect, url_for, request
from flask import jsonify
import pickle
import numpy as np


#forest = pickle.load(open('code.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')













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


if __name__ == '__main__':
    app.run()
