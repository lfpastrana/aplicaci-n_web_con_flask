from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Libro

# Connect to Database and create database session
engine = create_engine('sqlite:///libros.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# landing page that will display all the books in our database
# This function will operate on the Read operation.
@app.route('/')
@app.route('/libros')
def mostrarLibros():
    libros = session.query(Libro).all()
    return render_template('libros.html', libros=libros)


# This will let us Create a new book and save it in our database
@app.route('/libros/nuevo/', methods=['GET', 'POST'])
def nuevoLibro():
    if request.method == 'POST':
        nuevoLibro = Libro(titulo=request.form['nombre'],
                       autor=request.form['autor'],
                       genero=request.form['genero'])
        session.add(nuevoLibro)
        session.commit()
        return redirect(url_for('mostrarLibros'))
    else:
        return render_template('nuevoLibro.html')


# This will let us Update our books and save it in our database
@app.route("/libros/<int:libro_id>/editar/", methods=['GET', 'POST'])
def editarLibro(libro_id):
    libroEditado = session.query(Libro).filter_by(id=libro_id).one()
    if request.method == 'POST':
        if request.form['nombre'] and request.form['autor'] and request.form['genero']:
            libroEditado.titulo = request.form['nombre']
            libroEditado.autor = request.form['autor']
            libroEditado.genero = request.form['genero']
            return redirect(url_for('mostrarLibros'))
    else:
        return render_template('editarLibro.html', libro=libroEditado)


# This will let us Delete our book
@app.route('/libros/<int:libro_id>/eliminar/', methods=['GET', 'POST'])
def eliminarLibro(libro_id):
    libroAEliminar = session.query(Libro).filter_by(id=libro_id).one()
    if request.method == 'POST':
        session.delete(libroAEliminar)
        session.commit()
        return redirect(url_for('mostrarLibros', libro_id=libro_id))
    else:
        return render_template('eliminarLibro.html', libro=libroAEliminar)

# agregado menu
@app.route('/nuestrahistoria')
def nuestrahistoria():
    return render_template("nuestrahistoria.html")

@app.route('/ayuda')
def ayuda():
    return render_template("ayuda.html")

if __name__ == '__main__':
    app.run(debug=True)