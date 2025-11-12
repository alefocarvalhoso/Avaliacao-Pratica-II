from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sq

app = Flask(__name__)
PATH = 'fabrica.db'

def get_db():
    conn = sq.connect(PATH)
    conn.row_factory = sq.Row
    return conn

def init_db():
    db = get_db()
    with open('schema.sql', mode='r') as f:
        db.executescript(f.read())
    db.commit()
    db.close()

@app.route("/")
def index():
    db = get_db()
    alunos = db.execute('SELECT * FROM aluno').fetchall()
    db.close()
    return render_template('Index.html', alunos=alunos)
    
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        curso = request.form['curso']
        db = get_db()
        db.execute('INSERT INTO aluno (nome, idade, curso) VALUES (?, ?, ?)',
                   (nome, idade, curso))
        db.commit()
        db.close()
        return redirect(url_for('index'))
    return render_template('cadastro.html')

@app.route('/deletar/<int:id>', methods=['GET', 'POST'])
def deletar(id):
    db = get_db()
    aluno = db.execute('SELECT * FROM aluno WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        db.execute('DELETE FROM aluno WHERE id = ?', (id,))
        db.commit()
        db.close()
        return redirect(url_for('index'))

    db.close()
    return render_template('deletar.html', aluno=aluno)

if __name__ == '__main__':
    app.run(debug=True)
