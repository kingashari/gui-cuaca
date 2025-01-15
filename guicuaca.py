import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Daftar URL BMKG berdasarkan provinsi
PROVINCES = {
    'Aceh'              : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/11',
    'Sumatra Utara'     : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/12',
    'Sumatra Barat'     : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/13',
    'Riau'              : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/14',
    'Jambi'             : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/15',
    'Sumatra Selatan'   : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/16',
    'Bengkulu'          : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/17',
    'Lampung'           : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/18',
    'Bangka Belitung'   : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/19',
    'Kepulauan Riau'    : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/21',
    'DKI Jakarta'       : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/31',
    'Jawa Barat'        : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/32',
    'Jawa Tengah'       : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/33',
    'Yogyakarta'        : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/34',
    'Jawa Timur'        : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/35',
    'Banten'            : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/36',
    'Bali'              : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/51',
    'NTB'               : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/52',
    'NTT'               : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/53',
    'Kalimantan Barat'  : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/61',
    'Kalimantan Tengah' : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/62',
    'Kalimantan Selatan': 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/63',
    'Kalimantan Timur'  : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/64',
    'Kalimantan Utara'  : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/65',
    'Sulawesi Utara'    : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/71',
    'Sulawesi Tengah'   : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/72',
    'Sulawesi Selatan'  : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/73',
    'Sulawesi Tenggara' : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/74',
    'Gorontalo'         : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/75',
    'Sulawesi Barat'    : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/76',
    'Maluku'            : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/81',
    'Maluku Utara'      : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/82',
    'Papua'             : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/91',
    'Papua Barat'       : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/92',
    'Papua Selatan'     : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/93',
    'Papua Tengah'      : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/94',
    'Papua Pegunungan'  : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/95',
    'Papua Barat Daya'  : 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca/96',
}


# Fungsi untuk scraping data cuaca dari BMKG
def scrape_bmkg_weather(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table:
            raise Exception("Tabel cuaca tidak ditemukan di halaman.")
        
        data = []
        rows = table.find_all('tr')
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 4:
                wilayah = cols[0].text.strip()
                cuaca = cols[1].text.strip()
                data.append([wilayah, cuaca,])
        
        return data
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Permintaan gagal: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Kesalahan saat scraping: {e}")
    return None

# Fungsi untuk menampilkan data di tabel GUI
def show_weather():
    province = province_combobox.get()
    if not province:
        messagebox.showwarning("Peringatan", "Pilih provinsi terlebih dahulu!")
        return
    
    url = PROVINCES.get(province)
    if not url:
        messagebox.showerror("Error", "URL untuk provinsi ini tidak tersedia.")
        return
    
    data = scrape_bmkg_weather(url)
    if data:
        populate_table(data)

# Fungsi untuk mengisi tabel dengan data cuaca
def populate_table(data):
    for row in weather_table.get_children():
        weather_table.delete(row)
    
    for entry in data:
        weather_table.insert("", tk.END, values=entry)

# Fungsi untuk menyimpan data ke dalam format CSV
def save_to_csv():
    if not weather_table.get_children():
        messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    data = []
    for row in weather_table.get_children():
        data.append(weather_table.item(row)['values'])

    df = pd.DataFrame(data, columns=["Wilayah", "Cuaca"])
    try:
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Sukses", f"Data berhasil disimpan di {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan data: {e}")

# GUI Utama
root = tk.Tk()
root.title("Pengunduh Data Cuaca BMKG")
root.geometry("700x500")

# Dropdown untuk memilih provinsi
province_label = tk.Label(root, text="Pilih Provinsi:", font=("Arial", 12))
province_label.pack(pady=5)

province_combobox = ttk.Combobox(root, values=list(PROVINCES.keys()), font=("Arial", 12))
province_combobox.pack(pady=5)
province_combobox.set('...')

# Tombol untuk menampilkan cuaca
show_weather_button = tk.Button(root, text="Tampilkan Cuaca", font=("Arial", 12), command=show_weather)
show_weather_button.pack(pady=10)

# Tabel untuk menampilkan data cuaca
weather_table = ttk.Treeview(root, columns=("Wilayah", "Cuaca"), show='headings')
weather_table.heading("Wilayah", text="Wilayah")
weather_table.heading("Cuaca", text="Cuaca")
weather_table.pack(pady=10, fill=tk.BOTH, expand=True)

# Tombol untuk menyimpan data ke dalam format CSV
save_csv_button = tk.Button(root, text="Simpan ke CSV", font=("Arial", 12), command=save_to_csv)
save_csv_button.pack(pady=10)

root.mainloop()
