__author__ = 'KarthikWitty'

from flask import Flask,jsonify,abort,url_for,g,request,Response
import pymysql
import datetime
import json



'''Database: MYSQL Flask Rest API for Evaluation:
 "Endpoint Name: object" "Table Name: sample with columns ID, VALUE and timestamp"

 '''

try:
    app=Flask(__name__)

    @app.before_request
    def get_connection():

        '''Database Configuration for Pythonanywhere Hosted in Web..'''
        g.conn=pymysql.connect(host="Karthik.mysql.pythonanywhere-services.com",port=3306,user='Karthik',password='vaultdragon',db='data')

        #URL is karthik.pythonanywhere.com

        '''Database Configuration of for local database '''

        #g.conn=pymysql.connect(host="localhost",port=3306,user='root',db='mysql')
        g.cursor=g.conn.cursor()

    @app.route('/')
    def index():
        return "Flask-API Project"


    @app.after_request
    def close_connection(response):
        g.cursor.close()
        g.conn.close()
        return response

    def query_db(query, args=(), one=False):
        g.cursor.execute(query, args)
        rv = [dict((g.cursor.description[idx][0], value)
        for idx, value in enumerate(row)) for row in g.cursor.fetchall()]
        return (rv[0] if rv else None) if one else rv

    @app.route('/object/<id>', methods=['GET'])
    def get_task(id):
        ''' "object is Implemented in Get Method to get the value corresponding to ID For Eg:/object/1"'''
        result = query_db("SELECT VALUE FROM sample where id='"+id+"'")
        data = json.dumps(result)
        resp = Response(data, status=200, mimetype='application/json')
        return resp

    @app.route('/object',methods=['POST'])
    def post():
        '''"object is Implemented in Post Method to post the values . Eg: /object {'ID':'Value'} in json body"'''
        req=request.get_json()
        time=str(datetime.datetime.utcnow().strftime("%H%M%S"))
        g.cursor.execute("insert into sample(ID,VALUE,timestamp) VALUES ('"+str(req['ID'])+"','"+str(req['VALUE'])+"','"+str(time)+"') ON DUPLicate key update id='"+str(req['ID'])+"',value='"+str(req['VALUE'])+"',timestamp='"+str(time)+"'")
        g.conn.commit()
        response=Response("Updated",status=201,mimetype='application/json')
        return response


    @app.route('/object/<id>',methods=['GET'])
    def get_value(id):

        ''' "object is Implemented in Get Method to get the values based on timestamp. Eg: /object/1?timestamp=040102 and
            I have taken only the Hour minute second part from UTC time."'''

        time=request.args.get('timestamp')
        result=query_db("select value from sample where id='"+id+"' and timestamp='"+str(time)+"'")
        response=json.dumps(result)
        return Response(response,200,mimetype="application/json")


    if __name__ == '__main__':
        app.run(debug=True)

except Exception as e:
    raise Exception(e)


