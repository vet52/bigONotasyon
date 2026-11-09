import streamlit as st

st.set_page_config(page_title="Algoritma Adım Görselleştirici", layout="wide")
st.title("📊 Zaman Karmaşıklığı: Adım Adım Görselleştirici")

HAM_LISTE = [12, 5, 7, 14, 1, 9, 6, 11, 8, 15, 2, 3, 4, 10, 13]

ALGORITMALAR = [
    "O(n) - Doğrusal Arama (Linear Search)",
    "O(log n) - İkili Arama (Binary Search - Sıralı Dizi)",
    "O(n²) - Seçmeli Sıralama (Selection Sort)",
    "O(n²) - Kabarcık Sıralaması (Bubble Sort)",
]

secili_algo = st.sidebar.selectbox("Görselleştirilecek Algoritmayı Seçin:", ALGORITMALAR)
algo_indeks = ALGORITMALAR.index(secili_algo)

# Arama algoritmaları seçiliyse hedef sayı kaydırıcısını göster
hedef_sayi = 10
if algo_indeks in [0, 1]:
    hedef_sayi = st.sidebar.slider("Aranacak Hedef Sayı:", 1, 15, 10)


def adimlari_uret(indeks, baslangic_listesi, hedef):
    liste = baslangic_listesi.copy()
    adimlar = []

    # 0: O(n) Doğrusal Arama
    if indeks == 0:
        for i, val in enumerate(liste):
            durum = "✅ BULUNDU!" if val == hedef else "❌ Eşleşmedi, sıradakine geç"
            adimlar.append({
                "dizi": liste.copy(),
                "aktif": [i],
                "aciklama": f"Adım {i+1}: İndeks {i} (Değer: {val}) kontrol ediliyor. Hedef: {hedef} -> {durum}",
            })
            if val == hedef:
                break

    # 1: O(log n) İkili Arama
    elif indeks == 1:
        liste.sort()
        sol = 0
        sag = len(liste) - 1
        adim_no = 0
        while sol <= sag:
            adim_no += 1
            orta = (sol + sag) // 2
            orta_deger = liste[orta]
            if orta_deger == hedef:
                adimlar.append({
                    "dizi": liste.copy(),
                    "aktif": [orta],
                    "aciklama": f"Adım {adim_no}: Aralık [{sol}..{sag}] | Orta İndeks: {orta} (Değer: {orta_deger}) -> ✅ BULUNDU!",
                })
                break
            elif orta_deger < hedef:
                adimlar.append({
                    "dizi": liste.copy(),
                    "aktif": [orta],
                    "aciklama": f"Adım {adim_no}: Aralık [{sol}..{sag}] | Orta Değer ({orta_deger}) < Hedef ({hedef}) -> Sağ yarıya geç",
                })
                sol = orta + 1
            else:
                adimlar.append({
                    "dizi": liste.copy(),
                    "aktif": [orta],
                    "aciklama": f"Adım {adim_no}: Aralık [{sol}..{sag}] | Orta Değer ({orta_deger}) > Hedef ({hedef}) -> Sol yarıya geç",
                })
                sag = orta - 1

    # 2: O(n²) Seçmeli Sıralama
    elif indeks == 2:
        n = len(liste)
        adim_no = 0
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                adim_no += 1
                if liste[j] < liste[min_idx]:
                    min_idx = j
                adimlar.append({
                    "dizi": liste.copy(),
                    "aktif": [i, j, min_idx],
                    "aciklama": f"Adım {adim_no}: İndeks {j} (Değer: {liste[j]}) taranıyor | Şu anki en küçük: {liste[min_idx]}",
                })
            liste[i], liste[min_idx] = liste[min_idx], liste[i]
            adimlar.append({
                "dizi": liste.copy(),
                "aktif": [i],
                "aciklama": f"🔄 TAKAS: {liste[i]} sayısı {i}. indekse yerleştirildi.",
            })

    # 3: O(n²) Kabarcık Sıralaması
    elif indeks == 3:
        n = len(liste)
        adim_no = 0
        for i in range(n - 1):
            for j in range(n - i - 1):
                adim_no += 1
                mesaj = f"Adım {adim_no}: {liste[j]} ve {liste[j+1]} karşılaştırılıyor."
                if liste[j] > liste[j + 1]:
                    liste[j], liste[j + 1] = liste[j + 1], liste[j]
                    mesaj += f" ({liste[j+1]} > {liste[j]} olduğu için yer değiştirdi 🔄)"
                adimlar.append({
                    "dizi": liste.copy(),
                    "aktif": [j, j + 1],
                    "aciklama": mesaj,
                })

    return adimlar


adim_listesi = adimlari_uret(algo_indeks, HAM_LISTE, hedef_sayi)
toplam_adim = len(adim_listesi)

st.markdown(f"**Başlangıç Listesi:** `{HAM_LISTE}` | **Toplam Adım Sayısı:** `{toplam_adim}`")

# HATA ÖNLEYİCİ KONTROL: Slider yalnızca toplam adım 1'den büyükse oluşturulur
if toplam_adim > 1:
    secili_adim = st.slider("Adım İlerlemesi (İleri / Geri Sarın):", 1, toplam_adim, 1)
elif toplam_adim == 1:
    secili_adim = 1
    st.success("İşlem tek adımda (O(1) en iyi senaryo) tamamlandığı için kaydırıcıya gerek kalmadı.")
else:
    st.error("Adım listesi oluşturulamadı.")
    st.stop()

mevcut = adim_listesi[secili_adim - 1]
st.info(mevcut["aciklama"])

# Sayıları ve aktif işlem gören elemanları HTML/CSS kutuları olarak yan yana çiz
cols = st.columns(len(HAM_LISTE))
for idx, (col, deger) in enumerate(zip(cols, mevcut["dizi"])):
    aktif_mi = idx in mevcut["aktif"]
    renk = "#ef4444" if aktif_mi else "#3b82f6"
    yukseklik = deger * 14
    col.markdown(
        f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:flex-end; height:240px;">
            <div style="font-weight:bold; margin-bottom:4px; color:{renk};">{deger}</div>
            <div style="width:100%; height:{yukseklik}px; background-color:{renk}; border-radius:4px 4px 0 0;"></div>
            <div style="font-size:11px; color:#888; margin-top:4px;">[{idx}]</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
