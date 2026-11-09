### Yorum ###
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Algoritma Adım Görselleştirici", layout="wide")
st.title("📊 Zaman Karmaşıklığı: Adım Adım Görselleştirici")

HAM_LISTE = [12, 5, 7, 14, 1, 9, 6, 11, 8, 15, 2, 3, 4, 10, 13]

algoritma = st.sidebar.selectbox(
    "Görselleştirilecek Algoritmayı Seçin:",
    [
        "O(n) - Doğrusal Arama (Linear Search)",
        "O(n²) - Seçmeli Sıralama (Selection Sort)",
        "O(n²) - Kabarcık Sıralaması (Bubble Sort)",
    ],
)


def adimlari_uret(secim, baslangic_listesi):
    liste = baslangic_listesi.copy()
    adimlar = []

    if "Doğrusal Arama" in secim:
        hedef = st.sidebar.slider("Aranacak Hedef Sayı:", 1, 15, 10)
        for i, val in enumerate(liste):
            durum = "✅ BULUNDU!" if val == hedef else "❌ Eşleşmedi, sıradakine geç"
            adimlar.append({
                "dizi": liste.copy(),
                "aktif": [i],
                "aciklama": f"Adım {i+1}: İndeks {i} (Değer: {val}) kontrol ediliyor. Hedef: {hedef} -> {durum}",
            })
            if val == hedef:
                break

    elif "Seçmeli Sıralama" in secim:
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

    elif "Kabarcık Sıralaması" in secim:
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


adim_listesi = adimlari_uret(algoritma, HAM_LISTE)
toplam_adim = len(adim_listesi)

st.markdown(f"**Başlangıç Listesi:** `{HAM_LISTE}` | **Toplam Adım Sayısı:** `{toplam_adim}`")

secili_adim = st.slider("Adım İlerlemesi (İleri / Geri Sarın):", 1, toplam_adim, 1)
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
