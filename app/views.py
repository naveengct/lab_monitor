from django.shortcuts import render
from . import urls
import mysql.connector
import random
import re,uuid 
from datetime import datetime
from django.http import HttpResponse
import socket
from django.shortcuts import redirect
# Create your views here.
def hello(request):
    return redirect('/home/')
def home(request):
    return render(request, 'home.html', {})
def login(request):
    return render(request, 'login.html', {})
def register(request):
    return render(request, 'register.html', {})

def user_detail(request):
    if(request.POST):
        login_data = request.POST.dict()
        id = login_data.get("id")
        #connection open
        mydb = mysql.connector.connect(
        host="remotemysql.com",
        user="hDGTaXLeeQ",
        passwd="PQkVWwUhEt",
        database="hDGTaXLeeQ"
        )
        mycursor = mydb.cursor()
        system_no=0
        mycursor.execute("SELECT * FROM user_table")
        myresult = mycursor.fetchall()
        c1=0
        for i in myresult:
            if i[3]==id and i[6]==1:
                c1=c1+1
        if c1==0:
            mycursor.execute("SELECT * FROM list")
            myresult = mycursor.fetchall()
            for x in myresult:
                if x[-1]==0:
                    system_no=x[1]
                    t=x[2]
                    mac=str
                    l=str(t[2:5])
                    a=random.randint(100,1000)
                    password=str(a)+str(l)
                    dateTimeObj = datetime.now()
                    sql = "INSERT INTO user_table(id,password,user,start_time,status) VALUES (%s, %s, %s, %s, %s)"
                    val = [
                    (t,password,id,dateTimeObj,1)
                    ]
                    mycursor.executemany(sql, val)
                    mycursor.execute("UPDATE list SET status=1 WHERE id='{0}'".format(t))
                    mydb.commit()
                    break
            mycursor.close()
            mydb.close()
            if system_no:
                return render(request, 'dis_user.html', {'system_no':system_no,'id':id,'password':password})
            else:
                info="Sorry!! None of the system are avilable.."
                return render(request, 'home.html', {'info':info})
        else:
                info="Sorry!! User already in use.."
                return render(request, 'home.html', {'info':info})

def access(request):
    login_data = request.POST.dict()
    password = login_data.get("password")
    t=str(hex(uuid.getnode()))
    mydb = mysql.connector.connect(
        host="remotemysql.com",
        user="hDGTaXLeeQ",
        passwd="PQkVWwUhEt",
        database="hDGTaXLeeQ"
        )
    mycursor = mydb.cursor()
    response=render(request, 'login.html', {'info':"Wrong password.."})
    mycursor.execute("SELECT * FROM user_table")
    myresult = mycursor.fetchall()
    for x in myresult:
        if x[1]==t and x[2]==password and x[-1]==1:
            user=x[3]
            mycursor.close()
            mydb.close()
            t1="Sucess"
            response=render(request, 'index.html', {'system_no':user,'id':t1})
            response.set_cookie('user',user)
            print(x[5])
            response.set_cookie('time',x[4])
            break        
    return response

def insert_data(request):
    login_data = request.POST.dict()
    system_no = login_data.get("system_no")
    t=str(hex(uuid.getnode()))
    mydb = mysql.connector.connect(
        host="remotemysql.com",
        user="hDGTaXLeeQ",
        passwd="PQkVWwUhEt",
        database="hDGTaXLeeQ"
        )
    mycursor = mydb.cursor()
    temp=""
    mycursor.execute("SELECT * FROM list")
    myresult = mycursor.fetchall()
    c1=0
    c2=0
    total_time=datetime.strptime("00:00:00","%H:%M:%S")
    for i in myresult:
        if int(i[1])==int(system_no):
            c1=c1+1
        if i[2]==t:
            c2=c2+1
    if c1==0 and c2==0:
        sql = "INSERT INTO list(system_no,id,total_time,status) VALUES (%s, %s, %s, %s)"
        val = [
        (system_no,t,total_time,0)
        ]
        mycursor.executemany(sql, val)
        mydb.commit()
    mycursor.close()
    mydb.close()
    if c1==0 and c2==0:
        return render(request, 'register.html', {'info':"System registered sucessfully...."})
    elif c1:
        return render(request, 'register.html', {'info':"Try another system number...."})
    else:
        return render(request, 'register.html', {'info':"System already registered...."})

def denied(request):
    user = request.COOKIES['user'] 
    time1 = request.COOKIES['time']
    time1=datetime.strptime(time1,"%Y-%m-%d %H:%M:%S")
    time2 = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    time3=datetime.strptime(time2,"%Y-%m-%d %H:%M:%S")
    time=time3-time1
    print(time)
    mydb = mysql.connector.connect(
        host="remotemysql.com",
        user="hDGTaXLeeQ",
        passwd="PQkVWwUhEt",
        database="hDGTaXLeeQ"
        )
    mycursor = mydb.cursor()
    response=render(request, 'logout.html', {'info':"No user...."})
    mycursor.execute("SELECT * FROM user_table")
    myresult = mycursor.fetchall()
    for x in myresult:
        if x[3]==user and x[-1]==1:
            mycursor.execute("UPDATE user_table SET end_time='{1}', status=0 WHERE user='{0}' and start_time='{2}'".format(user,time2,time1))
            mydb.commit()
            mycursor.execute("SELECT * FROM list where id='{0}'".format(x[1]))
            result = mycursor.fetchall()
            time=time+result[0][3]
            mycursor.execute("UPDATE list SET total_time='{1}', status=0 WHERE id='{0}'".format(x[1],time))
            mydb.commit()
            response=render(request, 'logout.html', {'info':"Logged out...."})
            response.delete_cookie('user')
            response.delete_cookie('time')
    mycursor.close()
    mydb.close()
    return response  