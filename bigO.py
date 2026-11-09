import streamlit as st
import math
import random
import itertools
import pandas as pd

st.set_page_config(page_title="Big-O Algoritma Laboratuvarı", layout="wide")
st.title("📊 Big-O Zaman Karmaşıklığı ve Senaryo Laboratuvarı")

VARSAYILAN_LISTE = [12, 5, 7, 14, 1, 9, 6, 11, 8, 15, 2, 3, 4, 10, 13]

# =====================================================================
# 1. YAN MENÜ: VERİ SETİ OLUŞTURMA (SABİT VEYA RASTGELE DİNAMİK)
# =====================================================================
st.sidebar.header("1. Veri Kümesi Ayarları")
veri_kaynagi = st.sidebar.radio(
    "Liste Türü:",
    ["Kullanıcı Tanımlı Rastgele Liste", "Sabit 15 Elemanlı Örnek Liste"]
)

if veri_kaynagi == "Kullanıcı Tanımlı Rastgele Liste":
    n_boyut = st.sidebar.slider("Eleman Sayısı (N):", min_value=5, max_value=25, value=12, step=1)
    if "rastgele_liste" not in st.session_state or len(st.session_state.rastgele_liste) != n_boyut:
        st.session_state.rastgele_liste = random.sample(range(1, n_boyut * 3), n_boyut)
    if st.sidebar.button("🎲 Yeni Rastgele Liste Üret"):
        st.session_state.rastgele_liste = random.sample(range(1, n_boyut * 3), n_boyut)
    AKTIF_LISTE = st.session_state.rastgele_liste.copy()
else:
    AKTIF_LISTE = VARSAYILAN_LISTE.copy()

# =====================================================================
# 2. YAN MENÜ: ALGORİTMA VE SENARYO SEÇİMİ
# =====================================================================
st.sidebar.header("2. Algoritma Seçimi")
ALGORITMALAR = [
    "O(n) - Doğrusal Arama (Best / Average / Worst Case)",
    "O(log n) - İkili Arama (Best / Average / Worst Case)",
    "O(√n) - Asal Sayı Kontrolü (Karekök Karmaşıklığı)",
    "O(n²) - Kuadratik Çift Arama (2-Sum: A + B = Hedef)",
    "O(n²) - Kuadratik Kabarcık Sıralaması (Best / Average / Worst Case)",
    "O(n³) - Kübik Üçlü Arama (3-Sum: A + B + C = Hedef)",
    "O(2^n) - Üstel Zaman (Tüm Alt Kümeleri Üretme - Power Set)",
    "O(n!) - Faktöriyel Zaman (Tüm Permütasyonları Sıralama)",
]

secili_algo = st.sidebar.selectbox("Algoritma / Karmaşıklık Sınıfı:", ALGORITMALAR)
algo_indeks = ALGORITMALAR.index(secili_algo)

# =====================================================================
# 3. YAN MENÜ: SENARYO (BEST / AVERAGE / WORST CASE) VE PARAMETRELER
# =====================================================================
st.sidebar.header("3. Senaryo ve Parametreler")

senaryo_modu = "Manuel / Ortalama"
hedef_sayi = AKTIF_LISTE[len(AKTIF_LISTE) // 2]
hedef_toplam = sum(AKTIF_LISTE[:3])
asal_sayi = 97
alt_boyut = 4

# O(n) Doğrusal Arama Senaryoları
if algo_indeks == 0:
    senaryo_modu = st.sidebar.radio(
        "Senaryo Seçin:",
        [
            "En İyi Durum (Best Case - O(1)): İlk Eleman",
            "Ortalama Durum (Average Case - O(n/2)): Ortadaki Eleman",
            "En Kötü Durum (Worst Case - O(n)): Son Eleman / Listede Yok",
            "Manuel Hedef Seçimi"
        ]
    )
    if "En İyi" in senaryo_modu:
        hedef_sayi = AKTIF_LISTE[0]
    elif "Ortalama" in senaryo_modu:
        hedef_sayi = AKTIF_LISTE[len(AKTIF_LISTE) // 2]
    elif "En Kötü" in senaryo_modu:
        hedef_sayi = -99  # Listede olmayan sayı
    else:
        hedef_sayi = st.sidebar.selectbox("Aranacak Sayı:", AKTIF_LISTE + [-99])

# O(log n) İkili Arama Senaryoları
elif algo_indeks == 1:
    sirali_gecici = sorted(AKTIF_LISTE)
    orta_idx = (len(sirali_gecici) - 1) // 2
    senaryo_modu = st.sidebar.radio(
        "Senaryo Seçin:",
        [
            "En İyi Durum (Best Case - O(1)): Tam Ortadaki Eleman",
            "Ortalama Durum (Average Case - O(log n)): Ara Eleman",
            "En Kötü Durum (Worst Case - O(log n)): Uç Eleman / Listede Yok",
        ]
    )
    if "En İyi" in senaryo_modu:
        hedef_sayi = sirali_gecici[orta_idx]
    elif "Ortalama" in senaryo_modu:
        hedef_sayi = sirali_gecici[max(0, orta_idx // 2)]
    else:
        hedef_sayi = -99

# O(√n) Asal Sayı Kontrolü
elif algo_indeks == 2:
    senaryo_modu = st.sidebar.radio(
        "Senaryo Seçin:",
        [
            "En İyi Durum (Best Case - O(1)): Çift Sayı (98 - 2'ye bölünür)",
            "Ortalama Durum (Average Case): Küçük Çarpanlı (91 = 7×13)",
            "En Kötü Durum (Worst Case - Tam O(√n)): Asal Sayı (97)",
            "Manuel Sayı Girişi"
        ]
    )
    if "En İyi" in senaryo_modu:
        asal_sayi = 98
    elif "Ortalama" in senaryo_modu:
        asal_sayi = 91
    elif "En Kötü" in senaryo_modu:
        asal_sayi = 97
    else:
        asal_sayi = st.sidebar.number_input("Test Edilecek Sayı:", 2, 10000, 97)

# O(n²) Çift Arama
elif algo_indeks == 3:
    min_t = min(AKTIF_LISTE) * 2
    max_t = max(AKTIF_LISTE) * 2
    hedef_toplam = st.sidebar.slider("Hedef İkili Toplam (A + B):", min_t, max_t, AKTIF_LISTE[0] + AKTIF_LISTE[-1])

# O(n²) Bubble Sort Senaryoları
elif algo_indeks == 4:
    senaryo_modu = st.sidebar.radio(
        "Dizi Başlangıç Durumu (Senaryo):",
        [
            "En İyi Durum (Best Case - O(n)): Zaten Sıralı Dizi",
            "Ortalama Durum (Average Case - O(n²)): Rastgele Dağılmış Dizi",
            "En Kötü Durum (Worst Case - O(n²)): Ters Sıralı Dizi"
        ]
    )
    if "En İyi" in senaryo_modu:
        AKTIF_LISTE = sorted(AKTIF_LISTE)
    elif "En Kötü" in senaryo_modu:
        AKTIF_LISTE = sorted(AKTIF_LISTE, reverse=True)

# O(n³) Kübik Üçlü Arama (3-Sum)
elif algo_indeks == 5:
    alt_boyut = st.sidebar.slider("Kübik Tarama İçin Eleman Sınırı (N):", 4, min(10, len(AKTIF_LISTE)), min(7, len(AKTIF_LISTE)))
    AKTIF_LISTE = AKTIF_LISTE[:alt_boyut]
    varsayilan_3 = AKTIF_LISTE[-3] + AKTIF_LISTE[-2] + AKTIF_LISTE[-1]
    hedef_toplam = st.sidebar.number_input("Hedef Üçlü Toplam (A + B + C):", value=varsayilan_3)

# O(2^n) Üstel Zaman
elif algo_indeks == 6:
    alt_boyut = st.sidebar.slider("Alt Kümesi Üretilecek Eleman Sayısı (N):", 3, min(7, len(AKTIF_LISTE)), 4)
    AKTIF_LISTE = AKTIF_LISTE[:alt_boyut]

# O(n!) Faktöriyel Zaman
elif algo_indeks == 7:
    alt_boyut = st.sidebar.slider("Permütasyonu Üretilecek Eleman Sayısı (N):", 3, min(5, len(AKTIF_LISTE)), 4)
    AKTIF_LISTE = AKTIF_LISTE[:alt_boyut]


# =====================================================================
# ADIM ÜRETİCİ FONKSİYON
# =====================================================================
def adimlari_uret(indeks, baslangic_listesi, h_sayi, h_toplam, n_asal):
    liste = baslangic_listesi.copy()
    n = len(liste)
    adimlar = []

    # 0: O(n) Doğrusal Arama
    if indeks == 0:
        for i, val in enumerate(liste):
            bulundu = (val == h_sayi)
            durum = "✅ HEDEF BULUNDU!" if bulundu else f"❌ {val} ≠ {h_sayi} (Sıradakine geç)"
            adimlar.append({
                "dizi": liste.copy(),
                "etiketler": [f"[{k}]" for k in range(n)],
                "dis_dongu": [], "orta_dongu": [],
                "aktif": [i],
                "bulundu": [i] if bulundu else [],
                "aciklama": f"Adım {i+1}: İndeks {i} (Değer: {val}) kontrol ediliyor -> {durum}"
            })
            if bulundu:
                break

    # 1: O(log n) İkili Arama
    elif indeks == 1:
        liste.sort()
        sol, sag = 0, n - 1
        adim_no = 0
        while sol <= sag:
            adim_no += 1
            orta = (sol + sag) // 2
            val = liste[orta]
            aktif_aralik = list(range(sol, sag + 1))
            if val == h_sayi:
                adimlar.append({
                    "dizi": liste.copy(),
                    "etiketler": [f"[{k}]" for k in range(n)],
                    "dis_dongu": aktif_aralik, "orta_dongu": [],
                    "aktif": [orta], "bulundu": [orta],
                    "aciklama": f"Adım {adim_no}: Arama Aralığı [{sol}..{sag}] | Orta İndeks {orta} (Değer: {val}) -> ✅ BULUNDU!"
                })
                break
            elif val < h_sayi:
                adimlar.append({
                    "dizi": liste.copy(),
                    "etiketler": [f"[{k}]" for k in range(n)],
                    "dis_dongu": aktif_aralik, "orta_dongu": [],
                    "aktif": [orta], "bulundu": [],
                    "aciklama": f"Adım {adim_no}: Aralık [{sol}..{sag}] | Orta ({val}) < Hedef ({h_sayi}) -> Sol yarı çöpe atıldı, sağa geç."
                })
                sol = orta + 1
            else:
                adimlar.append({
                    "dizi": liste.copy(),
                    "etiketler": [f"[{k}]" for k in range(n)],
                    "dis_dongu": aktif_aralik, "orta_dongu": [],
                    "aktif": [orta], "bulundu": [],
                    "aciklama": f"Adım {adim_no}: Aralık [{sol}..{sag}] | Orta ({val}) > Hedef ({h_sayi}) -> Sağ yarı çöpe atıldı, sola geç."
                })
                sag = orta - 1

    # 2: O(√n) Asal Sayı Kontrolü
    elif indeks == 2:
        sinir = int(math.isqrt(n_asal))
        bolenler = list(range(2, max(3, sinir + 1)))
        for idx, b in enumerate(bolenler):
            kalan = n_asal % b
            if kalan == 0 and n_asal != b:
                adimlar.append({
                    "dizi": bolenler,
                    "etiketler": [f"÷{x}" for x in bolenler],
                    "dis_dongu": [], "orta_dongu": [],
                    "aktif": [idx], "bulundu": [],
                    "aciklama": f"Adım {idx+1}: {n_asal} ÷ {b} tam bölündü! ({n_asal} = {b} × {n_asal//b}) -> ❌ ASAL DEĞİL (Erken Çıkış)"
                })
                break
            else:
                son_mu = (idx == len(bolenler) - 1)
                mesaj = f"✅ √{n_asal}={sinir} sınırına ulaşıldı, bölen çıkmadı -> SAYI ASALDIR!" if son_mu else "Bölünmedi, devam."
                adimlar.append({
                    "dizi": bolenler,
                    "etiketler": [f"÷{x}" for x in bolenler],
                    "dis_dongu": [], "orta_dongu": [],
                    "aktif": [idx], "bulundu": [idx] if son_mu else [],
                    "aciklama": f"Adım {idx+1}: {n_asal} % {b} = {kalan} -> {mesaj}"
                })

    # 3: O(n²) Kuadratik Çift Arama (2-Sum)
    elif indeks == 3:
        adim_no = 0
        for i in range(n):
            for j in range(i + 1, n):
                adim_no += 1
                toplam = liste[i] + liste[j]
                bulundu = (toplam == h_toplam)
                adimlar.append({
                    "dizi": liste.copy(),
                    "etiketler": [f"[{k}]" for k in range(n)],
                    "dis_dongu": [i], "orta_dongu": [],
                    "aktif": [j],
                    "bulundu": [i, j] if bulundu else [],
                    "aciklama": f"Adım {adim_no}: Dış(i={i}) [{liste[i]}] + İç(j={j}) [{liste[j]}] = {toplam} (Hedef: {h_toplam}) -> {'✅ EŞLEŞTİ!' if bulundu else '❌ Eşleşmedi'}"
                })

    # 4: O(n²) Kabarcık Sıralaması (Optimize Edilmiş - Best Case O(n) Destekli)
    elif indeks == 4:
        adim_no = 0
        for i in range(n - 1):
            takas_oldu = False
            for j in range(n - i - 1):
                adim_no += 1
                msg = f"Adım {adim_no} (Tur {i+1}): {liste[j]} ile {liste[j+1]} karşılaştırılıyor."
                if liste[j] > liste[j + 1]:
                    liste[j], liste[j + 1] = liste[j + 1], liste[j]
                    takas_oldu = True
                    msg += " -> 🔄 Yer değiştirdi!"
                adimlar.append({
                    "dizi": liste.copy(),
                    "etiketler": [f"[{k}]" for k in range(n)],
                    "dis_dongu": [j], "orta_dongu": [],
                    "aktif": [j + 1],
                    "bulundu": list(range(n - i, n)),
                    "aciklama": msg
                })
            if not takas_oldu:
                adimlar[-1]["bulundu"] = list(range(n))
                adimlar[-1]["aciklama"] += " | ✅ Bu turda hiç takas olmadı! Dizi sıralı olduğu için algoritma erken durdu (Best Case O(n))."
                break

    # 5: O(n³) Kübik Üçlü Arama (3-Sum: İç İçe 3 Döngü)
    elif indeks == 5:
        adim_no = 0
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    adim_no += 1
                    toplam = liste[i] + liste[j] + liste[k]
                    bulundu = (toplam == h_toplam)
                    adimlar.append({
                        "dizi": liste.copy(),
                        "etiketler": [f"[{x}]" for x in range(n)],
                        "dis_dongu": [i],     # Turuncu: 1. Döngü (i)
                        "orta_dongu": [j],    # Mor: 2. Döngü (j)
                        "aktif": [k],         # Kırmızı: 3. Döngü (k)
                        "bulundu": [i, j, k] if bulundu else [],
                        "aciklama": (
                            f"Adım {adim_no} (O(n³)): i={i} ({liste[i]}) + j={j} ({liste[j]}) + k={k} ({liste[k]}) = {toplam} "
                            f"(Hedef: {h_toplam}) -> {'✅ ÜÇLÜ BULUNDU!' if bulundu else '❌ Eşleşmedi'}"
                        )
                    })

    # 6: O(2^n) Üstel Zaman (Tüm Alt Kümeleri / Power Set Üretme)
    elif indeks == 6:
        toplam_alt_kume = 2 ** n
        for maske in range(toplam_alt_kume):
            secilen_indeksler = [bit for bit in range(n) if (maske & (1 << bit))]
            alt_kume_degerleri = [liste[idx] for idx in secilen_indeksler]
            ikili_kod = format(maske, f"0{n}b")[::-1]
            adimlar.append({
                "dizi": liste.copy(),
                "etiketler": [f"Bit:{ikili_kod[x]}" for x in range(n)],
                "dis_dongu": [], "orta_dongu": [],
                "aktif": [],
                "bulundu": secilen_indeksler,
                "aciklama": (
                    f"Adım {maske + 1}/{toplam_alt_kume} (Maske: {ikili_kod}): "
                    f"Seçilen Alt Küme = {alt_kume_degerleri} (Küme Toplamı: {sum(alt_kume_degerleri)})"
                )
            })

    # 7: O(n!) Faktöriyel Zaman (Tüm Permütasyonları Üretme)
    elif indeks == 7:
        tum_permutasyonlar = list(itertools.permutations(liste))
        toplam_perm = len(tum_permutasyonlar)
        for idx, perm in enumerate(tum_permutasyonlar):
            perm_list = list(perm)
            degisenler = [k for k in range(n) if perm_list[k] != liste[k]]
            adimlar.append({
                "dizi": perm_list,
                "etiketler": [f"Poz:{k}" for k in range(n)],
                "dis_dongu": [], "orta_dongu": [],
                "aktif": degisenler,
                "bulundu": list(range(n)) if perm_list == sorted(liste) else [],
                "aciklama": (
                    f"Adım {idx + 1}/{toplam_perm} (N! = {n}!): Permütasyon Dizilimi = {perm_list} "
                    f"{'-> ✅ TAM SIRALI DİZİLİM YAKALANDI!' if perm_list == sorted(liste) else ''}"
                )
            })

    return adimlar


# Adımları üret
adim_listesi = adimlari_uret(algo_indeks, AKTIF_LISTE, hedef_sayi, hedef_toplam, asal_sayi)
toplam_adim = len(adim_listesi)
n_mevcut = len(AKTIF_LISTE)

# =====================================================================
# GÖRSEL ANLAMAYI KOLAYLAŞTIRICI UNSUR 1: ÜST METRİK KARTLARI (KPI)
# =====================================================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Veri Boyutu (N)", f"{n_mevcut} Eleman" if algo_indeks != 2 else f"N = {asal_sayi}")
col2.metric("Gerçekleşen İşlem Sayısı", f"{toplam_adim} Adım")

# O(n) ile kıyaslama metriği
if algo_indeks == 1:
    col3.metric("O(n) Olsaydı (Worst Case)", f"{n_mevcut} Adım", delta=f"{toplam_adim - n_mevcut} Adım Tasarruf", delta_color="inverse")
elif algo_indeks == 2:
    col3.metric("O(n) Olsaydı (Worst Case)", f"{asal_sayi - 2} Adım", delta=f"{toplam_adim - (asal_sayi - 2)} Adım Tasarruf", delta_color="inverse")
elif algo_indeks in [3, 4]:
    col3.metric("Büyüme Çarpanı (N²)", f"{n_mevcut ** 2} Teorik Tavan")
elif algo_indeks == 5:
    col3.metric("Kübik Çarpan (N³)", f"{n_mevcut ** 3} Teorik Tavan")
elif algo_indeks == 6:
    col3.metric("N=15 Olsaydı (2^15)", "32.768 Adım!")
elif algo_indeks == 7:
    col3.metric("N=15 Olsaydı (15!)", "1.3 Trilyon Adım!")
else:
    col3.metric("Teorik Tavan (Worst Case)", f"{n_mevcut} Adım")

col4.metric("Aktif Senaryo", senaryo_modu.split("(")[0].strip())

st.divider()

# =====================================================================
# ADIM KAYDIRICISI VE İLERLEME ÇUBUĞU
# =====================================================================
if toplam_adim > 1:
    secili_adim = st.slider("⏯️ Adım İlerlemesi (İleri / Geri Sararak Algoritmayı İzleyin):", 1, toplam_adim, 1)
elif toplam_adim == 1:
    secili_adim = 1
    st.success("⚡ **En İyi Durum (Best Case - O(1)):** İşlem ilk adımda tamamlandığı için döngüye devam edilmedi!")
else:
    st.error("Adım üretilemedi.")
    st.stop()

# İlerleme Çubuğu (Progress Bar)
st.progress(secili_adim / toplam_adim, text=f"Algoritma İlerlemesi: Adım {secili_adim} / {toplam_adim} (%{int((secili_adim/toplam_adim)*100)})")

mevcut = adim_listesi[secili_adim - 1]
st.info(f"**Anlık İşlem Detayı:** {mevcut['aciklama']}")

# Renk Rehberi (Lejand)
st.caption(
    "🟧 **Turuncu:** 1. Dış Döngü (`i`) / Aktif Arama Aralığı | "
    "🟪 **Mor:** 2. Orta Döngü (`j` - Kübik) | "
    "🟥 **Kırmızı:** Aktif Kontrol Edilen Eleman (`k`) | "
    "🟩 **Yeşil:** Hedef Bulundu / Seçilen Alt Küme / Sıralandı | "
    "🟦 **Mavi:** Bekleyen Elemanlar"
)

# =====================================================================
# GÖRSEL ANLAMAYI KOLAYLAŞTIRICI UNSUR 2: DİNAMİK RENKLİ ÇUBUK GRAFİK
# =====================================================================
gosterilen_dizi = mevcut["dizi"]
maks_deger = max(gosterilen_dizi) if gosterilen_dizi else 1

cols = st.columns(len(gosterilen_dizi))
for idx, (col, deger) in enumerate(zip(cols, gosterilen_dizi)):
    if idx in mevcut.get("bulundu", []):
        renk = "#10b981"  # Yeşil
        durum_ikon = "✓"
    elif idx in mevcut.get("aktif", []):
        renk = "#ef4444"  # Kırmızı
        durum_ikon = "▼"
    elif idx in mevcut.get("orta_dongu", []):
        renk = "#8b5cf6"  # Mor (Kübik 2. döngü)
        durum_ikon = "◈"
    elif idx in mevcut.get("dis_dongu", []):
        renk = "#f59e0b"  # Turuncu (1. Dış döngü)
        durum_ikon = "●"
    else:
        renk = "#3b82f6"  # Mavi
        durum_ikon = "&nbsp;"

    yukseklik = int((deger / maks_deger) * 170) + 25
    etiket = mevcut["etiketler"][idx]
    col.markdown(
        f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:flex-end; height:250px;">
            <div style="font-size:14px; font-weight:bold; color:{renk};">{durum_ikon}</div>
            <div style="font-weight:bold; margin-bottom:4px; color:{renk};">{deger}</div>
            <div style="width:100%; height:{yukseklik}px; background-color:{renk}; border-radius:6px 6px 0 0; transition: all 0.2s;"></div>
            <div style="font-size:11px; color:#666; margin-top:4px; font-family:monospace;">{etiket}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =====================================================================
# GÖRSEL ANLAMAYI KOLAYLAŞTIRICI UNSUR 3: KARMAŞIKLIK KIYASLAMA TABLOSU
# =====================================================================
with st.expander("📈 Mevcut Veri Boyutu (N) İçin Tüm Karmaşıklık Sınıflarının Kıyaslama Tablosu", expanded=True):
    n_hesap = n_mevcut
    karsilastirma_df = pd.DataFrame([
        {"Sınıf": "O(1) - Sabit", "En İyi (Best)": 1, "Ortalama (Avg)": 1, "En Kötü (Worst)": 1, "Durum": "🟢 Mükemmel"},
        {"Sınıf": "O(log n) - Logaritmik", "En İyi (Best)": 1, "Ortalama (Avg)": max(1, int(math.log2(n_hesap))), "En Kötü (Worst)": max(1, math.ceil(math.log2(n_hesap))), "Durum": "🟢 Çok Hızlı"},
        {"Sınıf": "O(√n) - Karekök", "En İyi (Best)": 1, "Ortalama (Avg)": max(1, int(math.isqrt(n_hesap)) // 2), "En Kötü (Worst)": max(1, int(math.isqrt(n_hesap))), "Durum": "🟢 Hızlı"},
        {"Sınıf": "O(n) - Doğrusal", "En İyi (Best)": 1, "Ortalama (Avg)": n_hesap // 2, "En Kötü (Worst)": n_hesap, "Durum": "🟡 İyi / Kabul Edilebilir"},
        {"Sınıf": "O(n²) - Kuadratik", "En İyi (Best)": n_hesap, "Ortalama (Avg)": (n_hesap ** 2) // 2, "En Kötü (Worst)": n_hesap ** 2, "Durum": "🟠 Yavaş (Büyük veride darboğaz)"},
        {"Sınıf": "O(n³) - Kübik", "En İyi (Best)": (n_hesap*(n_hesap-1)*(n_hesap-2))//6, "Ortalama (Avg)": (n_hesap ** 3) // 4, "En Kötü (Worst)": n_hesap ** 3, "Durum": "🔴 Çok Yavaş"},
        {"Sınıf": "O(2^n) - Üstel", "En İyi (Best)": 2 ** n_hesap, "Ortalama (Avg)": 2 ** n_hesap, "En Kötü (Worst)": 2 ** n_hesap, "Durum": "⛔ Tehlikeli (Çökme Riski)"},
        {"Sınıf": "O(n!) - Faktöriyel", "En İyi (Best)": math.factorial(min(n_hesap, 12)), "Ortalama (Avg)": math.factorial(min(n_hesap, 12)), "En Kötü (Worst)": math.factorial(min(n_hesap, 12)), "Durum": "💀 İmkansız (N>12 için kilitlenir)"},
    ])
    st.dataframe(karsilastirma_df, use_container_width=True, hide_index=True)
