import streamlit as st
import pandas as pd
from datetime import datetime

# =========================
# LOGIN ADMIN
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

USERNAME = "admin"
PASSWORD = "air123"

if not st.session_state.login:

    st.title("🔐 Login Admin")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == USERNAME and password == PASSWORD:
            st.session_state.login = True
            st.success("Login berhasil!")
            st.rerun()

        else:
            st.error("Username atau password salah!")
  
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
        "Tagihan",
        "Laporan",
        "Pendapatan Bulanan",
    ]
)

# =========================
# DATABASE SEMENTARA
# =========================
if "pelanggan" not in st.session_state:
    st.session_state.pelanggan = pd.DataFrame(columns=[
        "Nama", "Alamat", "No HP"
    ])
if "stok_air_kosong" not in st.session_state:
    st.session_state.stok_air_kosong = 30
    
if "penjualan" not in st.session_state:
    st.session_state.penjualan = pd.DataFrame(columns=[
        "Tanggal", "Pelanggan", "Jenis", "Jumlah", "Total"
    ])

if "hutang" not in st.session_state:
    st.session_state.hutang = pd.DataFrame(columns=[
        "Pelanggan", "Jumlah Hutang"
    ])

# =========================
# 🫧STOK GALON KOSONG
# =========================
if "stok_aqua_isi" not in st.session_state:
    st.session_state.stok_aqua_isi = 50

if "stok_aqua_kosong" not in st.session_state:
    st.session_state.stok_aqua_kosong = 20

if "stok_leminerale_isi" not in st.session_state:
    st.session_state.stok_leminerale_isi = 40

if "stok_leminerale_kosong" not in st.session_state:
    st.session_state.stok_leminerale_kosong = 15

if "stok_air_isi_ulang" not in st.session_state:
    st.session_state.stok_air_isi_ulang = 1520

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.title("💧 Dashboard💧")
    st.markdown("""
<div style="
background-color:#f5f7fa;
padding:25px;
border-radius:15px;
box-shadow:0 4px 10px rgba(0,0,0,0.1);
">

<h2 style="color:#1f4e79;">📌 Informasi Usaha</h2>

<p style="text-align:justify; font-size:16px; color:#333333;">

Selamat datang di <b>Ranto Mudo Water</b>, aplikasi manajemen  air galon isi ulang yang dirancang untuk membantu proses operasional usaha menjadi efisien dan terorganisir. Sistem ini dikembangkan untuk mempermudah pengelolaan data pelanggan, monitoring stok galon, pencatatan transaksi penjualan, pengelolaan tagihan, hingga penyusunan laporan usaha secara otomatis dalam satu platform.

</p>

<p style="text-align:justify; font-size:16px; color:#333333;">

Dengan tampilan yang sederhana namun profesional, aplikasi ini membantu meningkatkan efisiensi pelayanan, meminimalkan kesalahan pencatatan data, serta mempermudah pemilik usaha dalam memantau kondisi bisnis secara real-time. Seluruh informasi tersusun secara rapi sehingga proses pengambilan keputusan dapat dilakukan dengan lebih cepat, tepat, dan akurat.

</p>

<p style="text-align:justify; font-size:16px; color:#333333;">

Melalui sistem digital berbasis <b>Streamlit</b>, pengelolaan depot air minum isi ulang dapat dilakukan dengan lebih praktis, aman, dan mudah diakses kapan saja sesuai kebutuhan operasional usaha.

</p>

</div>
""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Pelanggan",
        len(st.session_state.pelanggan)
    )

    col2.metric(
        "Aqua Isi",
        st.session_state.stok_aqua_isi
    )

    col3.metric(
        "Le Minerale Isi",
        st.session_state.stok_leminerale_isi
    )

    total_penjualan = (
        st.session_state.penjualan["Total"].sum()
        if not st.session_state.penjualan.empty
        else 0
    )

    col4.metric(
        "Total Penjualan",
        f"Rp {total_penjualan:,}"
    )

    st.divider()

    # INFO STOK
    st.subheader("📦 Informasi Stok")

    st.write(
        f"🟦 Aqua Kosong : {st.session_state.stok_aqua_kosong}"
    )

    st.write(
        f"🟩 Le Minerale Kosong : {st.session_state.stok_leminerale_kosong}"
    )

    st.write(
        f"💧 Air Isi Ulang : {st.session_state.stok_air_isi_ulang} Liter"
    )

    # WARNING
    if st.session_state.stok_aqua_isi < 10:
        st.warning("⚠️ Stok Aqua isi hampir habis!")

    if st.session_state.stok_leminerale_isi < 10:
        st.warning("⚠️ Stok Le Minerale isi hampir habis!")

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

    # Tampilkan data pelanggan
    st.dataframe(
        st.session_state.pelanggan,
        use_container_width=True
    )

    st.divider()

    # =========================
    # HAPUS DATA PELANGGAN
    # =========================
    st.subheader("🗑️ Hapus Data Pelanggan")

    if not st.session_state.pelanggan.empty:

        pelanggan_hapus = st.selectbox(
            "Pilih pelanggan yang akan dihapus",
            st.session_state.pelanggan["Nama"]
        )

        if st.button("Hapus Pelanggan"):

            st.session_state.pelanggan = (
                st.session_state.pelanggan[
                    st.session_state.pelanggan["Nama"] != pelanggan_hapus
                ]
            )

            st.success(
                f"Data pelanggan '{pelanggan_hapus}' berhasil dihapus!"
            )

    else:
        st.info("Belum ada data pelanggan.")

# =========================
# STOK GALON
# =========================
elif menu == "Stok Galon":

    st.title("📦 Stok Galon")

    # =========================
    # AQUA
    # =========================
    st.subheader("AQUA")

    col1, col2 = st.columns(2)

    with col1:
        tambah_aqua_isi = st.number_input(
            "Tambah Stok Aqua Isi",
            min_value=0,
            step=1
        )

        if st.button("Tambah Aqua Isi"):
            st.session_state.stok_aqua_isi += tambah_aqua_isi
            st.success("Stok Aqua isi berhasil ditambah")

    with col2:
        tambah_aqua_kosong = st.number_input(
            "Tambah Stok Aqua Kosong",
            min_value=0,
            step=1
        )

        if st.button("Tambah Aqua Kosong"):
            st.session_state.stok_aqua_kosong += tambah_aqua_kosong
            st.success("Stok Aqua kosong berhasil ditambah")

    st.divider()

    # =========================
    # LE MINERALE
    # =========================
    st.subheader("LE MINERALE")

    col3, col4 = st.columns(2)

    with col3:
        tambah_leminerale_isi = st.number_input(
            "Tambah Stok Le Minerale Isi",
            min_value=0,
            step=1
        )

        if st.button("Tambah Le Minerale Isi"):
            st.session_state.stok_leminerale_isi += tambah_leminerale_isi
            st.success("Stok Le Minerale isi berhasil ditambah")

    with col4:
        tambah_leminerale_kosong = st.number_input(
            "Tambah Stok Le Minerale Kosong",
            min_value=0,
            step=1
        )

        if st.button("Tambah Le Minerale Kosong"):
            st.session_state.stok_leminerale_kosong += tambah_leminerale_kosong
            st.success("Stok Le Minerale kosong berhasil ditambah")

    st.divider()

    # =========================
    # AIR ISI ULANG
    # =========================
    st.subheader("💧 Air Isi Ulang")

    tambah_air = st.number_input(
        "Tambah Stok Air Isi Ulang (Liter)",
        min_value=0,
        step=10
    )

    if st.button("Tambah Air Isi Ulang"):
        st.session_state.stok_air_isi_ulang += tambah_air
        st.success("Stok air isi ulang berhasil ditambah")

    col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Stok Air Isi Ulang",
        f"{st.session_state.stok_air_isi_ulang} L"
    )

with col2:

    total_isi_ulang = (
        st.session_state.penjualan[
            st.session_state.penjualan["Jenis"] == "ISI ULANG"
        ]["Jumlah"].sum()
        if not st.session_state.penjualan.empty
        else 0
    )

    liter_terjual = total_isi_ulang * 19

    st.metric(
        "Air Isi Ulang Terjual",
        f"{liter_terjual} L"
    )

    

    # =========================
    # TOTAL STOK
    # =========================
    st.metric("Aqua Isi", st.session_state.stok_aqua_isi)
    st.metric("Aqua Kosong", st.session_state.stok_aqua_kosong)

    st.metric("Le Minerale Isi", st.session_state.stok_leminerale_isi)
    st.metric("Le Minerale Kosong", st.session_state.stok_leminerale_kosong)
    
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

        jenis_galon = st.selectbox(
            "Galon yang Dibeli",
            [
                "AQUA",
                "LE MINERALE",
                "ISI ULANG"
            ]
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

        submit_jual = st.form_submit_button(
            "Simpan Penjualan"
        )

        if submit_jual:

            total = jumlah * harga

            data_jual = pd.DataFrame([{
                "Tanggal": datetime.now().strftime("%Y-%m-%d"),
                "Pelanggan": pelanggan,
                "Jenis": jenis_galon,
                "Jumlah": jumlah,
                "Total": total
            }])

            st.session_state.penjualan = pd.concat(
                [st.session_state.penjualan, data_jual],
                ignore_index=True
            )

            # UPDATE STOK
            if jenis_galon == "AQUA":

                st.session_state.stok_aqua_isi -= jumlah
                st.session_state.stok_aqua_kosong += jumlah

            elif jenis_galon == "LE MINERALE":

                st.session_state.stok_leminerale_isi -= jumlah
                st.session_state.stok_leminerale_kosong += jumlah

            elif jenis_galon == "ISI ULANG":

                st.session_state.stok_air_isi_ulang -= (
                    jumlah * 19
                )

                st.session_state.stok_air_kosong += jumlah

            st.success("Penjualan berhasil disimpan!")

    st.dataframe(
        st.session_state.penjualan,
        use_container_width=True
    )
    
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
                "Jumlah Hutang": jumlah_tagihan
            }])

            st.session_state.hutang = pd.concat(
                [st.session_state.hutang, data_hutang],
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
    col3.metric("Total Tagihan", f"Rp {total_hutang:,}")

    st.divider()

# =========================
# PENDAPATAN BULANAN
# =========================
elif menu == "Pendapatan Bulanan":

    st.title("📆 Pendapatan Bulanan")

    if not st.session_state.penjualan.empty:

        # Copy data penjualan
        df_penjualan = st.session_state.penjualan.copy()

        # Ubah kolom tanggal menjadi datetime
        df_penjualan["Tanggal"] = pd.to_datetime(
            df_penjualan["Tanggal"]
        )

        # Ambil format bulan dan tahun
        df_penjualan["Bulan"] = (
            df_penjualan["Tanggal"]
            .dt.strftime("%B %Y")
        )

        # Hitung total pendapatan per bulan
        pendapatan_bulanan = (
            df_penjualan.groupby("Bulan")["Total"]
            .sum()
            .reset_index()
        )

        # Total seluruh pendapatan
        total_bulanan = pendapatan_bulanan["Total"].sum()

        # Tampilkan total
        st.metric(
            "Total Pendapatan",
            f"Rp {total_bulanan:,}"
        )

        st.divider()

        # Tabel pendapatan bulanan
        st.dataframe(
            pendapatan_bulanan,
            use_container_width=True
        )

    else:
        st.info("Belum ada data penjualan.")

    st.subheader("Data Penjualan")
    st.dataframe(
        st.session_state.penjualan,
        use_container_width=True
    )
