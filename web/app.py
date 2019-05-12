from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.BankAPI
users=db["Users"]

def UserExists(username):
    if users.find({"Username":username}).count() == 0:
        return False
    else:
        return True

def verifyPassword(username,password):
    if not UserExists(username):
        return False


    hashed_pwd= users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'),hashed_pwd) == hashed_pwd:
        return True
    else:
        return False

def Balance(username):
    cash=users.find({
        "Username":username
    })[0]["Credit"]
    return cash

def Loan(username):
    debit=users.find({
        "Username":username
    })[0]["Debit"]
    return debit

def generateReturnDictionary(status,msg):
    retJson={
        "status":status,
        "msg":msg
    }
    return retJson

def verifyCredentials(username,password):
    if not UserExists(username):
        return generateReturnDictionary(301,"invalid Username"), True

    correct_pw = verifyPassword(username,password)

    if not correct_pw:
        return generateReturnDictionary(302,"Incorrect Password"), True

    return None, False

def updateAccount(username,balance):
    users.update({
        "Username":username
    },{
        "$set":{
            "Credit": balance
        }
    })

def updateLoan(username,balance):
    users.update({
        "Username":username
    },{
        "$set":{
            "Debit": balance
        }
    })

class Register(Resource):
    def post(self):
        postedData= request.get_json()

        username = postedData["username"]
        password = postedData["password"]


        if UserExists(username):
            print("Checking the user,,,")
            retJson = {
                "status": "301",
                "msg": "Invaid Username"
            }
            return jsonify(retJson)

        hashed_pwd = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            "Username": username,
            "Password": hashed_pwd,
            "Credit":0,
            "Debit":0
        })

        retJson= {
            "status": 200,
            "msg": "You succesfully signed up for the API"
        }
        return jsonify(retJson)

class Add(Resource):
    def post(self):
        postedData=request.get_json()
        username=postedData["username"]
        password=postedData["password"]
        money=postedData["amount"]

        retJson, error = verifyCredentials(username, password)

        if error:
            return jsonify(retJson)

        if money<=0:
            return generateReturnDictionary(304,"The money amount entered must be > 0")

        cash= Balance(username)
        money-=1
        bank_cash=Balance("BANK")
        updateAccount("BANK", bank_cash+1)
        updateAccount(username,cash+money)

        return generateReturnDictionary(200," Account succesfully credited")

class Transfer(Resource):
    def post(self):
        postedData=request.get_json()
        username=postedData["username"]
        password=postedData["password"]
        to      =postedData["to"]
        money   =postedData["amount"]

        retJson, error = verifyCredentials(username,password)

        if error:
            return jsonify(retJson)

        cash = Balance(username)
        if cash<=0:
            return jsonify(generateReturnDictionary(304," You are out of money! Please add or take a loan"))

        if not UserExists(to):
            return jsonify(generateReturnDictionary(301," Receiver username is invalid"))

        cash_from = Balance(username)
        cash_to   = Balance(to)
        bank_cash = Balance("BANK")

        updateAccount("BANK",bank_cash+1)
        updateAccount(to,cash_to + money - 1)
        updateAccount(username,cash_from-money)

        return jsonify(generateReturnDictionary(200," Amount tranferred succesfully"))

class AccountBalance(Resource):
    def post(self):
        postedData=request.get_json()
        username=postedData["username"]
        password=postedData["password"]

        retJson, error = verifyCredentials(username,password)

        if error:
            return jsonify(retJson)

        retJson= users.find({
            "Username":username
        },{
            "Password":0,
            "_id":0
        })[0]

        return jsonify(retJson)

class TakeLoan(Resource):
    def post(self):
        postedData=request.get_json()

        username=postedData["username"]
        password=postedData["password"]
        money   =postedData["amount"]

        retJson, error = verifyCredentials(username, password)

        if error:
            return jsonify(retJson)

        cash = Balance(username)
        debt = Loan(username)
        updateAccount(username, cash+money)
        updateLoan(username,debt+money)

        return jsonify(generateReturnDictionary(200," Loan added to your account"))

class payLoan(Resource):
    def post(self):
        postedData=request.get_json()

        username=postedData["username"]
        password=postedData["password"]
        money   =postedData["amount"]

        retJson, error = verifyCredentials(username,password)

        if error:
            return jsonify(retJson)

        cash=Balance(username)
        if cash<money:
            return jsonify(generateReturnDictionary(303," Insufficeint balance"))

        debt = Loan(username)

        updateAccount(username,cash-money)
        updateLoan(username,debt-money)

        return jsonify(generateReturnDictionary(200," Loan repaid"))

api.add_resource(Register, '/register')
api.add_resource(Add,'/add')
api.add_resource(AccountBalance,'/balance')
api.add_resource(Transfer,'/tranfer')
api.add_resource(TakeLoan,'/takeloan')
api.add_resource(payLoan,'/payLoan')

if __name__=='__main__':
    app.run(host='0.0.0.0')
