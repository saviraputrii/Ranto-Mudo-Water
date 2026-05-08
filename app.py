import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Ranto Mudo Water - Aplikasi Galon Isi Ulang",
    page_icon="💧💧",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

/* Background utama */
.stApp {
    background: linear-gradient(to bottom right, #caf0f8, #90e0ef);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0077b6, #023e8a);
}

/* Tulisan sidebar */
section[data-testid="stSidebar"] * {
    color: white;
}

/* Judul */
h1, h2, h3 {
    color: #023e8a;
}

/* Card metric */
div[data-testid="metric-container"] {
    background-color: white;
    border: 2px solid #00b4d8;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}

/* Form input */
div[data-testid="stForm"] {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}

/* Tombol */
.stButton > button {
    background: linear-gradient(90deg, #0096c7, #00b4d8);
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #023e8a, #0077b6);
    color: white;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
    padding: 10px;
}

/* Info Box */
.info-box {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border-left: 8px solid #0077b6;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("💧 Ranto Mudo Water")
menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Data Pelanggan",
        "Stok Galon",
        "Penjualan",
        "Pengantaran",
        "Tagihan",
        "Laporan"
    ]
)

# =========================
# DATABASE SEMENTARA
# =========================
if "pelanggan" not in st.session_state:
    st.session_state.pelanggan = pd.DataFrame(columns=[
        "Nama", "Alamat", "No HP"
    ])

if "penjualan" not in st.session_state:
    st.session_state.penjualan = pd.DataFrame(columns=[
        "Tanggal", "Pelanggan", "Jumlah", "Total"
    ])

if "pengantaran" not in st.session_state:
    st.session_state.pengantaran = pd.DataFrame(columns=[
        "Tanggal", "Pelanggan", "Status"
    ])

if "hutang" not in st.session_state:
    st.session_state.hutang = pd.DataFrame(columns=[
        "Pelanggan", "Jumlah Hutang"
    ])

if "stok_isi" not in st.session_state:
    st.session_state.stok_isi = 50

if "stok_kosong" not in st.session_state:
    st.session_state.stok_kosong = 20

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.title("💧 Dashboard💧")
    
    st.markdown("""
    <div class="info-box">
    <h3>📌 Informasi Usaha</h3>
    <p>
    Selamat datang di aplikasi manajemen usaha galon isi ulang.
    Aplikasi ini untuk pencatatan pelanggan, stok galon,
    transaksi penjualan, pengantaran,tagihan, serta laporan usaha.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Pelanggan", len(st.session_state.pelanggan))
    col2.metric("Stok Isi", st.session_state.stok_isi)
    col3.metric("Stok Kosong", st.session_state.stok_kosong)

    total_penjualan = st.session_state.penjualan["Total"].sum() \
        if not st.session_state.penjualan.empty else 0

    col4.metric("Total Penjualan", f"Rp {total_penjualan:,}")

    st.divider()

    if st.session_state.stok_isi < 10:
        st.warning("⚠️ Stok galon isi hampir habis!")

    if st.session_state.stok_kosong < 5:
        st.warning("⚠️ Stok galon kosong menipis!")

# =========================
# DATA PELANGGAN
# =========================
elif menu == "Data Pelanggan":

    st.title("👥 Data Pelanggan")

    with st.form("form_pelanggan"):
        nama = st.text_input("Nama")
        alamat = st.text_input("Alamat")
        hp = st.text_input("No HP")

        submit = st.form_submit_button("Tambah Pelanggan")

        if submit:
            data_baru = pd.DataFrame([{
                "Nama": nama,
                "Alamat": alamat,
                "No HP": hp
            }])

            st.session_state.pelanggan = pd.concat(
                [st.session_state.pelanggan, data_baru],
                ignore_index=True
            )

            st.success("Pelanggan berhasil ditambahkan!")

    st.dataframe(st.session_state.pelanggan, use_container_width=True)

# =========================
# STOK GALON
# =========================
elif menu == "Stok Galon":

    st.title("📦 Stok Galon")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Galon Isi")
        tambah_isi = st.number_input(
            "Tambah Stok Isi",
            min_value=0,
            step=1
        )

        if st.button("Tambah Stok Isi"):
            st.session_state.stok_isi += tambah_isi
            st.success("Stok isi berhasil ditambah")

    with col2:
        st.subheader("Galon Kosong")
        tambah_kosong = st.number_input(
            "Tambah Stok Kosong",
            min_value=0,
            step=1
        )

        if st.button("Tambah Stok Kosong"):
            st.session_state.stok_kosong += tambah_kosong
            st.success("Stok kosong berhasil ditambah")

    st.divider()

    st.metric("Total Stok Isi", st.session_state.stok_isi)
    st.metric("Total Stok Kosong", st.session_state.stok_kosong)

# =========================
# PENJUALAN
# =========================
elif menu == "Penjualan":

    st.title("💰 Penjualan")

    pelanggan_list = (
        st.session_state.pelanggan["Nama"].tolist()
        if not st.session_state.pelanggan.empty
        else []
    )

    with st.form("form_penjualan"):

        pelanggan = st.selectbox(
            "Pilih Pelanggan",
            pelanggan_list
        )

        jumlah = st.number_input(
            "Jumlah Galon",
            min_value=1,
            step=1
        )

        harga = st.number_input(
            "Harga per Galon",
            min_value=0,
            step=1000
        )

        submit_jual = st.form_submit_button("Simpan Penjualan")

        if submit_jual:

            total = jumlah * harga

            data_jual = pd.DataFrame([{
                "Tanggal": datetime.now().strftime("%Y-%m-%d"),
                "Pelanggan": pelanggan,
                "Jumlah": jumlah,
                "Total": total
            }])

            st.session_state.penjualan = pd.concat(
                [st.session_state.penjualan, data_jual],
                ignore_index=True
            )

            st.session_state.stok_isi -= jumlah
            st.session_state.stok_kosong += jumlah

            st.success("Penjualan berhasil disimpan!")

    st.dataframe(st.session_state.penjualan, use_container_width=True)

# =========================
# PENGANTARAN
# =========================
elif menu == "Pengantaran":

    st.title("🚚 Riwayat Pengantaran")

    pelanggan_list = (
        st.session_state.pelanggan["Nama"].tolist()
        if not st.session_state.pelanggan.empty
        else []
    )

    with st.form("form_pengantaran"):

        pelanggan = st.selectbox(
            "Pelanggan",
            pelanggan_list
        )

        status = st.selectbox(
            "Status",
            ["Diproses", "Dikirim", "Selesai"]
        )

        submit_antar = st.form_submit_button("Tambah Pengantaran")

        if submit_antar:

            data_antar = pd.DataFrame([{
                "Tanggal": datetime.now().strftime("%Y-%m-%d"),
                "Pelanggan": pelanggan,
                "Status": status
            }])

            st.session_state.pengantaran = pd.concat(
                [st.session_state.pengantaran, data_antar],
                ignore_index=True
            )

            st.success("Data pengantaran berhasil ditambahkan!")

    st.dataframe(st.session_state.pengantaran, use_container_width=True)

# =========================
# TAGIHAN
# =========================
elif menu == "Tagihan":

    st.title("📝 Tagihan 💸")

    pelanggan_list = (
        st.session_state.pelanggan["Nama"].tolist()
        if not st.session_state.pelanggan.empty
        else []
    )

    with st.form("form_tagihan"):

        pelanggan = st.selectbox(
            "Pelanggan",
            pelanggan_list
        )

        jumlah_tagihan = st.number_input(
            "Jumlah Tagihan",
            min_value=0,
            step=1000
        )

        submit_tagihan = st.form_submit_button("Tambah Tagihan")

        if submit_tagihan:

            data_hutang = pd.DataFrame([{
                "Pelanggan": pelanggan,
                "Jumlah tagihan": jumlah_tagihan
            }])

            st.session_state.hutang = pd.concat(
                [st.session_state.hutang, data_tagihan],
                ignore_index=True
            )

            st.success("Data tagihan berhasil ditambahkan!")

    st.dataframe(st.session_state.hutang, use_container_width=True)

# =========================
# LAPORAN
# =========================
elif menu == "Laporan":

    st.title("📊 Laporan")

    total_penjualan = st.session_state.penjualan["Total"].sum() \
        if not st.session_state.penjualan.empty else 0

    total_transaksi = len(st.session_state.penjualan)

    total_hutang = st.session_state.hutang["Jumlah Hutang"].sum() \
        if not st.session_state.hutang.empty else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Penjualan", f"Rp {total_penjualan:,}")
    col2.metric("Jumlah Transaksi", total_transaksi)
    col3.metric("Total Hutang", f"Rp {total_hutang:,}")

    st.divider()

    st.subheader("Data Penjualan")
    st.dataframe(st.session_state.penjualan, use_container_width=True)
