from django.shortcuts import render
from django.http import HttpResponse 
import pymysql
from lib import wordcheck as wd
import random
from django.shortcuts import redirect
import re
from django.views.decorators.clickjacking import xframe_options_sameorigin 
# Create your views here.

@xframe_options_sameorigin 
def index(request):
    if request.method == "GET": 
        sessionid = request.COOKIES.get("sessionid") 
        logincookie = request.COOKIES.get("login")
        login=False
        if logincookie == None and sessionid !=None:
            response=render(request,"login.html",locals()) 
            response.delete_cookie("sessionid")
            return response
        if sessionid != None :
            username = request.session.get("username")
            if username != None:
                login=True
                return render(request,"paper.html",locals())
    
        return  render(request,"login.html",locals()) 
    else:###################################################!POST 

        #寫入文章
        message=request.POST.get("message")
        if message != None :
            message=re.sub(r"^\n|\n$","",re.sub((r'( {2,})'),' ',re.sub(r"\n\s+",r"\n",message)))
            if message != "嗨!朋友:" and len(message)>0:
                author = request.session.get("username")
                db = pymysql.connect(host="127.0.0.1", user="kunwei",passwd="mysqlkun19960212@@",database="kunwei") 
                cursor = db.cursor()
                sql="insert into message (Author,value) values (%s,%s)"
                cursor.execute(sql,(author,message)) 
                db.commit()
                db.close()
                return redirect("/")
        #檢查帳密
        username=request.POST.get("username")
        password=request.POST.get("password")
        if username != None:
            db = pymysql.connect(host="127.0.0.1", user="kunwei",passwd="mysqlkun19960212@@",database="kunwei") 
            cursor = db.cursor()
            sql="select * from member where UserName= %s "
            cursor.execute(sql,(username)) 
            db.commit()
            if not cursor.fetchone():#如果帳號不在資料庫內
                if username == None:
                    username=""
                db.close()
                return render(request,"login.html",{"username":username,"usernameerror":"此帳號不存在，請確認沒打錯字"})
            else:#如果帳號在資料庫內
                sql="select * from member where UserName= %s and Password= %s "
                cursor.execute(sql,(username,password))
                db.commit() 
                if not cursor.fetchone():#密碼不對
                    db.close()
                    return render(request,"login.html",{"username":username,"passworderror":"密碼錯誤"})

            request.session["username"]=username
            request.session["password"]=password
            response=render(request,"loginyes.html",locals())
            response.set_cookie("login","dkksidopqpdkvdlwlfjalsic",max_age=31536000)
            db.close()
            return response
        return redirect("/")
    

def signup(request): 
    if request.method == "GET":
        return  render(request,"signup.html",locals())   
    else:
        usererror={"error":0,"username":"","password":"","conmfirm_password":""}

        username=request.POST.get("username") 
        password=request.POST.get("password")
        comfirm_password = request.POST.get("comfirm_password")
        db = pymysql.connect(host="127.0.0.1", user="kunwei",passwd="mysqlkun19960212@@",database="kunwei")
        cursor = db.cursor() 

        if wd.username(username): #wd.username 為True時 表示帳號沒有特殊字

            sql="select * from member where UserName=%s"
            cursor.execute(sql,(username))
            db.commit()
            if cursor.fetchone():
                usererror["error"]=usererror["error"]+1
                usererror["username"]="此帳號已有人使用"
        else:
            usererror["username"]="帳號僅接受大小寫英文與數字"



        if not wd.password(password):
            usererror["error"]=usererror["error"]+1
            usererror["password"]="密碼僅接受大小寫英文,數字與以下符號:!@$%^?~"
        else:
            if password != comfirm_password:
                usererror["error"]=usererror["error"]+1
                usererror["conmfirm_password"]="密碼與確認密碼不相符"  


        
        if usererror["error"] !=0:
            db.close()
            return render(request,"signup.html",locals()) 

        sql="insert into member (UserName,Password) values (%s,%s)"
        cursor.execute(sql,(username,password))
        db.commit()
        db.close()

        return render(request,"signupyes.html",locals())

def api(request):
    db = pymysql.connect(host="127.0.0.1", user="kunwei",passwd="mysqlkun19960212@@",database="kunwei")
    cursor = db.cursor()
    sql='SELECT max(id) FROM message'
    cursor.execute(sql)
    db.commit()
    max=int(cursor.fetchone()[0])
    apimessage="目前還沒有任何漂流瓶喔~~快去寫封信丟進星空中吧"
    while True:
        randint=int(random.randint(1,max))
        sql='SELECT value FROM message where id= %s'
        cursor.execute(sql,(randint)) 
        db.commit()
        apimessage = cursor.fetchone()[0]
        if apimessage != None:
            break
    # 隨機取資料庫內的資料
    db.close()
    return render(request,"messageapi.html",locals())

def apimessage(request):
    return HttpResponse("還沒")

# db = pymysql.connect(host="127.0.0.1", user="kunwei",passwd="mysqlkun19960212@@",database="kunwei")
# cursor = db.cursor()
# strSQL='select * from dc_pool '
# cursor.execute(strSQL) 
# results=cursor.fetchall()
# res=random.choice(results)
# 隨機取資料庫內的資料

#找出所有東西從`content`命名為t1與交集(找 )
