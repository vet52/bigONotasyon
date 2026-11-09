import streamlit as st
import math

st.set_page_config(page_title="Algoritma Adım Görselleştirici", layout="wide")
st.title("📊 Zaman Karmaşıklığı: Adım Adım Görselleştirici")

HAM_LISTE = [12, 5, 7, 14, 1, 9, 6, 11, 8, 15, 2, 3, 4, 10, 13]

ALGORITMALAR = [
    "O(n) - Doğrusal Arama (Linear Search)",
    "O(log n) - İkili Arama (Binary Search - Sıralı Dizi)",
    "O(√n) - Asal Sayı Kontrolü (Karekök Zaman Karmaşıklığı)",
    "O(n²) - Kuadratik Çift Arama (İç İçe Döngü ile Hedef Toplam Bulma)",
    "O(n²) - Kuadratik Seçmeli Sıralama (Selection Sort)",
    "O(n²) - Kuadratik Kabarcık Sıralaması (Bubble Sort)",
]

secili_algo = st.sidebar.selectbox("Görselleştirilecek Algoritmayı Seçin:", ALGORITMALAR)
algo_indeks = ALGORITMALAR.index(secili_algo)

# Algoritmaya göre yan menü (sidebar) parametreleri
hedef_sayi = 10
hedef_toplam = 23
cift_arama_modu = "Bulunca Dur (Erken Çıkış)"
asal_modu = "Tekil Sayı Testi (Detaylı Bölen Analizi)"
test_edilecek_sayi = 97

if algo_indeks in [0, 1]:
    hedef_sayi = st.sidebar.slider("Aranacak Hedef Sayı:", 1, 15, 10)
elif algo_indeks == 2:
    asal_modu = st.sidebar.radio(
        "Görselleştirme Modu:",
        ["Tekil Sayı Testi (Detaylı Bölen Analizi)", "15 Elemanlı Liste Üzerinde Test"]
    )
    if asal_modu == "Tekil Sayı Testi (Detaylı Bölen Analizi)":
        test_edilecek_sayi = st.sidebar.number_input(
            "Asallığı Test Edilecek Sayı (N):", min_value=2, max_value=10000, value=97, step=1
        )
elif algo_indeks == 3:
    hedef_toplam = st.sidebar.slider("Aranan İkili Toplam (Hedef = A + B):", 3, 30, 27)
    cift_arama_modu = st.sidebar.radio(
        "Döngü Davranışı:",
        [
            "Tüm Çiftleri Tara (Tam O(n²) En Kötü Senaryo)",
            "İlk Eşleşmede Dur (Bulunca Çık)"
        ]
    )


def adimlari_uret(indeks, baslangic_listesi, hedef, mod, n_sayi, h_toplam, cift_mod):
    liste = baslangic_listesi.copy()
    adimlar = []

    # 0: O(n) Doğrusal Arama
    if indeks == 0:
        for i, val in enumerate(liste):
            durum = "✅ BULUNDU!" if val == hedef else "❌ Eşleşmedi, sıradakine geç"
            adimlar.append({
                "dizi": liste.copy(),
                "etiketler": [f"[{k}]" for k in range(len(liste))],
                "dis_dongu": [],
                "aktif": [i],
                "bulundu": [i] if val == hedef else [],
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
                    "etiketler": [f"[{k}]" for k in range(len(liste))],
                    "dis_dongu": [],
                    "aktif": [orta],
                    "bulundu": [orta],
                    "aciklama": f"Adım {adim_no}: Aralık [{sol}..{sag}] | Orta İndeks: {orta} (Değer: {orta_deger}) -> ✅ BULUNDU!",
                })
                break
            elif orta_deger < hedef:
                adimlar.append({
                    "dizi": liste.copy(),
                    "etiketler": [f"[{k}]" for k in range(len(liste))],
                    "dis_dongu": [],
                    "aktif": [orta],
                    "bulundu": [],
                    "aciklama": f"Adım {adim_no}: Aralık [{sol}..{sag}] | Orta Değer ({orta_deger}) < Hedef ({hedef}) -> Sağ yarıya geç",
                })
                sol = orta + 1
            else:
                adimlar.append({
                    "dizi": liste.copy(),
                    "etiketler": [f"[{k}]" for k in range(len(liste))],
                    "dis_dongu": [],
                    "aktif": [orta],
                    "bulundu": [],
                    "aciklama": f"Adım {adim_no}: Aralık [{sol}..{sag}] | Orta Değer ({orta_deger}) > Hedef ({hedef}) -> Sol yarıya geç",
                })
                sag = orta - 1

    # 2: O(√n) Asal Sayı Kontrolü
    elif indeks == 2:
        if mod == "Tekil Sayı Testi (Detaylı Bölen Analizi)":
            sinir = int(math.isqrt(n_sayi))
            if sinir < 2:
                adimlar.append({
                    "dizi": [n_sayi],
                    "etiketler": ["Sayı"],
                    "dis_dongu": [],
                    "aktif": [0],
                    "bulundu": [0],
                    "aciklama": f"Sayı: {n_sayi} | √{n_sayi} = {sinir} olduğu için döngüye girmeden ASAL olduğu anlaşılır (1 Adım).",
                })
            else:
                bolen_adaylari = list(range(2, sinir + 1))
                for idx, bolen in enumerate(bolen_adaylari):
                    kalan = n_sayi % bolen
                    if kalan == 0:
                        adimlar.append({
                            "dizi": bolen_adaylari,
                            "etiketler": [f"÷{b}" for b in bolen_adaylari],
                            "dis_dongu": [],
                            "aktif": [idx],
                            "bulundu": [],
                            "aciklama": (
                                f"Adım {idx+1}: {n_sayi} ÷ {bolen} kontrol ediliyor (Kalan: 0) -> "
                                f"❌ TAM BÖLÜNDÜ! ({n_sayi} = {bolen} × {n_sayi//bolen}). Sayı ASAL DEĞİLDİR!"
                            ),
                        })
                        break
                    else:
                        son_adim_mi = (idx == len(bolen_adaylari) - 1)
                        ek_mesaj = (
                            f" -> ✅ √{n_sayi} sınırına ({sinir}) ulaşıldı, hiçbir sayı tam bölmedi. {n_sayi} ASAL SAYIDIR!"
                            if son_adim_mi else " -> Bölünmedi, sıradaki aday bölene geç."
                        )
                        adimlar.append({
                            "dizi": bolen_adaylari,
                            "etiketler": [f"÷{b}" for b in bolen_adaylari],
                            "dis_dongu": [],
                            "aktif": [idx],
                            "bulundu": [idx] if son_adim_mi else [],
                            "aciklama": f"Adım {idx+1}/{len(bolen_adaylari)}: {n_sayi} % {bolen} = {kalan} (Tam bölünmedi){ek_mesaj}",
                        })
        else:
            adim_no = 0
            for i, val in enumerate(liste):
                adim_no += 1
                if val < 2:
                    adimlar.append({
                        "dizi": liste.copy(),
                        "etiketler": [f"[{k}]" for k in range(len(liste))],
                        "dis_dongu": [],
                        "aktif": [i],
                        "bulundu": [],
                        "aciklama": f"Adım {adim_no}: Liste[{i}] = {val} -> 2'den küçük olduğu için ❌ ASAL DEĞİL.",
                    })
                    continue
                sinir = int(math.isqrt(val))
                asal_mi = True
                denenen_bolenler = []
                for b in range(2, sinir + 1):
                    denenen_bolenler.append(b)
                    if val % b == 0:
                        asal_mi = False
                        break
                durum = "✅ ASAL SAYI" if asal_mi else f"❌ ASAL DEĞİL ({denenen_bolenler[-1]}'e bölündü)"
                bolen_str = f"Denenen bölenler (2..√{val}={sinir}): {denenen_bolenler}" if denenen_bolenler else f"√{val}={sinir} < 2 (Bölen denemesine gerek yok)"
                adimlar.append({
                    "dizi": liste.copy(),
                    "etiketler": [f"[{k}]" for k in range(len(liste))],
                    "dis_dongu": [],
                    "aktif": [i],
                    "bulundu": [i] if asal_mi else [],
                    "aciklama": f"Adım {adim_no}: Sayı {val} kontrol edildi | {bolen_str} -> {durum}",
                })

    # 3: O(n²) Kuadratik Çift Arama (İç İçe İki Döngü - Two Sum Brute Force)
    elif indeks == 3:
        n = len(liste)
        adim_no = 0
        bulunan_ciftler = []
        erken_cik = "İlk Eşleşmede" in cift_mod

        for i in range(n):
            for j in range(i + 1, n):
                adim_no += 1
                toplam = liste[i] + liste[j]
                eslesti_mi = (toplam == h_toplam)

                if eslesti_mi:
                    bulunan_ciftler.append(f"({liste[i]}+{liste[j]})")
                    durum_mesaji = f"✅ HEDEF BULUNDU! ({liste[i]} + {liste[j]} = {h_toplam})"
                else:
                    durum_mesaji = f"❌ Eşleşmedi ({liste[i]} + {liste[j]} = {toplam} ≠ {h_toplam})"

                adimlar.append({
                    "dizi": liste.copy(),
                    "etiketler": [f"[{k}]" for k in range(n)],
                    "dis_dongu": [i],  # Turuncu: Dış döngünün sabit tuttuğu eleman
                    "aktif": [j],      # Kırmızı: İç döngünün o an denediği eleman
                    "bulundu": [i, j] if eslesti_mi else [],
                    "aciklama": (
                        f"Adım {adim_no} | Dış Döngü i={i} (Değer: {liste[i]}) sabit tutuldu, "
                        f"İç Döngü j={j} (Değer: {liste[j]}) ile toplanıyor -> {durum_mesaji}"
                    ),
                })
                if eslesti_mi and erken_cik:
                    return adimlar

    # 4: O(n²) Kuadratik Seçmeli Sıralama
    elif indeks == 4:
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
                    "etiketler": [f"[{k}]" for k in range(len(liste))],
                    "dis_dongu": [i],
                    "aktif": [j, min_idx],
                    "bulundu": [],
                    "aciklama": f"Adım {adim_no}: Dış İndeks i={i} için İç İndeks j={j} (Değer: {liste[j]}) taranıyor | Şu anki en küçük: {liste[min_idx]}",
                })
            liste[i], liste[min_idx] = liste[min_idx], liste[i]
            adimlar.append({
                "dizi": liste.copy(),
                "etiketler": [f"[{k}]" for k in range(len(liste))],
                "dis_dongu": [],
                "aktif": [],
                "bulundu": [i],
                "aciklama": f"🔄 TAKAS: {liste[i]} sayısı {i}. indekse kalıcı olarak yerleştirildi.",
            })

    # 5: O(n²) Kuadratik Kabarcık Sıralaması
    elif indeks == 5:
        n = len(liste)
        adim_no = 0
        for i in range(n - 1):
            for j in range(n - i - 1):
                adim_no += 1
                mesaj = f"Adım {adim_no} (Tur {i+1}): {liste[j]} ve {liste[j+1]} karşılaştırılıyor."
                takas_yapildi = False
                if liste[j] > liste[j + 1]:
                    liste[j], liste[j + 1] = liste[j + 1], liste[j]
                    takas_yapildi = True
                    mesaj += f" ({liste[j+1]} > {liste[j]} olduğu için yer değiştirdi 🔄)"
                adimlar.append({
                    "dizi": liste.copy(),
                    "etiketler": [f"[{k}]" for k in range(len(liste))],
                    "dis_dongu": [j] if not takas_yapildi else [],
                    "aktif": [j, j + 1] if takas_yapildi else [j + 1],
                    "bulundu": list(range(n - i, n)),
                    "aciklama": mesaj,
                })

    return adimlar


adim_listesi = adimlari_uret(
    algo_indeks, HAM_LISTE, hedef_sayi, asal_modu, test_edilecek_sayi, hedef_toplam, cift_arama_modu
)
toplam_adim = len(adim_listesi)

# Seçili algoritmaya özel bilgi kartları
if algo_indeks == 2 and asal_modu == "Tekil Sayı Testi (Detaylı Bölen Analizi)":
    karekoku = int(math.isqrt(test_edilecek_sayi))
    st.success(
        f"💡 **O(√n) Optimizasyon Farkı:** **{test_edilecek_sayi}** sayısı için O(n) algoritması **~{test_edilecek_sayi - 2} adım** "
        f"deneme yaparken, O(√n) algoritması yalnızca **√{test_edilecek_sayi} ≈ {karekoku}** sınırına kadar (en fazla **{max(1, karekoku - 1)} adım**) deneme yapar!"
    )
elif algo_indeks in [3, 4, 5]:
    n_boyut = len(HAM_LISTE)
    st.warning(
        f"⚠️ **O(n²) Kuadratik Büyüme Uyarısı:** Liste boyutu **N = {n_boyut}** iken iç içe iki döngü **N × (N - 1) / 2 = {(n_boyut * (n_boyut - 1)) // 2}** "
        f"karşılaştırma adımı üretir. Eğer liste boyutu 1.000 olsaydı, bu işlem yaklaşık **500.000 adım** sürecekti!"
    )
else:
    st.markdown(f"**Başlangıç Listesi:** `{HAM_LISTE}` | **Toplam Adım Sayısı:** `{toplam_adim}`")

# HATA ÖNLEYİCİ KONTROL: Slider yalnızca toplam adım 1'den büyükse oluşturulur
if toplam_adim > 1:
    secili_adim = st.slider("Adım İlerlemesi (İleri / Geri Sarın):", 1, toplam_adim, 1)
elif toplam_adim == 1:
    secili_adim = 1
    st.info("İşlem tek adımda tamamlandığı için kaydırıcıya gerek kalmadı.")
else:
    st.error("Adım listesi oluşturulamadı.")
    st.stop()

mevcut = adim_listesi[secili_adim - 1]
st.info(mevcut["aciklama"])

# Renk açıklaması (Lejand)
st.caption("🟧 **Turuncu:** Dış Döngü (Sabit Tutulan Eleman `i`) | 🟥 **Kırmızı:** İç Döngü (Kontrol Edilen Eleman `j`) | 🟩 **Yeşil:** Eşleşen / Yerleşen Eleman | 🟦 **Mavi:** Bekleyen Elemanlar")

# Çubukların ekran yüksekliğini aşmaması için dinamik ölçekleme
gosterilen_dizi = mevcut["dizi"]
maks_deger = max(gosterilen_dizi) if gosterilen_dizi else 1

cols = st.columns(len(gosterilen_dizi))
for idx, (col, deger) in enumerate(zip(cols, gosterilen_dizi)):
    if idx in mevcut.get("bulundu", []):
        renk = "#10b981"  # Yeşil (Eşleşti / Yerleşti)
    elif idx in mevcut.get("aktif", []):
        renk = "#ef4444"  # Kırmızı (İç döngü aktif)
    elif idx in mevcut.get("dis_dongu", []):
        renk = "#f59e0b"  # Turuncu (Dış döngü sabit)
    else:
        renk = "#3b82f6"  # Mavi (Normal)

    yukseklik = int((deger / maks_deger) * 180) + 20
    etiket = mevcut["etiketler"][idx]
    col.markdown(
        f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:flex-end; height:240px;">
            <div style="font-weight:bold; margin-bottom:4px; color:{renk};">{deger}</div>
            <div style="width:100%; height:{yukseklik}px; background-color:{renk}; border-radius:4px 4px 0 0;"></div>
            <div style="font-size:11px; color:#888; margin-top:4px;">{etiket}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
