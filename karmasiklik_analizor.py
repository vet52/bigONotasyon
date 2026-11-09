### Karmaşıklık ölçer ###
import streamlit as st
import ast
import time
import math
import pandas as pd

st.set_page_config(page_title="Python Kod Karmaşıklığı Analizörü", layout="wide")
st.title("🕵️‍♂️ Python Kodu Zaman Karmaşıklığı (Big-O) Hesaplayıcı")

# =====================================================================
# HAZIR ÖRNEK KOD ŞABLONLARI
# =====================================================================
ORNEK_KODLAR = {
    "Örnek 1: O(n²) - İç İçe Döngü (Kuadratik)": """def cozum(n):
    toplam = 0
    for i in range(n):
        for j in range(n):
            toplam += i * j
    return toplam""",

    "Örnek 2: O(log n) - Yarıya Bölerek İlerleme (Logaritmik)": """def cozum(n):
    adim = 0
    while n > 1:
        n = n // 2
        adim += 1
    return adim""",

    "Örnek 3: O(n) - Tek Döngü (Doğrusal)": """def cozum(n):
    liste = [i for i in range(n)]
    toplam = 0
    for eleman in liste:
        toplam += eleman
    return toplam""",

    "Örnek 4: O(n log n) - Sıralama veya Döngü İçi Bölme": """def cozum(n):
    sayac = 0
    for i in range(n):
        k = n
        while k > 1:
            k = k // 2
            sayac += 1
    return sayac""",

    "Örnek 5: O(n³) - Kübik Zaman (3'lü İç İçe Döngü)": """def cozum(n):
    sayac = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                sayac += 1
    return sayac""",

    "Örnek 6: O(2^n) - Üstel Özyineleme (Recursive Fibonacci)": """def cozum(n):
    if n <= 1:
        return n
    return cozum(n - 1) + cozum(n - 2)"""
}


# =====================================================================
# 1. MOTOR: AST TABANLI STATİK KOD ANALİZÖRÜ
# =====================================================================
class BigOAstAnalizor(ast.NodeVisitor):
    def __init__(self):
        self.maks_dongu_derinligi = 0
        self.mevcut_derinlik = 0
        self.logaritmik_bolme_var = False
        self.log_dongu_derinligi = 0
        self.siralama_cagrisi_var = False
        self.fonksiyon_adi = None
        self.ozyineleme_sayisi = 0
        self.bulgular = []

    def visit_FunctionDef(self, node):
        self.fonksiyon_adi = node.name
        self.generic_visit(node)

    def _dongu_incele(self, node, tur):
        self.mevcut_derinlik += 1
        if self.mevcut_derinlik > self.maks_dongu_derinligi:
            self.maks_dongu_derinligi = self.mevcut_derinlik

        # Döngü gövdesinde ikiye bölme veya ikiyle çarpma (log n belirtisi) var mı?
        for alt_dugum in ast.walk(node):
            if isinstance(alt_dugum, ast.AugAssign) and isinstance(alt_dugum.op, (ast.FloorDiv, ast.Div, ast.Mult, ast.RShift)):
                self.logaritmik_bolme_var = True
                self.log_dongu_derinligi = max(self.log_dongu_derinligi, self.mevcut_derinlik)
            elif isinstance(alt_dugum, ast.Assign):
                for deger_dugum in ast.walk(alt_dugum.value):
                    if isinstance(deger_dugum, (ast.FloorDiv, ast.Div, ast.RShift)):
                        self.logaritmik_bolme_var = True
                        self.log_dongu_derinligi = max(self.log_dongu_derinligi, self.mevcut_derinlik)

        self.bulgular.append(f"Satır {node.lineno}: `{tur}` döngüsü tespit edildi (İç içe derinlik seviyesi: {self.mevcut_derinlik}).")
        self.generic_visit(node)
        self.mevcut_derinlik -= 1

    def visit_For(self, node):
        self._dongu_incele(node, "for")

    def visit_While(self, node):
        self._dongu_incele(node, "while")

    def visit_ListComp(self, node):
        self._dongu_incele(node, "List Comprehension")

    def visit_Call(self, node):
        # Özyineleme (Recursion) kontrolü
        if isinstance(node.func, ast.Name):
            if node.func.id == self.fonksiyon_adi:
                self.ozyineleme_sayisi += 1
                self.bulgular.append(f"Satır {node.lineno}: Özyinelemeli (Recursive) `{self.fonksiyon_adi}()` çağrısı tespit edildi.")
            elif node.func.id == "sorted":
                self.siralama_cagrisi_var = True
                self.bulgular.append(f"Satır {node.lineno}: `sorted()` fonksiyonu tespit edildi -> Timsort O(n log n).")
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr == "sort":
                self.siralama_cagrisi_var = True
                self.bulgular.append(f"Satır {node.lineno}: `.sort()` metodu tespit edildi -> Timsort O(n log n).")
        self.generic_visit(node)

    def teorik_karmasikligi_hesapla(self):
        if self.ozyineleme_sayisi >= 2:
            return "O(2^n)", "Çoklu özyineleme (dallanma) tespit edildi (Üstel Zaman)."
        if self.ozyineleme_sayisi == 1:
            return "O(n) veya O(log n)", "Tekil özyineleme (Linear veya Binary Recursion) tespit edildi."
        if self.maks_dongu_derinligi == 0:
            if self.siralama_cagrisi_var:
                return "O(n log n)", "Döngü yok ancak sıralama (Timsort) çağrısı var."
            return "O(1)", "Hiçbir döngü veya özyineleme tespit edilmedi (Sabit Zaman)."
        if self.maks_dongu_derinligi == 1:
            if self.logaritmik_bolme_var:
                return "O(log n)", "Tek döngü içinde adım aralığı bölünerek/katlanarak ilerliyor."
            if self.siralama_cagrisi_var:
                return "O(n² log n)", "Döngü içinde sıralama işlemi yapılıyor."
            return "O(n)", "Tek seviyeli doğrusal döngü tespit edildi."
        if self.maks_dongu_derinligi == 2:
            if self.logaritmik_bolme_var:
                return "O(n log n)", "İç içe 2 döngü var ancak biri logaritmik bölme yapıyor."
            return "O(n²)", "İç içe 2 tam döngü tespit edildi (Kuadratik Zaman)."
        if self.maks_dongu_derinligi == 3:
            return "O(n³)", "İç içe 3 döngü tespit edildi (Kübik Zaman)."
        return f"O(n^{self.maks_dongu_derinligi})", f"İç içe {self.maks_dongu_derinligi} seviyeli Polinom döngü tespit edildi."


# =====================================================================
# 2. MOTOR: DİNAMİK ÇALIŞMA ZAMANI VE BÜYÜME ORANI ÖLÇÜCÜ
# =====================================================================
def dinamik_performans_olc(kod_metni, tahmin_edilen_sinif):
    yerel_uzay = {}
    exec(kod_metni, {}, yerel_uzay)
    if "cozum" not in yerel_uzay:
        return None, "`cozum(n)` adında bir fonksiyon bulunamadı."

    fonksiyon = yerel_uzay["cozum"]

    # Karmaşıklık sınıfına göre sistemi kilitlemeyecek güvenli N boyutları seç
    if "2^n" in tahmin_edilen_sinif:
        n_degerleri = [10, 14, 18, 22, 25]
    elif "n³" in tahmin_edilen_sinif or "n^" in tahmin_edilen_sinif:
        n_degerleri = [10, 20, 40, 60, 80]
    elif "n²" in tahmin_edilen_sinif:
        n_degerleri = [100, 200, 400, 800, 1200]
    else:
        n_degerleri = [1000, 5000, 20000, 50000, 100000]

    sonuclar = []
    for n in n_degerleri:
        # Doğru ölçüm için 3 kez çalıştırıp en kararlı (en düşük) süreyi al
        sureler = []
        for _ in range(3):
            baslangic = time.perf_counter()
            fonksiyon(n)
            bitis = time.perf_counter()
            sureler.append((bitis - baslangic) * 1000)  # Milisaniye
        en_iyi_sure = min(sureler)
        sonuclar.append({"Girdi Boyutu (N)": n, "Çalışma Süresi (ms)": round(en_iyi_sure, 5)})

    return pd.DataFrame(sonuclar), None


# =====================================================================
# ARAYÜZ: KOD EDİTÖRÜ VE SONUÇ EKRANI
# =====================================================================
col_sol, col_sag = st.columns([1, 1])

with col_sol:
    st.subheader("📝 1. Analiz Edilecek Python Kodunu Girin")
    secilen_sablon = st.selectbox("Hazır Şablon Seçin veya Kendi Kodunuzu Yazın:", list(ORNEK_KODLAR.keys()))
    kullanici_kodu = st.text_area(
        "Fonksiyon adını `def cozum(n):` olarak bırakın:",
        value=ORNEK_KODLAR[secilen_sablon],
        height=240
    )
    analiz_butonu = st.button("🚀 Karmaşıklığı Hesapla ve Test Et", type="primary", use_container_width=True)

with col_sag:
    st.subheader("🔍 2. Statik AST Analizi Sonuçları")
    try:
        agac = ast.parse(kullanici_kodu)
        analizor = BigOAstAnalizor()
        analizor.visit(agac)
        teorik_big_o, aciklama = analizor.teorik_karmasikligi_hesapla()

        k1, k2 = st.columns(2)
        k1.metric("Teorik Zaman Karmaşıklığı", teorik_big_o)
        k2.metric("Maksimum Döngü Derinliği", f"{analizor.maks_dongu_derinligi} Seviye")

        st.success(f"**Analiz Kararı:** {aciklama}")

        with st.expander("🛠️ Kod İçinde Tespit Edilen Yapısal Bulgular (AST)", expanded=True):
            if analizor.bulgular:
                for b in analizor.bulgular:
                    st.markdown(f"- {b}")
            else:
                st.write("Döngü veya özyineleme bulunamadı, doğrudan sabit işlemler (`O(1)`) yürütülüyor.")

    except SyntaxError as e:
        st.error(f"Kodunuzda sözdizimi (Syntax) hatası var: Satır {e.lineno} - {e.msg}")
        st.stop()

st.divider()

# =====================================================================
# DİNAMİK PERFORMANS TESTİ VE BÜYÜME GRAFİĞİ
# =====================================================================
if analiz_butonu:
    st.subheader("📈 3. Gerçek Çalışma Zamanı (Ampirik) Testi ve Büyüme Grafiği")
    with st.spinner("Fonksiyon farklı N boyutlarıyla çalıştırılıp süreler ölçülüyor..."):
        df_sonuc, hata = dinamik_performans_olc(kullanici_kodu, teorik_big_o)

    if hata:
        st.error(hata)
    else:
        c_tablo, c_grafik = st.columns([1, 2])
        with c_tablo:
            st.markdown("**Ölçülen Süre Tablosu**")
            st.dataframe(df_sonuc, use_container_width=True, hide_index=True)

            # İlk ve son N arasındaki büyüme çarpanını hesapla
            n_orani = df_sonuc.iloc[-1]["Girdi Boyutu (N)"] / df_sonuc.iloc[0]["Girdi Boyutu (N)"]
            ilk_sure = max(df_sonuc.iloc[0]["Çalışma Süresi (ms)"], 0.00001)
            son_sure = df_sonuc.iloc[-1]["Çalışma Süresi (ms)"]
            sure_orani = son_sure / ilk_sure

            st.info(
                f"📊 **Büyüme Özeti:** Veri boyutu (`N`) **{n_orani:.0f} katına** çıktığında, "
                f"çalışma süresi **{sure_orani:.1f} katına** çıktı."
            )

        with c_grafik:
            st.markdown("**Girdi Boyutu (N) vs. Çalışma Süresi (ms) Eğrisi**")
            st.line_chart(df_sonuc.set_index("Girdi Boyutu (N)"))