import sqlite3 [cite: 56]
from flask import Flask, render_template, request, redirect, url_for [cite: 57]

app = Flask(__name__) [cite: 58, 59]
DB_NAME = "books.db" [cite: 60]

def connectdb(): [cite: 62]
    conn = sqlite3.connect(DB_NAME) [cite: 63]
    conn.row_factory = sqlite3.Row [cite: 64, 65]
    return conn [cite: 67]

def init_db(): [cite: 69]
    conn = connectdb() [cite: 72, 73]
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul VARCHAR(100) NOT NULL,
            penulis VARCHAR(100) NOT NULL
        )
    ''') [cite: 74, 78, 79, 80, 81]
    conn.commit() [cite: 84]
    conn.close() [cite: 85]

@app.route('/') [cite: 87]
def index(): [cite: 88]
    conn = connectdb() [cite: 89, 90]
    books = conn.execute("SELECT * FROM books").fetchall() [cite: 92, 93]
    conn.close() [cite: 95]
    return render_template("index.html", books=books) [cite: 97]

@app.route('/add', methods=['GET', 'POST']) [cite: 99]
def add(): [cite: 100]
    if request.method == "POST": [cite: 102]
        judul = request.form["judul"] [cite: 103, 104]
        penulis = request.form["penulis"] [cite: 106, 107]
        conn = connectdb() [cite: 109]
        conn.execute("INSERT INTO books (judul, penulis) VALUES (?, ?)", (judul, penulis)) [cite: 112]
        conn.commit() [cite: 113]
        conn.close() [cite: 115]
        return redirect(url_for('index')) [cite: 117]
    return render_template('add.html') [cite: 119]

@app.route('/edit/<int:id>', methods=['GET', 'POST']) [cite: 120]
def edit(id): [cite: 121]
    conn = connectdb() [cite: 125]
    book = conn.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone() [cite: 126]
    
    if not book: [cite: 126]
        return "Buku tidak ditemukan", 404 [cite: 127]
        
    if request.method == "POST": [cite: 128]
        judul = request.form["judul"] [cite: 129]
        penulis = request.form["penulis"] [cite: 130]
        conn.execute("UPDATE books SET judul = ?, penulis = ? WHERE id = ?", (judul, penulis, id)) [cite: 131]
        conn.commit() [cite: 132]
        conn.close() [cite: 133]
        return redirect(url_for('index')) [cite: 134]
    
    conn.close() [cite: 135]
    return render_template('edit.html', book=book) [cite: 162]

@app.route('/delete/<int:id>') [cite: 148]
def delete(id): [cite: 152]
    conn = connectdb() [cite: 153]
    conn.execute("DELETE FROM books WHERE id = ?", (id,)) [cite: 154]
    conn.commit() [cite: 156]
    conn.close() [cite: 158]
    return redirect(url_for('index')) [cite: 160]

if __name__ == '__main__': [cite: 164]
    init_db() [cite: 165]
    app.run(host='0.0.0.0', port=6001, debug=True) [cite: 167]