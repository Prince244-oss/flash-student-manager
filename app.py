from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ************ DATABASE CONFIGURATION ***************
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # fixed key name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ************ MODEL DEFINITION ***************
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll = db.Column(db.String(100), nullable=False)
    student_class = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# ************ ROUTES ***************

@app.route('/')
def home():
    students = Student.query.all()
    return render_template('index.html', std=students)


# ➕ ADD STUDENT
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        student_class = request.form['class']
        email = request.form['email']

        new_student = Student(name=name, roll=roll, student_class=student_class, email=email)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('home'))
    
    return render_template('add.html')


# ✏️ UPDATE STUDENT
@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.roll = request.form['roll']
        student.student_class = request.form['class']
        student.email = request.form['email']

        db.session.commit()
        return redirect(url_for('home'))

    return render_template('update.html', student=student)


# 🗑️ DELETE STUDENT
@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('home'))


# ℹ️ ABOUT PAGE
@app.route('/about')
def about():
    return render_template('about.html')


# 📞 CONTACT PAGE
@app.route('/contact')
def contact():
    return render_template('contact.html')


# ************ MAIN ***************
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # creates DB tables if not present
    app.run(debug=True)
