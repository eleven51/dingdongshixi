from flask import Flask,render_template,request,flash
import pymysql

app = Flask(__name__)
@app.route('/')
def hello_world():
    # 跳转到首页
    return render_template("index1.html")

@app.route("/select")
def select():
    #跳转到选择注册员工或管理者界面
    return  render_template("select.html")

@app.route("/register")
def user_register():
    #跳转到员工注册界面
    return  render_template("register.html")

@app.route("/register_mana")
def manager_register():
    #跳转到管理员注册界面
    return  render_template("manager.html")

@app.route("/login")
def user_login():
    # 跳转到登录界面
    return render_template("login.html")

#员工注册界面
@app.route("/doregister")
def register():
   name = request.args.get("uname")
   phone = request.args.get("uphone")
   print(type(phone))
   cpny = request.args.get("ucpny")
   dptmt = request.args.get("udptmt")
   pwd = request.args.get("upwd")
   pwd2 = request.args.get("upwd2")
   if pwd == pwd2:
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
         print("register succeeded")
         sql = "insert into mystaffs values(null,%s,%s,%s,%s,%s)"
         cs.execute(sql,args)
         conn.commit()
         # flash("注册成功！")
         return render_template("login.html")
     else:
       print("register failed")
       return "该手机号已被注册"
   else:
       return "两次密码不相同！请重新输入！"

# 管理员注册界面
@app.route("/doregister_mana")
def register_mana():
    mname = request.args.get("mname")
    mphone = request.args.get("mphone")
    mcompany = request.args.get("mcompany")
    mpassword = request.args.get("mpassword")
    smpassword = request.args.get("smpassword")
    if mpassword == smpassword:
        print(mname,mphone,mcompany,mpassword)
        args = [mname,mphone,mcompany,mpassword]
        conn = pymysql.connect(host="127.0.0.1", port=3306, db="kuu", user="root", password="mysql002657",
                               charset="utf8")
        cs = conn.cursor()
        sql = "select * from mymanagers"
        aa = cs.execute(sql)
        all_managers = cs.fetchall()
        all_managers = list(all_managers)
        has_regiter = 0
        i = 0
        while i < len(all_managers):
            for phones in list(all_managers):
                if mphone in list(phones):
                    print('cunzai')
                    has_regiter = 1
            i += 1
        if has_regiter == 0:
            print("register succeeded")
            sql = "insert into mymanagers values(null,%s,%s,%s,%s)"
            cs.execute(sql, args)
            conn.commit()
            # flash("注册成功！")
            return render_template("login.html")
        else:
            print("register failed")
            return "该手机号已被注册"
    else:
        return "两次密码输入不相同！请重新输入！"


# 登录界面
@app.route("/dologin")
def login():
    position = request.args.get("position")
    phone = request.args.get("phone")
    password = request.args.get("pwd")
    print(phone,password)
    conn = pymysql.connect(host="127.0.0.1", port=3306, db="kuu", user="root", password="mysql002657", charset="utf8")
    cs = conn.cursor()
    if position == 'staff':
        sql = "select * from mystaffs where  (uphone = %s) and (upwd = %s)"
    else:
        sql = "select * from mymanagers where  (mphone = %s) and (mpassword = %s)"
    aa = cs.execute(sql,[phone,password])
    print(aa)
    conn.commit()
    if aa == 1:
        print("login succeeded")
        # flash("登录成功！")
        if position == 'staff':
            return render_template("home.html")
        else:
            return render_template("home_manager.html")
    else:
        return "手机号或密码输入错误"

if __name__ == '__main__':
    app.run()

