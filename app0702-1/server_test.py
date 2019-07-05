# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 17:56:33 2019

@author: Azumi Mamiya

pip3 install flask
pip3 install mysql-connector-python
"""
from flask import Flask,request,render_template
from flask import Flask, make_response
import my_function2_demo as my_func
import sys

app = Flask(__name__)
#server host
server_host='test-server0701.herokuapp.com'
server_port=50000
#SQL server
SQLserver_host='192.168.0.32'
SQLserver_port=3306
database_name='hydration_db'

@app.route("/")
def entry():
    resp = make_response(render_template('index.html',serverhost=server_host,serverport=server_port))
    #resp.set_cookie('user', 'daiki')
    #resp.set_cookie('pass', 'miyagawa')
    resp.set_cookie('user', '')
    resp.set_cookie('pass', '')
    #resp.set_cookie('user', 'tomohiro')
    #resp.set_cookie('pass', 'tsuchiya')
    return resp

@app.route("/hello", methods=["GET","POST"])
def hello():
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    print("ID:{} LOGIN ".format(userid),end='')
    #connect test
    try:#success
        hantei=my_func.kakunin(userid,userpass,SQLserver_port,SQLserver_host,database_name)
    except:#fail
        hantei=False
    print(hantei)
    if hantei:
        return render_template('hello.html', title='flask test', name=userid,serverhost=server_host,serverport=server_port)# lonin success
    else:
        return 'either id or pass is not match'# login fail

@app.route("/show", methods=["POST"])
def show():
    #userid = request.form['user']
    #userpass = request.form['pass']
    if request.cookies.get('user') == '':
        userid = request.form['user']
        userpass = request.form['pass']
        print("ID:{} GET ".format(userid),end='')
        try:
            data=my_func.sql_data_get(userid,userpass,SQLserver_port,SQLserver_host,database_name)
            posts=[]
            for d in reversed(data):
                posts.append({
                  'date' : str(d[0]),
                  'bweight' : str(d[1]),
                  'aweight' : str(d[2]),
                  'training' : str(d[3]),
                  'period' : str(d[4]),
                  'intake' : str(d[5]),
                  'dehydraterate' : str(d[6]),
                  'dehydrateval' : str(d[1] - d[2])
                })
            print('Success')
            resp = make_response(render_template('main.html', title='My Title', user=userid, posts=posts,serverhost=server_host,serverport=server_port)
    )
            #resp.set_cookie('user', 'daiki')
            #resp.set_cookie('pass', 'miyagawa')
            resp.set_cookie('user', userid)
            resp.set_cookie('pass', userpass)
            return resp
        except:
            print('Fail')
            return 'NG'
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    print("ID:{} GET ".format(userid),end='')
    try:
        data=my_func.sql_data_get(userid,userpass,SQLserver_port,SQLserver_host,database_name)
        posts=[]
        for d in reversed(data):
            posts.append({
              'date' : str(d[0]),
              'bweight' : str(d[1]),
              'aweight' : str(d[2]),
              'training' : str(d[3]),
              'period' : str(d[4]),
              'intake' : str(d[5]),
              'dehydraterate' : str(d[6]),
              'dehydrateval' : str(d[1] - d[2])
            })
        print('Success')
        return render_template('main.html', title='My Title', user=userid, posts=posts,serverhost=server_host,serverport=server_port)
    except:
        print('Fail')
        return 'NG'

#@app.route("/entry", methods=["POST"])
@app.route("/enter", methods=["GET","POST"])
def enter():
    #userid = request.form['user']
    #userpass = request.form['pass']
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    print("ID:{} GET ".format(userid))
    try:
        weight_after= float(request.form['wa'])
        weight_before= float(request.form['wb'])
        contents= str(request.form['text'])
        time= float(request.form['time'])
        moisture= float(request.form['moi'])
        tenki= int(request.form['tenki'])
        shitsudo= float(request.form['sitsu'])
        my_func.sql_data_send(userid,userpass,SQLserver_port,SQLserver_host,database_name,weight_after,weight_before,contents,time,moisture,tenki,shitsudo)
        data=my_func.sql_data_get(userid,userpass,SQLserver_port,SQLserver_host,database_name)
        posts=[]
        for d in reversed(data):
            posts.append({
              'date' : str(d[0]),
              'bweight' : str(d[1]),
              'aweight' : str(d[2]),
              'training' : str(d[3]),
              'period' : str(d[4]),
              'intake' : str(d[5]),
              'dehydraterate' : str(d[6]),
              'dehydrateval' : str(d[1] - d[2])
            })

        return render_template('main.html', title='My Title', user=userid, posts=posts,serverhost=server_host,serverport=server_port)
        #return render_template('result.html', title='My Title', user=userid, posts=posts)
    except Exception as error:
        return error.__str__()

# administration page
@app.route("/admin")
def admin_entry():
    html = render_template('admin_index.html')
    return html

@app.route("/adminwindow", methods=["POST"])
def admin_window():
    userid = request.form['user']
    userpass = request.form['pass']
    administrator=['azumi']
    
    print('ID:{} ADMINLOGIN '.format(userid))
    if userid in administrator:
        print('Success')
        return render_template('adminwindow.html')
    else:
        print('Fail')
        return 'you are not an administrator'


















if __name__ == "__main__":
    app.run(debug=False, host=server_host, port=server_port, threaded=True)