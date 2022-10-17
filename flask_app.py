import sqlite3
import math
import array as arr
import smtplib
import email.utils
from email.mime.text import MIMEText
from random import randint
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from flask_mail import Mail, Message

from werkzeug.exceptions import abort #Для ответа 404
from flasgger import Swagger

from cryptohash import sha1


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ketzelbretzel'

swagger = Swagger(app)

def genMail():
    return randint(0, 1000000)

def send2fa(mailToAuth):

    print("mailToAuth =", mailToAuth)
    codeMail = randint(100, 1000000)
    msg = MIMEText('Here is yours registration code:\n' + str(codeMail))
    msg['To'] = email.utils.formataddr(('LKGservice user', mailToAuth))
    msg['From'] = email.utils.formataddr(('LKGservice', 'daniilprotasove@gmail.com'))
    msg['Subject'] = 'Second step of authentication'

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    print(f"SMTP_SSL done")
    server.login('daniilprotasove@gmail.com', 'dvfaxfvzxeeazuss')
    print(f"login done")


    try:
        res = server.sendmail('daniilprotasove@gmail.com', mailToAuth, msg.as_string())
    finally:
        pass

    return codeMail

def genCookie():

    cookieToRet = temp = chr(randint(33, 127))
    for x in range(15):
        temp = chr(randint(33, 127))
        cookieToRet = cookieToRet + temp

    return cookieToRet

def send_for_forgpsw(mailToAuth):

    codeMail = genCookie()
    msg = MIMEText('Here is yours new password:\n' + str(codeMail))
    msg['To'] = email.utils.formataddr(('LKGservice user', mailToAuth))
    msg['From'] = email.utils.formataddr(('LKGservice', 'daniilprotasove@gmail.com'))
    msg['Subject'] = 'New password'

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    print(f"SMTP_SSL done")
    server.login('daniilprotasove@gmail.com', 'dvfaxfvzxeeazuss')
    print(f"login done")


    try:
        res = server.sendmail('daniilprotasove@gmail.com', mailToAuth, msg.as_string())
    finally:
        pass

    return codeMail



def get_db_connection(dbName):
    dbConnection = sqlite3.connect(dbName)
    dbConnection.row_factory = sqlite3.Row

    cursor = dbConnection.cursor()
    return dbConnection


# Функция нахождения наибольшего простого делителя:
def max_simple_divider(m):
    ans = 1
    d = 2
    while (d * d <= m):
        if (m % d == 0):
            ans = d
            m = m//d
        else:
            d = d + 1
    if (m > 1):
        ans = m
    return ans;

def oraculus(x0, x1, x2, x3):
    a = 1
    c = 1
    m = max(max(x1, x2), max(x3, x0))
    b = 1

    ost1 = x2 - x1
    ost2 = x3 - x2
    ost3 = x3 - x1
    prea1 = x1 - x0
    prea2 = x2 - x1
    prea3 = x2 - x0
    while (m < 65336):
        save_b = max_simple_divider(m)
        b = save_b
        ost1s = ost1
        ost2s = ost2
        ost3s = ost3
        if(ost1s < 0):
            ost1s = m + ost1s
        if(ost2s < 0):
            ost2s = m + ost2s
        if(ost3s < 0):
            ost3s = m + ost3s
        a = b + 1
        while(a < m):
            if (prea1 >= 0 and prea2 >= 0 and prea3 >= 0):
                if((prea1 * a)%m == ost1s and (prea2 * a)%m == ost2s and (prea3 * a)%m == ost3s):
                    c = x2 - ((a * x1)%m)
                    if ( c < 0):
                        c = m + c
                    return (a*x3 + c )%m
            if (prea1 < 0 and prea2 >= 0 and prea3 >= 0):
                q = ((prea1 * a) / m) - 1
                if((prea1 * a) - (m*q) == ost1s and (prea2 * a)%m == ost2s and (prea3 * a)%m == ost3s):
                    c = x2 - ((a * x1)%m)
                    if ( c < 0):
                        c = m + c
                    return (a*x3 + c )%m
            if (prea1 >= 0 and prea2 < 0 and prea3 >= 0):
                q = ((prea2 * a) / m) - 1
                if((prea1 * a)%m == ost1s and (prea2 * a) - (m*q) == ost2s and (prea3 * a)%m == ost3s):
                    c = x2 - ((a * x1)%m)
                    if ( c < 0):
                        c = m + c
                    return (a*x3 + c )%m
            if (prea1 < 0 and prea2 < 0 and prea3 >= 0):
                q1 = ((prea1 * a) / m) - 1
                q2 = ((prea2 * a) / m) - 1
                if((prea1 * a) - (m*q1) == ost1s and (prea2 * a) - (m*q2) == ost2s and (prea3 * a)%m == ost3s):
                    c = x2 - ((a * x1)%m)
                    if ( c < 0):
                        c = m + c
                    return (a*x3 + c )%m
            if (prea1 >= 0 and prea2 >= 0 and prea3 < 0):
                q = ((prea3 * a) / m) - 1
                if((prea1 * a)%m == ost1s and (prea2 * a)%m == ost2s and (prea3 * a) - (m*q) == ost3s):
                    c = x2 - ((a * x1)%m)
                    if ( c < 0):
                        c = m + c
                    return (a*x3 + c )%m
            if (prea1 < 0 and prea2 >= 0 and prea3 < 0):
                q1 = ((prea1 * a) / m) - 1
                q3 = ((prea3 * a) / m) - 1
                if((prea1 * a) - (m*q1) == ost1s and (prea2 * a)%m == ost2s and (prea3 * a) - (m*q3) == ost3s):
                    c = x2 - ((a * x1)%m)
                    if ( c < 0):
                        c = m + c
                    return (a*x3 + c )%m
            if (prea1 >= 0 and prea2 < 0 and prea3 < 0):
                q2 = ((prea2 * a) / m) - 1
                q3 = ((prea3 * a) / m) - 1
                if((prea1 * a)%m == ost1s and (prea2 * a) - (m*q2) == ost1s and (prea3 * a) - (m*q3) == ost3s):
                    c = x2 - ((a * x1)%m)
                    if ( c < 0):
                        c = m + c
                    return (a*x3 + c )%m
            if (prea1 < 0 and prea2 < 0 and prea3 < 0):
                q1 = ((prea1 * a) / m) - 1
                q2 = ((prea2 * a) / m) - 1
                q3 = ((prea3 * a) / m) - 1
                if((prea1 * a) - (m*q1) == ost1s and (prea2 * a) - (m*q2) == ost1s and (prea3 * a) - (m*q3) == ost3s):
                    c = x2 - ((a * x1)%m)
                    if ( c < 0):
                        c = m + c
                    return (a*x3 + c )%m
            b = b + save_b
            a = b + 1
        m = m + 1
    return 0

def schet_period(a, c, m):
        x = randint(1, m)
        periodd = 2
        x = (a * x + c) % m
        nach = x
        x = (a * x + c) % m
        while (x!=nach):
            x = (a * x + c) % m
            if (x!=nach):
                periodd = periodd + 1
                if(periodd > (2 * m)):
                    return periodd
        return periodd




@app.route('/', methods = ["GET"])
def indexGET():
    """Main html of the project.
    GET method checks if session exists.
    +\tIf it is - redirects to page of sequnce create for user of this session.
    -\tIf not - asks to enter the correct data.
    ---
    tags:
      - User login page
    responses:
      200:
        description: No response just renders login page ('index' page of the project)
        schema:
          $ref: '/'
    """

    if 'user' in session:
        return redirect(url_for('createGET'))

    if not request.cookies.get('curuser'):
        return render_template('index.html')
    else:
        return redirect(url_for('createGET'))

    return render_template()


@app.route('/', methods = ["POST"])
def indexPOST():
    """Main html of the project.
    POST method does next:
    1) Reads the data from fields login and password.
    2) Reads DB data of users.
    -\t\t2.1) If data is correct - redirects to confirmation page with 2fa
    -\t\t2.1) If data is not correct - re-render this page with same values so user can edit their input
    ---
    tags:
      - User login page
    parameters:
      - name: login
        in: path
        type: string
        required: true
        default: "none default value"
        description: User login

      - name: password
        in: path
        type: string
        required: true
        default: "none default value"
        description: User password

    responses:
      200:
        description: If login process was successful - redirects to 2fa page. If not - asks for data re-enter.
        schema:
          $ref: '/confirmation'
    """

    cookie = request.cookies.get('curuser', None)
    print("cookie = ", cookie)


    login = request.form['uname']
    password = request.form['psw']
    hPass = sha1(password)

    conn = get_db_connection('usersDB.db')
    users = conn.execute('SELECT user_name, password, email FROM users;').fetchall()

    print(password)
    print(hPass)
    print("login = ", login)


    for row in users:
        print(row[1])
        if (login == row[0] and hPass == row[1]):
            res = make_response(render_template('base.html'))
            res.set_cookie('curuser', login)

            name = request.cookies.get('curuser', None)
            print("cookie = ", name)

            code = send2fa(row[2])

            conn.execute("UPDATE users SET curAuthMail = ? WHERE email = ?", [code, row[2]])
            conn.commit()
            conn.close()

            EmailE = row[2]

            session['email'] = str(EmailE)

            render_template('confirmation.html', mailCur = str(EmailE))

            return redirect(url_for('confirmationGET'))

    conn.commit()
    conn.close()
    return render_template('index.html', otv = 'Неверное имя пользователя или пароль!')



@app.route('/confirmation', methods = ["GET"])
def confirmationGET():
    """HTML page for 2fa.
    GET method checks if session exists:
    +\tIf it does - takes mail value of the current session and re-render the page for POST for code enter.
    -\tIf session doesn't exists - redirects user to 'index' page for login procedure.
    ---
    tags:
      - User 2fa (confirmation) page

    responses:
      200:
        description: No response just renders 2fa (confirmation) page
        schema:
          $ref: '/confirmation'
    """

    if not 'email' in session:
        return redirect(url_for('indexGET'))

    emailCur = session.get('email', None)

    return render_template('confirmation.html', mailCur = emailCur)


@app.route('/confirmation', methods = ["POST"])
def confirmationPOST():
    """HTML page for 2fa.
    POST method does next:
    1) Reads the data from page code field.
    2) Reads DB data of users.
    -\t\t2.1) If entered and sended code are equal - redirects user to 'sequenc create' page.
    -\t\t2.1) If data is not correct - re-render this page with empty code field. Then user must enter either a code, or '0' value for re-send the confirmation page.
    ---
    tags:
      - User 2fa (confirmation) page
    parameters:
      - name: code
        in: path
        type: integer
        required: true
        default: "none default value"
        description: Confirmation code user which must enter. Code sends in previos step (login page) to email.


    responses:
      200:
        description: <br>If 2fa process was successful - redirects to sequence create page.</br>If not - asks for data re-enter.
        schema:
          $ref: '/create'
    """
    emailCur = session.get('email', None)

    print ("mail = ", emailCur)

    codePage = int(request.form['mailConfCode'])

    if codePage == 0:
        conn = get_db_connection('usersDB.db')

        code = send2fa(emailCur)

        conn.execute("UPDATE users SET curAuthMail = ? WHERE email = ?", [code, emailCur])
        conn.commit()
        conn.close()
        return render_template('confirmation.html', mailCur = emailCur, otv = 'Повторное письмо было выслано на вашу почту.')



    conn = get_db_connection('usersDB.db')
    userTable = conn.execute('SELECT curAuthMail FROM users WHERE email = ?;', [emailCur]).fetchall()
    userTableCookie = conn.execute('SELECT curCookie FROM users WHERE email = ?;', [emailCur]).fetchall()

    codeTable = userTable[0][0]
    codeTable = int(codeTable)
    conn.close()



    if not codeTable == codePage:
        return render_template('confirmation.html', mailCur = emailCur, otv = 'Неверный код подтверждения. Повторите попытку.')

    userTableCookie = userTableCookie[0][0]
    session['user'] = str(userTableCookie)

    return redirect(url_for('createGET'))




@app.route('/registration', methods = ["GET"])
def registrationGET():
    """This is the user registration page.
    GET method does nothing except renders the 'registration.html' page.
    <br>User must create his credentials and enter them to the field</br>
    <br>For security reason passord must be not less than 6 simbols in length</br>
    ---
    tags:
      - User registration page

    responses:
      200:
        description: No response just renders registration page
        schema:
          $ref: '/registration'
    """
    return render_template('registration.html')

@app.route('/registration', methods = ["POST"])
def registrationPOST():
    """This is the user registration page.
    POST method does next:
    1) Reads the data from fields 'login', 'password' and 'email'.
    2) Reads DB data of users.
    -\t\t2.1) If entered email and login does not registered yet - enters values to DB and redirects to registrationGET with message 'Регистрация прошла успешно!'.
    -\t\t2.1) If data is not correct (password len less than 6 simbols or login/mail already registered) - re-render this page with empty fields. Then user must enter new values.
    ---
    tags:
      - User registration page
    parameters:
      - name: login
        in: path
        type: string
        required: true
        default: "none default value"
        description: Login which user must create. Must be unique in DB.

      - name: password
        in: path
        type: string
        required: true
        default: "none default value"
        description: Password which user must create. Len of the password must be more than 6 chars.

      - name: mail
        in: path
        type: string
        required: true
        default: "none default value"
        description: Mail address owened by the user. Must be actual and available, because it's using in 2fa.


    responses:
      200:
        description: <br>If new user registration process was successful - redirects to registrationGET.</br>If not - do the same, but asks for data re-enter.
        schema:
          $ref: '/create'
    """
    conn = get_db_connection('usersDB.db')
    users = conn.execute('SELECT user_name FROM users;').fetchall()
    emails = conn.execute('SELECT email FROM users;').fetchall()

    login = request.form['uname']
    password = request.form['psw']
    hPass = sha1(password)
    email = request.form['email']

    for row in users:
        if(login == row[0]):
            flash('Данное имя пользователя уже зарегисрировано!')
            conn.commit()
            conn.close()
            return render_template('registration.html', otv = 'Данное имя пользователя уже зарегисрировано!')

    for row in emails:
        if(email == row[0]):
            flash('Данный почтовый адрес уже зарегисрирован!')
            conn.commit()
            conn.close()
            return render_template('registration.html', otv = 'Данный почтовый адрес уже зарегисрирован!')

    if len(password) < 6:
        conn.commit()
        conn.close()
        return render_template('registration.html', otv = 'Слишком короткий пароль! Пароль от 6 символов!')


    cookie = genCookie()


    conn.execute("INSERT INTO users (user_name, password, email, curCookie) VALUES (?, ?, ?, ?)",
            (login, hPass, email, cookie))

    conn.commit()
    conn.close()


    return render_template('registration.html', otv = 'Регистрация прошла успешно!')





#Создание новой последовательности
@app.route('/create', methods = ["GET"])
def createGET():
    """This HTML of the main idea of this project.
    GET method does nothing except renders the 'create.html' page.
    <br>User needs to enter LKG parameters such as values of a, m, c and number of digits in sequence</br>
    <br>Parameters can be any natural numbers.</br>
    <br>But for better digits in sequence (for sequrity reasons - for better random) parameters must satisfy the following conditions:</br>
    <br>C must be coprime with M.</br>
    <br>B must be a multiple of P for every prime P that is a divisor of M.</br>
    <br>B is a multiple of 4 if M is a multiple of 4.</br>
    ---
    tags:
      - Sequence creating page

    responses:
      200:
        description: No response just renders create page
        schema:
          $ref: '/create'
    """
    if not 'user' in session:
        return redirect(url_for('indexGET'))

    return render_template('create.html')

@app.route('/create', methods = ["POST"])
def createPOST():
    """This is the user registration page.
    POST method does next:
    1) Reads the data from fields of values.
    2) Generates sequenc by provided parameters.
    3) Writes it to the DB.
    4) Prints is on the page.

    ---
    tags:
      - Sequence creating page
    parameters:
      - name: Value a
        in: path
        type: integer
        required: true
        default: "none default value"
        description: Login which user must create. Must be unique in DB.

      - name: Value c
        in: path
        type: integer
        required: true
        default: "none default value"
        description: Any natural. But better if C is coprime with M.

      - name: Value m
        in: path
        type: integer
        required: true
        default: "none default value"
        description: Any natural. B = A - 1 better be a multiple of 4 if M is a multiple of 4.


      - name: Number of digits in the sequence
        in: path
        type: integer
        required: true
        default: "none default value"
        description: Can be any natural, but better if min value is 10.


    responses:
      200:
        description: <br>Just renders 'create' web-page with some assertions.</br>New page also contains saved sequence with parameters.
        schema:
          $ref: '/create'
    """
    intA = 1
    intC = 1
    intM = 1
    intNum = 10

    if (request.form['ButtonEnter'] == "Generate"):
        intA = 2
        while intA >= intM:
            intM = randint(6000, 65336)
            intC = randint(1, 65330)
            while (math.gcd(intC,intM) != 1):
                intC = randint(1, intM - 1)

            intB = 1

            for i in range(intM - 1, 1, -1):
                is_simple = 0
                if (intM % i == 0):
                    for j in range(i - 1, 1, -1):
                        if (i % j == 0):
                            is_simple = is_simple + 1
                    if (is_simple == 0):
                        intB = intB * i

            if(intM % 4 == 0 and intB % 4 != 0):
                intB = intB * 4
            intA = intB + 1


        return render_template('create.html', var_a = intA,
                var_c = intC, var_m = intM, var_num = intNum)

    if (request.form['ButtonEnter'] == "Enter"):

        arrayNames = ['значение a', 'значение c',
                            'значение m', 'Количество чисел для генерации']
        assertArray = []
        assertArray = [request.form['Param_a'], request.form['Param_c'],
                            request.form['Param_m'], request.form['Param_num']]


        index = 0
        boolCheck = False

        print("assertArray = ", assertArray)
        for value in assertArray:
            if value == '':
                flash('Параметр \'' + arrayNames[index] + '\' пуст!')
                boolCheck = True
            else:
                if index == 0: intA = int(assertArray[0])
                if index == 1: intC = int(assertArray[1])
                if index == 2: intM = int(assertArray[2])
                if index == 3: intNum = int(assertArray[3])

            index = index + 1


        if boolCheck:
            return render_template('create.html', var_a = intA,
                var_c = intC, var_m = intM, var_num = intNum)
        b = intA - 1

        if math.gcd(intC,intM) != 1:
            flash('с и m не взаимно простые!')
            #return render_template('create.html')

        boolWasPrint = False
        # print(f"\t[+] boolWasPrint = False")
        for i in range(intM - 1, 1, -1):
            is_simple = 0
            if (intM % i == 0):
                for j in range(i - 1, 1, -1):
                    if (i % j == 0):
                        is_simple = is_simple + 1
                if (is_simple == 0):
                    if b % i != 0:
                        if boolWasPrint == False:
                            flash('m имеет простой делитель, не кратный b = a-1!')
                            boolWasPrint = True
                       # return render_template('power.html')

        if (intM % 4 == 0 and b % 4 != 0) or (intM % 4 != 0 and b % 4 == 0):
            flash('если m кратно 4, b = a-1 тоже должно быть кратно 4 (и наоборот)!')
          #  return render_template('create.html')

        X = arr.array('i')
        xx = randint(1, intM)

        X.append((intA * xx + intC)%intM)
        for i in range(1, intNum):
            X.append((intA * X[i-1] + intC)%intM)

        posl = ''
        for i in range(0, intNum-1):
            posl = posl + str(X[i]) + ' '

        posl = posl + str(X[intNum-1])


        CuserCook = session.get('user', None)
        conn = get_db_connection('usersDB.db')
        Cuser = conn.execute('SELECT user_name FROM users WHERE curCookie = ?;', [CuserCook]).fetchall()
        Cuser = Cuser[0][0]
        Cuser = str(Cuser)
        conn.close()

        conn = get_db_connection('dataDB.db')
        conn.execute("INSERT INTO history (user_name, posledovatelnost, a, c, m) VALUES (?, ?, ?, ?, ?)",
            (Cuser, posl, intA, intC, intM))
        conn.commit()
        conn.close()
        return render_template('create.html', otv = 'Последовательность:\n' + posl + '\na = ' + str(intA) + '\nc = '+ str(intC) +'\nm = ' + str(intM))


#Функция нахождения пятого числа по четырём предыдущим.
@app.route('/oracle', methods = ["GET"])
def oracleGET():
    """Page provides the algorythm for predicting the 5-th element of sequence by 4 provided elements.
    GET method does nothing except renders the 'create.html' page.
    <br>User needs to enter 4 values of sequence.</br>
    ---
    tags:
      - Sequence checking page

    responses:
      200:
        description: No response just renders create page
        schema:
          $ref: '/oracle'
    """
    if not 'user' in session:
        return redirect(url_for('indexGET'))

    return render_template('oracle.html')

@app.route('/oracle', methods = ["POST"])
def oraclePOST():
    """This is the user registration page.
    POST method does next:
    1) Reads the data from fields of values.
    2) Generates sequenc by provided parameters.
    3) Writes it to the DB.
    4) Prints is on the page.

    ---
    tags:
      - Sequence checking page
    parameters:
      - name: Value a1
        in: path
        type: integer
        required: true
        default: "none default value"
        description: 1-st digit of sequence.

      - name: Value a2
        in: path
        type: integer
        required: true
        default: "none default value"
        description: 2-st digit of sequence.

      - name: Value a3
        in: path
        type: integer
        required: true
        default: "none default value"
        description: 3-st digit of sequence.

      - name: Value a4
        in: path
        type: integer
        required: true
        default: "none default value"
        description: 4-st digit of sequence.


    responses:
      200:
        description: Just renders 'oracle' web-page with result printing on the page.
        schema:
          $ref: '/oracle'
    """
    if request.method == 'POST':
        x1 = int(request.form['first'])
        x2 = int(request.form['second'])
        x3 = int(request.form['third'])
        x4 = int(request.form['forth'])

        x5 = oraculus(x1, x2, x3, x4)
        if x5 == 0:
            flash('Не получилось (вероятнее всего, параметр m в вашей последовательности больше 65336)!')
            return render_template('oracle.html')

        return render_template('oracle.html', x5=x5)


#Проверка периода.
@app.route('/period', methods = ["GET"])
def periodGET():
    """This HTML provides the algorythm for checking the period of the sequnce by values of a, c and m.
    GET method does nothing except renders the 'period.html' page.
    <br>User needs to enter 3 values: a, c and m.</br>
    ---
    tags:
      - Period checking page

    responses:
      200:
        description: No response just renders create page
        schema:
          $ref: '/oracle'
    """
    if not 'user' in session:
        return redirect(url_for('indexGET'))
    return render_template('period.html')


@app.route('/period', methods = ["POST"])
def periodPOST():
    """Period checking page.
    POST method does next:
    1) Reads entered values a, c and m.
    2) Checking the period parameter.
    3) Outputs the result on the same page as 'flash'.

    ---
    tags:
      - Period checking page
    parameters:
      - name: Value a
        in: path
        type: integer
        required: true
        default: "none default value"
        description: Value of a.

      - name: Value c
        in: path
        type: integer
        required: true
        default: "none default value"
        description: Value of c.

      - name: Value m
        in: path
        type: integer
        required: true
        default: "none default value"
        description: Value of m.


    responses:
      200:
        description: Renders 'period' page with result of checking the period.
        schema:
          $ref: '/period'
    """
    a = int(request.form['a'])
    c = int(request.form['c'])
    m = int(request.form['m'])
    b = a - 1

    if math.gcd(c,m) != 1:
        flash('с и m не взаимно простые!')
        #return render_template('period.html')

    for i in range(m - 1, 1, -1):
        is_simple = 0
        if (m % i == 0):
            for j in range(i - 1, 1, -1):
                if (i % j == 0):
                    is_simple = is_simple + 1
            if (is_simple == 0):
                if b % i != 0:
                    if boolWasPrint == False:
                        flash('m имеет простой делитель, не кратный b = a-1!')
                        boolWasPrint = True
                    #return render_template('power.html')

    if (m % 4 == 0 and b % 4 != 0) or (m % 4 != 0 and b % 4 == 0):
        flash('если m кратно 4, b = a-1 тоже должно быть кратно 4 (и наоборот)!')
        #return render_template('period.html')

    per = schet_period(a, c, m)
    if (per == m):
        otv = 'Период = ' + str(per) + '. Период ЛКГ с данными параметрами хороший, так как равен m.'
    elif (int(per) > (2 * m)):
        otv = 'Период слишком большой и не поддаётся рассчёту (должен быть равен m)!'
    else:
        otv = 'Период = ' + str(per) + '. Период ЛКГ с данными параметрами плохой, так как не равен m.'

    return render_template('period.html', otv=otv)


#Проверка мощности.
@app.route('/power', methods = ["GET"])
def powerGET():
    """This HTML provides the algorythm for checking the period of the sequnce by values of a, c and m.
    GET method does nothing except renders the 'period.html' page.
    <br>User needs to enter 3 values: a, c and m.</br>
    ---
    tags:
      - Power checking page

    responses:
      200:
        description: No response just renders create page
        schema:
          $ref: '/oracle'
    """
    if not 'user' in session:
        return redirect(url_for('indexGET'))
    return render_template('power.html')

@app.route('/power', methods = ["POST"])
def powerPOST():
    """Power checking page.
    POST method does next:
    1) Reads entered values a, c and m.
    2) Checking the Power parameter.
    3) Outputs the result on the same page as 'flash'.

    ---
    tags:
      - Power checking page
    parameters:
      - name: Value a
        in: path
        type: integer
        required: true
        default: "none default value"
        description: Value of a.

      - name: Value c
        in: path
        type: integer
        required: true
        default: "none default value"
        description: Value of c.

      - name: Value m
        in: path
        type: integer
        required: true
        default: "none default value"
        description: Value of m.


    responses:
      200:
        description: Renders 'period' page with result of checking the period.
        schema:
          $ref: '/period'
    """

    a = int(request.form['a'])
    c = int(request.form['c'])
    m = int(request.form['m'])
    b = a - 1

    if math.gcd(c,m) != 1:
        flash('с и m не взаимно простые!')
        #return render_template('power.html')

    for i in range(m - 1, 1, -1):
        is_simple = 0
        if (m % i == 0):
            for j in range(i - 1, 1, -1):
                if (i % j == 0):
                    is_simple = is_simple + 1
            if (is_simple == 0):
                if b % i != 0:
                    if boolWasPrint == False:
                        flash('m имеет простой делитель, не кратный b = a-1!')
                        boolWasPrint = True
                    # flash('m имеет простой делитель, не кратный b = a-1!')
                    #return render_template('power.html')

    if (m % 4 == 0 and b % 4 != 0) or (m % 4 != 0 and b % 4 == 0):
        flash('если m кратно 4, b = a-1 тоже должно быть кратно 4 (и наоборот)!')
       # return render_template('power.html')

    s = 0
    while ((b**s) % m != 0):
        s = s + 1

    if (s >= 5):
        otv = 'Мощность = ' + str(s) + '. ЛКГ с данными параметрами обладает хорошей мощностью.'
    else:
        otv = 'Мощность = ' + str(s) + '. ЛКГ с данными параметрами обладает плохой мощностью.'

    return render_template('power.html', otv=otv)



@app.route('/changeinfo', methods = ["GET"])
def changeinfoGET(needRet=False):
    """On this page user can chamge theirs login (username).
    GET method proceeds the DB query if needed or/and renders the 'changeinfo' web-page.
    <br>User just needs to enter new login.</br>
    <br>If new login does not exists - it will be updated.</br>
    ---
    tags:
      - Change login page

    responses:
      200:
        description: No response just renders changeinfo page or return the info to another function.
        schema:
          $ref: '/changeinfo'
    """
    if not 'user' in session:
        return redirect(url_for('indexGET'))

    CuserCook = session.get('user', None)
    conn = get_db_connection('usersDB.db')
    CuserInfo = conn.execute('SELECT user_name, email FROM users WHERE curCookie = ?;', [CuserCook]).fetchall()
    Cuser = CuserInfo[0][0]
    Cuser = str(Cuser)
    conn.close()

    if needRet:
        return Cuser, CuserCook
    else:
        return render_template('changeinfo.html', oldname = Cuser)



@app.route('/changeinfo', methods = ["POST"])
def changeinfoPOST():
    """On this page user can chamge theirs login (username).
    POST method does next:
    1) Reads entered login.
    2) Checks new login for presence in DB.
    3) If login does not presente - change old login to new.

    ---
    tags:
      - Change login page
    parameters:
      - name: New login
        in: path
        type: string
        required: true
        default: "none default value"
        description: The new login that the user wants to replace the previous one with.


    responses:
      200:
        description: Renders 'changeinfo' page with message of error or success result.
        schema:
          $ref: '/changeinfo'
    """

    Cuser, CuserCook = changeinfoGET(True)

    newname = str(request.form['uname'])
    print ("newname = ", newname)
    oldUserName = Cuser

    conn = get_db_connection('usersDB.db')
    CuserInfo = conn.execute('SELECT EXISTS(SELECT user_name FROM users WHERE user_name = ?);', [newname]).fetchall()
    conn.close()

    if CuserInfo[0][0]:
        return render_template('changeinfo.html', oldname = Cuser, otv = 'Данное имя уже занято!')



    conn = get_db_connection('usersDB.db')
    conn.execute("UPDATE users SET user_name = ? WHERE curCookie = ?", [newname, CuserCook])
    CuserInfo = conn.execute('SELECT user_name, email FROM users WHERE curCookie = ?;', [CuserCook]).fetchall()
    Cuser = CuserInfo[0][0]
    Cuser = str(Cuser)
    conn.commit()
    conn.close()
    print ("Cuser = ", Cuser)
    if not Cuser == newname:
        return render_template('changeinfo.html', oldname = Cuser, otv = 'Данное имя уже занято!')
    else:
        conn = get_db_connection('dataDB.db')
        conn.execute("UPDATE history SET user_name = ? WHERE user_name = ?", [Cuser, oldUserName])
        conn.commit()
        conn.close()

        return render_template('changeinfo.html', oldname = Cuser, otv = 'Имя успешно заменено!')



@app.route('/changepsw', methods = ["GET"])
def changepswGET():
    """On this page user can chamge theirs password.
    GET method just renders changepsw.html page.
    <br>User needs to enter new password which will not equal previous.</br>
    ---
    tags:
      - Change password page

    responses:
      200:
        description: No response just renders changepsw page
        schema:
          $ref: '/changepsw'
    """
    if not 'user' in session:
        return redirect(url_for('indexGET'))

    return render_template('changepsw.html')

@app.route('/changepsw', methods = ["POST"])
def changepswPOST():
    """On this page user can change theirs password.
    POST method does next:
    1) Reads entered password.
    2) Checks new password for equality with old password.
    3) If passwords are the same - the sustem will ask user for password re-enter.
    4) If passwords are not the same - the sustem will update the DB and re-render changepsw page with success message.

    ---
    tags:
      - Change password page
    parameters:
      - name: New password
        in: path
        type: string
        required: true
        default: "none default value"
        description: The new password that the user wants to replace the previous one with.


    responses:
      200:
        description: Renders 'changepsw' page with message of error or success result.
        schema:
          $ref: '/changepsw'
    """
    if request.method == 'POST':
        oldpsw = str(request.form['oldpsw'])
        newpsw = str(request.form['newpsw'])

        CuserCook = session.get('user', None)
        conn = get_db_connection('usersDB.db')
        CuserInfo = conn.execute('SELECT password FROM users WHERE curCookie = ?;', [CuserCook]).fetchall()
        CuserPass = CuserInfo[0][0]
        CuserPass = str(CuserPass)
        conn.close()

        oldpsw = sha1(oldpsw)
        newpsw = sha1(newpsw)

        if not CuserPass == oldpsw:
            return render_template('changepsw.html', otv = "Старый пароль введён ошибочно!")
        else:
            conn = get_db_connection('usersDB.db')
            conn.execute("UPDATE users SET password = ? WHERE curCookie = ?", [newpsw, CuserCook])
            conn.commit()
            conn.close()
            return render_template('changepsw.html', otv = "Пароль изменён успешно!")


@app.route('/forgpsw', methods = ["GET"])
def forgpswGET():
    """This page predicted for user password recover.
    GET method just renders forgpsw.html page.
    <br>User needs to enter his login and the mail for identity.</br>
    ---
    tags:
      - Restore password page

    responses:
      200:
        description: No response just renders forgpsw page
        schema:
          $ref: '/forgpsw'
    """
    return render_template('forgpsw.html')


@app.route('/forgpsw', methods = ["POST"])
def forgpswPOST():
    """On this page user can restore theirs password.
    POST method does next:
    1) Reads entered login and mail.
    2) Checks entered data for existing in DB.
    3) If user data presents in DB - new password will be sent to user's mail.
    4) If user data don't present in DB - the page will be re-rendered and user could enter correct data.

    ---
    tags:
      - Restore password page
    parameters:
      - name: User login
        in: path
        type: string
        required: true
        default: "none default value"
        description: String for user login value of the account wich password needs to be restored.

      - name: User mail
        in: path
        type: string
        required: true
        default: "none default value"
        description: String for user mail value of the account wich password needs to be restored.


    responses:
      200:
        description: Renders 'forgpsw' page with message of error or success result.
        schema:
          $ref: '/forgpsw'
    """

    login = str(request.form['uname'])
    email = str(request.form['email'])

    conn = get_db_connection('usersDB.db')
    CuserInfo = conn.execute('SELECT EXISTS(SELECT * FROM users WHERE user_name = ? AND email = ?);', [login, email]).fetchall()

    conn.close()

    if not CuserInfo[0][0]:
        return render_template('forgpsw.html', otv = 'Нет зарегестрированных пользователей с таким логином и адресом электронной почты!')

    newpass = send_for_forgpsw(email)
    hPass = sha1(newpass)

    print(newpass)
    print(hPass)

    conn = get_db_connection('usersDB.db')
    conn.execute("UPDATE users SET password = ? WHERE user_name = ?", [hPass, login])
    conn.commit()
    conn.close()

    return render_template('forgpsw.html', otv = 'Сообщение с новым паролем было направлено на вашу почту')


@app.route('/lk', methods = ["GET"])
def lkGET(infoGet = False):
    """This page predicted for user data printing and changing on the page.
    GET method renders reads all necessary data from the DB and pass it to the html page 'lk.html'.
    <br>There will be sequences history, user login and mail data printed on the page.</br>
    ---
    tags:
      - Personal account page

    responses:
      200:
        description: No response just renders lk page
        schema:
          $ref: '/lk'
    """

    if not 'user' in session:
        return redirect(url_for('indexGET'))

    CuserCook = session.get('user', None)

    conn = get_db_connection('usersDB.db')
    CuserInfo = conn.execute('SELECT user_name, email FROM users WHERE curCookie = ?;', [CuserCook]).fetchall()
    Cuser = CuserInfo[0][0]
    Cuser = str(Cuser)
    UserMail = CuserInfo[0][1]
    UserMail = str(UserMail)
    conn.close()

    conn = get_db_connection('dataDB.db')
    history = conn.execute('SELECT * FROM history WHERE user_name = ?', [Cuser]).fetchall()
    history.reverse()
    conn.close()

    if infoGet == False:
        return render_template('lk.html', uname = Cuser, email = UserMail, history=history)
    else:
        return Cuser, UserMail, history

@app.route('/lk', methods = ["POST"])
def lkPOST():
    """This page predicted for user data printing and changing on the page.
    POST method executes when it calls from html page. It calls when user press some button one the page - for example, when they press trash icon for sequence remove.
    ---
    tags:
      - Personal account page
    parameters:
      - name: Saved user sequences
        in: path
        type: table
        required: true
        default: "none default value"
        description: The table contains saved user sequences.

      - name: User login
        in: path
        type: string
        required: true
        default: "none default value"
        description: Immutable string for user login value.

      - name: User mail
        in: path
        type: string
        required: true
        default: "none default value"
        description: Immutable string for user mail value.


    responses:
      200:
        description: Renders 'lk' page with message of error or success result.
        schema:
          $ref: '/lk'
    """
    Cuser, UserMail, history = lkGET(True)

    pos = request.form['Posledovatelnost']
    a = int(request.form['Param_a'])
    c = int(request.form['Param_c'])
    m = int(request.form['Param_m'])

    conn = get_db_connection('dataDB.db')
    history = conn.execute('SELECT * FROM history WHERE user_name = ?', [Cuser]).fetchall()
    history.reverse()
    conn.close()

    conn = get_db_connection('dataDB.db')
    conn.execute('DELETE from history WHERE posledovatelnost = ? AND a = ? AND c = ? AND m = ?', [pos, a, c, m]).fetchall()
    history = conn.execute('SELECT * FROM history WHERE user_name = ?', [Cuser]).fetchall()
    history.reverse()
    conn.commit()
    conn.close()

    return render_template('lk.html', uname = Cuser, email = UserMail, history=history)




@app.route('/logout', methods = ["GET"])
def logoutGET():
    """This page predicted for confirmation user intent for logout.
    GET method renders logout page with 2 buttons.
    <br>There will be sequences history, user login and mail data printed on the page.</br>
    ---
    tags:
      - Logout intent confirmation page

    responses:
      200:
        description: No response just renders logout page
        schema:
          $ref: '/logout'
    """
    if not 'user' in session:
        return redirect(url_for('indexGET'))

    return render_template('logout.html')

@app.route('/logout', methods = ["POST"])
def logoutPOST():
    """This page predicted for confirmation user intent for logout.
    POST method drops user session (cookie) on button command and redirects to main (index) page.
    ---
    tags:
      - Logout intent confirmation page
    parameters:
      - name: Saved user sequences
        in: path
        type: table
        required: true
        default: "none default value"
        description: The table contains saved user sequences.

      - name: User login
        in: path
        type: string
        required: true
        default: "none default value"
        description: Immutable string for user login value.

      - name: User mail
        in: path
        type: string
        required: true
        default: "none default value"
        description: Immutable string for user mail value.


    responses:
      200:
        description: Renders 'logout' page with message of error or success result.
        schema:
          $ref: '/logout'
    """
    session.pop('user', None)
    session.pop('email', None)

    return redirect(url_for('indexGET'))