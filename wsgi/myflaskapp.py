from flask import Flask, request, jsonify, render_template

import database_driver

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world!', 200


@app.route('/userinfo/', methods=['POST'])
def post_userinfo():
    if 'phonenumber' not in request.form:
        return 'Missing phonenumber', 400
    current_info = database_driver.get_userinfo(request.form['phonenumber'])
    if current_info:
        return 'Data exist! make put request to entirely replace', 409
    result = database_driver.post_userinfo(request.form)
    if not result:
        return 'Illegal request', 400
    else:
        return 'Success', 201


@app.route('/userinfo/<phonenumber>', methods=['GET'])
def get_userinfo(phonenumber):
    info = database_driver.get_userinfo(phonenumber)
    if not phonenumber or not info:
        return 'Not found', 404
    return jsonify(info)


@app.route('/admin/login')
def admin_login():
    return render_template("admin_login.html")

@app.route('/admin_student_status.html',methods=['POST'])
def test():
	if('approve' not in request.form):
		data = request.form.get('decline')
		phno = data.split(":")[0]
		stat = data.split(":")[1]
		database_driver.post_status_userinfo(phno,stat)
		#pending = database_driver.get_students_info()
		return ('',204)
		
		
	elif('decline' not in request.form):
		data = request.form.get('approve')
		phno = data.split(":")[0]
		stat = data.split(":")[1]
		database_driver.post_status_userinfo(phno,stat)
		#pending = database_driver.get_students_info()
		return ('',204)
		
	
@app.route('/admin_student_status.html',methods=['GET'])
def admin_student_status():
    pending = database_driver.get_students_info()
    return render_template('admin_student_status.html', pending=pending)
if __name__ == '__main__':
    app.run(debug=True)
