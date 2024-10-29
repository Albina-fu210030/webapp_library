from flask import Flask, render_template, request, redirect, url_for
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
import sqlalchemy as sa
import pyodbc


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://albina:albinaalbina@SQL2017/library_albina?driver=SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
cache = Cache(app)
cache.clear()

class books(db.Model):
    __tablename__ = "books"
    id_book = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=True)
    author = Column(String(50), nullable=True)
    publication_date = Column(String(50), nullable=True)


class library(db.Model):
    __tablename__ = "library"
    id_library = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('books'))
    id_employee = Column(Integer, ForeignKey('employees'))
    library_name = Column(String(50), nullable=True)
    location = Column(String(50), nullable=True)
    working_hours = Column(Integer, nullable=True)
    LinkBooks = relationship('books', backref='library')
    LinkEmployees = relationship('employees', backref='library')


class employees(db.Model):
    __tablename__ = "employees"
    id_employee = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    role = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)


# Подключение к БД   
def connect_db(db_name):
    connect_str = "mssql+pyodbc://SQL2017/" + db_name + "?driver=SQL+Server"
    engine = sa.create_engine(connect_str, echo=False)
    Session = sessionmaker(bind=engine)
    return Session()


# Роут для отображения информации о библиотеке
@app.route('/')
def index():
    Книги = db.session.query(books).all()
    Библиотека = db.session.query(library).all()
    Сотрудники = db.session.query(employees).all()
    return render_template('index.html', Книги=Книги, Библиотека=Библиотека, Сотрудники=Сотрудники)

# Роут для отображения информации о библиотеке
@app.route('/index1.html')
def index1():
    Книги = db.session.query(books).all()
    Библиотека = db.session.query(library).all()
    Сотрудники = db.session.query(employees).all()
    return render_template('index1.html', Книги=Книги, Библиотека=Библиотека, Сотрудники=Сотрудники)

# Роут для отображения информации о библиотеке
@app.route('/index2.html')
def index2():
    Книги = db.session.query(books).all()
    Библиотека = db.session.query(library).all()
    Сотрудники = db.session.query(employees).all()
    return render_template('index2.html', Книги=Книги, Библиотека=Библиотека, Сотрудники=Сотрудники)

# Роут для отображения информации о библиотеке
@app.route('/index3.html')
def index3():
    Книги = db.session.query(books).all()
    Библиотека = db.session.query(library).all()
    Сотрудники = db.session.query(employees).all()
    return render_template('index3.html', Книги=Книги, Библиотека=Библиотека, Сотрудники=Сотрудники)


# Роут для добавления библиотеки
@app.route('/add1', methods = ['GET', 'POST'])
def add1():
    if request.method == 'POST':
        Таргет1_title = request.form['title']
        Таргет1_author = request.form['author']
        Таргет1_publication_date = request.form['publication_date']


        Таргет1 = books(title=Таргет1_title,
                        author=Таргет1_author,
                        publication_date=Таргет1_publication_date)
        db.session.add(Таргет1)
        db.session.commit()

    return redirect(url_for('index1'))

# Роут для добавления библиотеки
@app.route('/add2', methods = ['GET', 'POST'])
def add2():
    if request.method == 'POST':
        id_book = request.form['id_book']
        id_employee = request.form['id_employee']
        Таргет2_library_name = request.form['library_name']
        Таргет2_location = request.form['location']
        Таргет2_working_hours= request.form['working_hours']

        Таргет2 = library(
                                        id_book=id_book,
                                        id_employee=id_employee,
                                        library_name=Таргет2_library_name,
                                        location=Таргет2_location,
                                        working_hours=Таргет2_working_hours)
        db.session.add(Таргет2)
        db.session.commit()

    return redirect(url_for('index2'))

# Роут для добавления библиотеки
@app.route('/add3', methods = ['GET', 'POST'])
def add3():
    if request.method == 'POST':
        Таргет3_name = request.form['name']
        Таргет3_role = request.form['role']
        Таргет3_age= request.form['age']

        Таргет3 = employees(name=Таргет3_name,
                            role=Таргет3_role,
                            age=Таргет3_age)
        db.session.add(Таргет3)
        db.session.commit()

    return redirect(url_for('index3'))




# Роут для изменения библиотеки
@app.route('/alter1', methods = ['GET', 'POST'])
def alter1():
    if request.method == 'POST':
        id_book = int(request.values.get('id_book'))
        Таргет1_title = request.values.get('title')
        Таргет1_author = request.values.get('author')
        Таргет1_publication_date = request.values.get('publication_date')


        Таргет1 = db.session.query(books).get(id_book)

        if Таргет1.id_book != id_book:
            Таргет1.id_book = id_book
        if Таргет1.title != Таргет1_title:
            Таргет1.title = Таргет1_title
        if Таргет1.author != Таргет1_author:
            Таргет1.author = Таргет1_author
        if Таргет1.publication_date != Таргет1_publication_date:
            Таргет1.publication_date = Таргет1_publication_date

        db.session.commit()

    return redirect(url_for('index1'))



# Роут для изменения библиотеки
@app.route('/alter2', methods = ['GET', 'POST'])
def alter2():
    if request.method == 'POST':
        id_library = int(request.values.get('id_library'))
        id_book = request.values.get('id_book')
        id_employee = request.values.get('id_employee')
        Таргет2_library_name = request.values.get('library_name')
        Таргет2_location = request.values.get('location')
        Таргет2_working_hours = int(request.values.get('working_hours'))

        Таргет2 = db.session.query(library).get(id_library)

        if Таргет2.id_library != id_library:
            Таргет2.id_library = id_library
        if Таргет2.id_book != id_book:
            Таргет2.id_book = id_book
        if Таргет2.id_employee != id_employee:
            Таргет2.id_employee = id_employee
        if Таргет2.library_name != Таргет2_library_name:
            Таргет2.library_name = Таргет2_library_name
        if Таргет2.location != Таргет2_location:
            Таргет2.location = Таргет2_location
        if Таргет2.working_hours != Таргет2_working_hours:
            Таргет2.working_hours = Таргет2_working_hours

        db.session.commit()

    return redirect(url_for('index2'))



# Роут для изменения библиотеки
@app.route('/alter3', methods = ['GET', 'POST'])
def alter3():
    if request.method == 'POST':
        id_employee = int(request.values.get('id_employee'))
        Таргет3_name = request.values.get('name')
        Таргет3_role = request.values.get('role')
        Таргет3_age = int(request.values.get('age'))

        Таргет3 = db.session.query(employees).get(id_employee)

        if Таргет3.id_employee != id_employee:
            Таргет3.id_employee = id_employee
        if Таргет3.name != Таргет3_name:
            Таргет3.name = Таргет3_name
        if Таргет3.role != Таргет3_role:
            Таргет3.role = Таргет3_role
        if Таргет3.age != Таргет3_age:
            Таргет3.age = Таргет3_age

        db.session.commit()

    return redirect(url_for('index3'))





# Роут для удаления библиотеки
@app.route('/remove1', methods = ['GET', 'POST'])
def remove1():
    if request.method == 'POST':
        Таргет1_title = request.values.get('title')
        Таргет1_author = request.values.get('author')
        Таргет1_publication_date = int(request.values.get('publication_date'))

        db.session.query(books).filter(
                books.title == Таргет1_title,
                books.author == Таргет1_author,
                books.publication_date == Таргет1_publication_date).delete()
        db.session.commit()

    return redirect(url_for('index1'))

# Роут для удаления библиотеки
@app.route('/remove2', methods = ['GET', 'POST'])
def remove2():
    if request.method == 'POST':
        id_book = int(request.values.get('id_book'))
        id_employee = int(request.values.get('id_employee'))
        Таргет2_library_name = request.values.get('library_name')
        Таргет2_location = request.values.get('location')
        Таргет2_working_hours = int(request.values.get('working_hours'))

        db.session.query(library).filter(
            library.id_book == id_book,
            library.id_employee == id_employee,
            library.library_name == Таргет2_library_name,
            library.location == Таргет2_location,
            library.working_hours == Таргет2_working_hours).delete()
        db.session.commit()

    return redirect(url_for('index2'))

# Роут для удаления библиотеки
@app.route('/remove3', methods = ['GET', 'POST'])
def remove3():
    if request.method == 'POST':
        Таргет3_name = request.values.get('name')
        Таргет3_role = request.values.get('role')
        Таргет3_age = int(request.values.get('age'))

        db.session.query(employees).filter(
                    employees.name == Таргет3_name,
                    employees.role == Таргет3_role,
                    employees.age == Таргет3_age).delete()
        db.session.commit()

    return redirect(url_for('index3'))




if __name__ == '__main__':
    app.run(host="127.0.0.1", port = 9524, debug = True)
