from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('rfr_model.pkl', 'rb'))
@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        Year = int(request.form['Year'])
        years_old = 2020 - Year

        km_driven = int(request.form['Kmdriven'])

        Fuel = request.form['Fuel']

        if (Fuel == 'Fuel_GNC'):
            fuel_CNG = 1
            fuel_Diesel = 0
            fuel_Electric = 0
            fuel_LPG = 0
            fuel_Petrol = 0
        elif (Fuel == 'Fuel_Diesel'):
            fuel_CNG = 0
            fuel_Diesel = 1
            fuel_Electric = 0
            fuel_LPG = 0
            fuel_Petrol = 0
        elif (Fuel == 'Fuel_Elecric'):
            fuel_CNG = 0
            fuel_Diesel = 0
            fuel_Electric = 1
            fuel_LPG = 0
            fuel_Petrol = 0
        elif (Fuel == 'Fuel_LPG'):
            fuel_CNG = 0
            fuel_Diesel = 0
            fuel_Electric = 0
            fuel_LPG = 1
            fuel_Petrol = 0
        else:
            fuel_CNG = 0
            fuel_Diesel = 0
            fuel_Electric = 0
            fuel_LPG = 0
            fuel_Petrol = 1
        
        Seller = request.form['Seller']
        if (Seller == 'Dealer'):
            seller_type_Dealer = 1
            seller_type_Individual = 0
            seller_type_TrustmarkDealer = 0
        else:
            seller_type_Dealer = 0
            seller_type_Individual = 1
            seller_type_TrustmarkDealer = 0

        Transmission = request.form['Transmission']
        if (Transmission == 'Manual'):
            transmission_Automatic = 0
            transmission_Manual = 1
        else:
            transmission_Automatic = 1
            transmission_Manual = 0

        Owner = request.form['Owner']
        if (Owner == 'Owner1'):
            owner_First_Owner = 1
            owner_Second_Owner = 0
            owner_Fourth_Above_Owner = 0
            owner_Third_Owner = 0
            owner_Test_Drive_Car = 0
        if (Owner == 'Owner2'):
            owner_First_Owner = 0
            owner_Second_Owner = 1
            owner_Fourth_Above_Owner = 0
            owner_Third_Owner = 0
            owner_Test_Drive_Car = 0
        if (Owner == 'Owner3'):
            owner_First_Owner = 0
            owner_Second_Owner = 0
            owner_Fourth_Above_Owner = 0
            owner_Third_Owner = 1
            owner_Test_Drive_Car = 0
        else:
            owner_First_Owner = 0
            owner_Second_Owner = 0
            owner_Fourth_Above_Owner = 1
            owner_Third_Owner = 0
            owner_Test_Drive_Car = 0

        Gama = request.form['Gama']
        if (Gama == 'High'):
            gama = 1.9
        elif (Gama == 'Low'):
            gama = 0.5
        else:
            gama = 1

        prediction = model.predict([[km_driven, years_old, fuel_CNG, fuel_Diesel, fuel_Electric, fuel_LPG, fuel_Petrol, seller_type_Dealer, seller_type_Individual, seller_type_TrustmarkDealer, transmission_Automatic, transmission_Manual, owner_First_Owner, owner_Fourth_Above_Owner, owner_Second_Owner, owner_Test_Drive_Car, owner_Third_Owner]])
        output = round(prediction[0],2)
        output = float(output) * float(gama)
        output = float(output)/62
        output = round(output,2)

        if output<0:
            return render_template('index.html',prediction_texts="Error en el cálculo del precio")
        else:
            return render_template('index.html',prediction_text="Puedes vender el auto a € {}".format(output))

    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
        

        
        
