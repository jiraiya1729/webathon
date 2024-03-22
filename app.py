from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Update with your secret key
# firestrom 
cred = credentials.Certificate('credintials.json')
application = firebase_admin.initialize_app(cred)
db = firestore.client()
def get_document_id(email):
    # Query Firestore to find the document with the specified user ID
    query = db.collection("cities").where("email", "==", email).limit(1).get()
    # Iterate over the query results (there should be only one result due to limit(1))
    for doc in query:
        return doc.id  # Return the document ID of the first (and only) result
    return None


# app = firebase_admin.initialize_app()
# db = firestore.client()
def createdata(role ,name, email, number, course, college, gender, dob):
    data ={
        'role': role,
        'name': name,
        'email': email,
        'number': number,
        'course': course,
        'college': college,
        'gender': gender,
        'dob': dob,
    }
    print(data)
    new_doc_ref = db.collection('cities').document()
    new_doc_ref.set(data)
    
    
# Firebase configuration
config = {
    
    "apiKey": "AIzaSyDm1DJ9_38MPkVKEr7_6sYv6SXhgS3P4Uo",
    'authDomain': "authenticate-efe79.firebaseapp.com",
    'projectId': "authenticate-efe79",
    'storageBucket': "authenticate-efe79.appspot.com",
    'messagingSenderId': "238337435227",
    'appId': "1:238337435227:web:f6b78c0be18ab8de5a417e",
    'measurementId': "G-KKBWF4NR09",
    'databaseURL': ''
  
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def createlogin(email, password):
    pass

@app.route('/', methods=['GET'])
def home():
    if 'user' in session:
        # User is logged in, display a logout link
        return render_template('home.html', logged_in=True)
    else:
        # User is not logged in, display the default index.html
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            # Attempt authentication
            user = auth.sign_in_with_email_and_password(email, password)
            print("auth done")
            document_id = get_document_id(email)
            if document_id:
                return redirect(url_for('login_success', doc_id=document_id))
        except:
            return render_template('login.html', error="Invalid email or password.")
    return render_template('login.html')

@app.route('/login_success/<doc_id>')
def login_success(doc_id):
    # Use doc_id in the login_success route handler
    doc_ref = db.collection("cities").document(doc_id)

    doc = doc_ref.get()
    if doc.exists:
        user_data = doc.to_dict()
    else:
        print("No such document!")
        
    return render_template('login_success.html', user_data=user_data)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('login'))
        except:
            return render_template('signup.html', error="Registration failed.")
    return render_template('signup.html')

@app.route('/school_register',  methods=['GET', 'POST'])
def school_register():
    return render_template('school_register.html')


@app.route('/work_register')
def work_register():
    return render_template('work_register.html')

@app.route('/personal_register')
def personal_register():
    return render_template('personal_register.html')

@app.route('/trainer_register',  methods=['GET', 'POST'])
def trainer_register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        number = request.form['phone']
        course = "None"
        college = request.form['college']
        gender = request.form['gender']
        dob = request.form['dob']
        try:
            auth.create_user_with_email_and_password(email, password)
            createdata("trainer",name, email, number, course, college, gender, dob)
            return render_template('login.html')
        except:
            return " Failed to create account"

    return render_template('trainer_register.html')

@app.route('/trainee_register',  methods=['GET', 'POST'])
def trainee_register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        number = request.form['phone']
        course = request.form['preparationCourse']
        college = request.form['college']
        gender = request.form['gender']
        dob = request.form['dob']
        
        try:
            auth.create_user_with_email_and_password(email, password)
            createdata("trainee",name, email, number, course, college, gender, dob)
            return render_template('login.html')
        except:
            return " Failed to create account"
    return render_template('trainee_register.html')
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/Teacher_P_register',  methods=['GET', 'POST'])
def Teacher_P_register():
    if request.method == 'POST':
        
            name = request.form['name']
            password = request.form['password']
            email = request.form['email']
            number = request.form['phone']
            course = "None"
            college = request.form['college']
            gender = request.form['gender']
            dob = request.form['dob']
            try:
                print(email,password)
                auth.create_user_with_email_and_password(email, password)
                print("error")
                createdata("personal_teacher",name, email, number, course, college, gender, dob)
                
                return render_template('login.html')
            except:
                return " Failed to create account"
        
    return render_template('teacher_p_register.html')

@app.route('/Student_P_register',  methods=['GET', 'POST'])
def Student_P_register():
    if request.method == 'POST':
            print("entered")
            name = request.form['name']
            password = request.form['password']
            email = request.form['email']
            number = request.form['phone']
            course = request.form['preparationCourse']
            college = request.form['college']
            gender = request.form['gender']
            dob = request.form['dob']
            try:
                auth.create_user_with_email_and_password(email, password)
                createdata("personal_student",name, email, number, course, college, gender, dob)
                return render_template('login.html')
            except:
                return " Failed to create account"
            # print("done")
    return render_template('student_p_register.html')
if __name__ == '__main__':
    app.run(debug=True)
