# @author AbdRahmen Amri
# @Licence MIT

'''
Machine learnig using to predict GPA
Algorithme: Regression Linear
Dependent DATA [ TP, DS, EXMAN]
Independent DATA [ MOYENNE ]
We use this ML to predict GPA from module grade point
'''
from pandas import read_csv
import numpy as np
data = read_csv('./gpa.csv')
x = data.iloc[:,:-1]
y = data.iloc[:,-1]
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test= train_test_split(x, y)
tp = x_train.iloc[:,:-2]
ds = x_train.iloc[:,1:-1]
exman = x_train.iloc[:,2:]
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(x_train, y_train)

def getGPA(arr):
    return "{:.2f}".format(model.predict(arr)[0])

def to_float(x):
    return float(x)






from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
@app.route("/api/v1/gpa",methods=['GET', 'POST'])
def GPA():
    try:
        if request.method == 'POST':
            tp = to_float(request.values.get('tp'))
            ds = to_float(request.values.get('ds'))
            exman = to_float(request.values.get('exman'))
        elif request.method == 'GET':
            tp = to_float(request.args.get('tp'))
            ds = to_float(request.args.get('ds'))
            exman = to_float(request.args.get('exman'))
    except:
        return jsonify({
            'ERROR':'TP DS EXMAN REQUIRED',
            'method':['POST','GET'],
            'URI':'/api/v1/gpa',
            'PARAM':'tp, ds, exman',
            'type':'float',
            'val':'[0.00 -> 20.00]'
            }),400
    if tp == None or ds == None or exman == None:
        return jsonify({
            'ERROR':'TP DS EXMAN REQUIRED',
            'method':['POST','GET'],
            'URI':'/api/v1/gpa',
            'PARAM':'tp, ds, exman',
            'type':'float',
            'val':'[0.00 -> 20.00]'
            }),400
    
    return jsonify({
        "gpa":getGPA([[tp,ds,exman]])
    }),200

    

if __name__ == '__main__':
   app.run()