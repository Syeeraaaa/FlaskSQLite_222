from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'identitas_secret_key_123'  # Untuk flash messages

def connect_db():
    """Fungsi untuk koneksi ke database SQLite"""
    conn = sqlite3.connect('identitas.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Fungsi untuk inisialisasi database"""
    conn = connect_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS identitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            nim TEXT NOT NULL,
            prodi TEXT NOT NULL,
            kelas TEXT NOT NULL,
            email TEXT,
            tanggal_lahir TEXT,
            alamat TEXT,
            no_hp TEXT,
            hobi TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.close()

def get_all_identitas():
    """Fungsi untuk mengambil semua data identitas dari database"""
    conn = connect_db()
    cursor = conn.execute("SELECT * FROM identitas ORDER BY nama")
    data = cursor.fetchall()
    conn.close()
    
    return data

def get_identitas_by_id(id):
    """Fungsi untuk mengambil data identitas berdasarkan ID"""
    conn = connect_db()
    cursor = conn.execute("SELECT * FROM identitas WHERE id = ?", (id,))
    data = cursor.fetchone()
    conn.close()
    
    return data

def add_identitas(data):
    """Fungsi untuk menambahkan data identitas baru"""
    conn = connect_db()
    try:
        conn.execute('''
            INSERT INTO identitas (nama, nim, prodi, kelas, email, tanggal_lahir, alamat, no_hp, hobi)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['nama'],
            data['nim'],
            data['prodi'],
            data['kelas'],
            data['email'],
            data['tanggal_lahir'],
            data['alamat'],
            data['no_hp'],
            data['hobi']
        ))
        conn.commit()
        success = True
    except Exception as e:
        print(f"Error: {e}")
        success = False
    finally:
        conn.close()
    
    return success

def update_identitas(id, data):
    """Fungsi untuk memperbarui data identitas"""
    conn = connect_db()
    try:
        conn.execute('''
            UPDATE identitas 
            SET nama = ?, nim = ?, prodi = ?, kelas = ?, email = ?, 
                tanggal_lahir = ?, alamat = ?, no_hp = ?, hobi = ?
            WHERE id = ?
        ''', (
            data['nama'],
            data['nim'],
            data['prodi'],
            data['kelas'],
            data['email'],
            data['tanggal_lahir'],
            data['alamat'],
            data['no_hp'],
            data['hobi'],
            id
        ))
        conn.commit()
        success = True
    except Exception as e:
        print(f"Error: {e}")
        success = False
    finally:
        conn.close()
    
    return success

def delete_identitas(id):
    """Fungsi untuk menghapus data identitas"""
    conn = connect_db()
    try:
        conn.execute("DELETE FROM identitas WHERE id = ?", (id,))
        conn.commit()
        success = True
    except Exception as e:
        print(f"Error: {e}")
        success = False
    finally:
        conn.close()
    
    return success

def calculate_age(tanggal_lahir):
    """Fungsi untuk menghitung usia berdasarkan tanggal lahir"""
    if not tanggal_lahir:
        return None
    
    try:
        birth_date = datetime.strptime(tanggal_lahir, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth_date.year
        
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
            
        return age
    except:
        return None

@app.route('/')
def index():
    """Route utama untuk menampilkan daftar identitas"""
    init_db()
    all_data = get_all_identitas()
    
    # Format data untuk ditampilkan
    formatted_data = []
    for row in all_data:
        data = dict(row)
        # Hitung usia
        data['usia'] = calculate_age(data.get('tanggal_lahir'))
        
        # Format tanggal lahir
        if data.get('tanggal_lahir'):
            try:
                tanggal_obj = datetime.strptime(data['tanggal_lahir'], '%Y-%m-%d')
                data['tanggal_lahir_formatted'] = tanggal_obj.strftime('%d %B %Y')
            except:
                data['tanggal_lahir_formatted'] = data['tanggal_lahir']
        
        formatted_data.append(data)
    
    return render_template('index.html', identitas_list=formatted_data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Route untuk menambahkan data identitas baru"""
    if request.method == 'POST':
        # Ambil data dari form
        data = {
            'nama': request.form['nama'],
            'nim': request.form['nim'],
            'prodi': request.form['prodi'],
            'kelas': request.form['kelas'],
            'email': request.form['email'],
            'tanggal_lahir': request.form['tanggal_lahir'],
            'alamat': request.form['alamat'],
            'no_hp': request.form['no_hp'],
            'hobi': request.form['hobi']
        }
        
        # Validasi data wajib
        if not data['nama'] or not data['nim'] or not data['prodi']:
            flash('Nama, NIM, dan Prodi wajib diisi!', 'error')
            return render_template('add.html', data=data)
        
        # Simpan ke database
        if add_identitas(data):
            flash('Data identitas berhasil ditambahkan!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Gagal menambahkan data!', 'error')
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Route untuk mengedit data identitas"""
    data = get_identitas_by_id(id)
    
    if not data:
        flash('Data tidak ditemukan!', 'error')
        return redirect(url_for('index'))
    
    data = dict(data)
    
    if request.method == 'POST':
        # Ambil data dari form
        updated_data = {
            'nama': request.form['nama'],
            'nim': request.form['nim'],
            'prodi': request.form['prodi'],
            'kelas': request.form['kelas'],
            'email': request.form['email'],
            'tanggal_lahir': request.form['tanggal_lahir'],
            'alamat': request.form['alamat'],
            'no_hp': request.form['no_hp'],
            'hobi': request.form['hobi']
        }
        
        # Validasi data wajib
        if not updated_data['nama'] or not updated_data['nim'] or not updated_data['prodi']:
            flash('Nama, NIM, dan Prodi wajib diisi!', 'error')
            return render_template('edit.html', data=updated_data, id=id)
        
        # Update ke database
        if update_identitas(id, updated_data):
            flash('Data identitas berhasil diperbarui!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Gagal memperbarui data!', 'error')
    
    return render_template('edit.html', data=data, id=id)

@app.route('/delete/<int:id>')
def delete(id):
    """Route untuk menghapus data identitas"""
    if delete_identitas(id):
        flash('Data identitas berhasil dihapus!', 'success')
    else:
        flash('Gagal menghapus data!', 'error')
    
    return redirect(url_for('index'))

@app.route('/about')
def about():
    """Halaman tentang aplikasi"""
    return render_template('index.html', about_page=True)

if __name__ == '__main__':
    print("Aplikasi Identitas Diri CRUD berjalan...")
    print("Buka browser dan akses: http://localhost:5000")
    print("Tekan Ctrl+C untuk menghentikan aplikasi")
    app.run(host='0.0.0.0', port=5000, debug=True)