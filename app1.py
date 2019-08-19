from flask import Flask,render_template,request,flash
import pymysql

app = Flask(__name__)
@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'

@app.route("/register")
def user_register():
    #跳转到注册界面
    return  render_template("register.html")

@app.route("/login")
def user_login():
    return render_template("login.html")

#注册界面
@app.route("/doregister")
def register():
   name = request.args.get("uname")
   phone = request.args.get("uphone")
   print(type(phone))
   cpny = request.args.get("ucpny")
   dptmt = request.args.get("udptmt")
   pwd = request.args.get("upwd")
   print(name,phone,cpny,dptmt,pwd)
   args = [name, phone, cpny, dptmt, pwd]
   conn = pymysql.connect(host="127.0.0.1",port=3306,db="kuu",user="root",password="mysql002657",charset="utf8")
   cs = conn.cursor()
   sql = "select * from mystaffs"
   aa = cs.execute(sql)
   # print(aa)
   all_users= cs.fetchall()
   all_users = list(all_users)
   # print(all_users)
   has_regiter = 0
   i = 0
   while i < len(all_users):
       for phones in list(all_users):
           if phone in list(phones):
               print('cunzai')
               has_regiter = 1
       i+=1
   if has_regiter == 0:
       sql = "insert into mystaffs values(null,%s,%s,%s,%s,%s)"
       cs.execute(sql,args)
       conn.commit()
       return render_template("login.html")
   else:
       print("register failed")
       return "该手机号已被注册"

@app.route("/dologin")
def login():
    phone = request.args.get("phone")
    password = request.args.get("pwd")
    print(phone,password)
    conn = pymysql.connect(host="127.0.0.1", port=3306, db="kuu", user="root", password="mysql002657", charset="utf8")
    cs = conn.cursor()
    sql = "select * from mystaffs where  (uphone = %s) and (upwd = %s)"
    aa = cs.execute(sql,[phone,password])
    print(aa)
    conn.commit()
    if aa == 1:
        print("login succeeded")
        return render_template("home.html")
    else:
        return "手机号或密码输入错误"
if __name__ == '__main__':
    app.run()

