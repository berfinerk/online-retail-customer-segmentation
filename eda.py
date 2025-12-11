import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "data/online_retail_II.xlsx"

df = pd.read_excel(file_path)

# print(df.head())
# print(df.shape)
# print(df.columns)
# print(df.dtypes)
# print(df.isnull().sum())

#1.costumer ıd boş olan satırları sil
#2.quantitiy < 0 olan satırları sil (iade ve hatalı kayıtlar)
#3. price<0 olan satırları sil (hataya uğramış fiyatlar)
#4. totalprice = quantity*price sütununu ekle
#5.son eksik değer ve shape kontrolü yap

#1 costumer ıd boş olan kayıtları silme (müşteri kimliği belli olmayan satırları temizle)
df = df.dropna(subset=["Customer ID"])
# print(df.shape)
#RFM müşteri analizi olduğu için kimliği belli olmayan müşterilerin siparişlerinden davranış çıkaramayız.

#2 quantity <0 olan satırları silme
#bu satırlar genelde iade(returns) anlamına gelir.
df = df[df["Quantity"] > 0]
# print(df.shape)
#negatid quantitiy= iade işlemi
#sıfır = hatalı kayıt
#rfm ve ml analizini bozar, o yüzden kaldırıyoruz.
#quantity, satış verilerinde satılan ürün adedi(miktarı) anlamına gelir.Yani bir müşteirnin tek bir alışverişte kaç ürün aldığını gösterir.
#eksik veri yok ama hatalı veri olabilir.

#3 price <0 olan satırları silme
#fiyatı 0 veya - değer olan satırlar geçersizdir.
df = df[df["Price"] > 0]
# print(df.shape)
# 0 tl veya negatif fiyat olmaz.Gerçek fiyat bilinmediği için düzeltilemez, analizden çıakrılır.

#totalprice = quantity*price ekleme
#bu sütun gerekiyor çünkü monetary(harcama) totalprice ile hesaplanacak
df["TotalPrice"] = df["Quantity"] * df["Price"]
# print(df[["Quantity", "Price","TotalPrice"]].head())
#rfm de monetary (m) = bir müşterinin yaptığı tüm totalprileın toplamı
#kontrol
# print(df.shape)

#temel istatistikler
# print("\ntoplam işlem sayısı:", len(df))
# print("toplam müşteri sayısı:", df["Customer ID"].nunique())
# print("toplam fatura sayısı:", df["Invoice"].nunique())
# print("toplam ciro:", df["TotalPrice"].sum())
# print("\nmüşteri başına ortalama harcama:",
#       df.groupby("Customer ID")["TotalPrice"].sum().mean())
# print("\nEn çok harcayan ilk 10 müşteri:")
# print(df.groupby("Customer ID")["TotalPrice"].sum()
#       .sort_values(ascending=False)
#       .head(10))

#ZAMAN ANALİZİ
#satış verilerini yıl ve aya göre gruplandırarak aylık toplam satışları hesaplandı.
df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
monthly_sales = df.groupby(["Year", "Month"])["TotalPrice"].sum().reset_index()
# print(monthly_sales.head())
#tabloyu kronolojik sıraya sokalım
monthly_sales = monthly_sales.sort_values(["Year","Month"])
# print(monthly_sales.head())
# print(df["Year"].unique())

#satışların zaman içindeki değişimi(ay bazında) göstermektedir.
#zaman etiketi(örn: 2010-1) tek bir string etiketine dönüştürdük
monthly_sales["YearMonth"] = monthly_sales["Year"].astype(str) + "-" + monthly_sales["Month"].astype(str)

plt.figure(figsize=(14,6))
plt.plot(monthly_sales["YearMonth"], monthly_sales["TotalPrice"],marker='o')

plt.xticks(rotation=90)
plt.title("Aylık Toplam Satış Trendleri")
plt.xlabel("Ay")
plt.ylabel("Toplam Satış (£)")
plt.tight_layout()
# plt.show()

#ülke bazında satışların hesaplanması
country_sales = df.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False)
# print(country_sales.head(10))
#ülke grafiği
top_countries = country_sales.head(10)
plt.figure(figsize=(10,6))
plt.bar(top_countries.index, top_countries.values)
plt.title("En Çok Satış Yapılan İlk 10 Ülke")
plt.xlabel("Ülke")
plt.ylabel("Toplam Satış (£)")
plt.xticks(rotation=45)
plt.tight_layout()

# plt.show()

#ürün analizi
#1. En çok satılan ürünler(quantity)
#ürün açıklamalarına göre grupluyor
#her ürünün toplam kaç adet satıldığını hesaplıyor
#en çok satan 10 ürünü listeliyor
#bu, miktar olarak en popüler ürün hangisi? sorusunu cevaplar
top_products_qty = df.groupby("Description")["Quantity"].sum().sort_values(ascending=False)
# print(top_products_qty.head(10))

#top10 quantity ( en çok satılan ilk 10 ürün)
top10_qty = top_products_qty.head(10)

plt.figure(figsize=(12,6))
plt.barh(top10_qty.index,top10_qty.values)
plt.title("En Çok Satılan İlk 10 Ürün (Quantity)")
plt.xlabel("Satılan Adet")
plt.ylabel("Ürün")
plt.tight_layout()
# plt.show()


#2.En çok gelir getiren ürünler(TotalPrice)
#hangi ürünün şirkete en çok para kazandırdığını gösterir.
#bazı ürünler çok satılır ama ucuz olduğu için ciro getirmez.
#bazı ürünler az satar ama pahalıdır, çok ciro getirir.
top_products_revenue = df.groupby("Description")["TotalPrice"].sum().sort_values(ascending=False)
# print(top_products_revenue.head(10))

#top 10 revenue ( en çok gelir getiren ilk 10 ürün)
top10_rev = top_products_revenue.head(10)

plt.figure(figsize=(12,6))
plt.barh(top10_rev.index, top10_rev.values)
plt.title("En Çok Gelir Getiren İlk 10 Ürün (Revenue)")
plt.xlabel("Toplam Gelir (£)")
plt.ylabel("Ürün")
plt.tight_layout()
# plt.show()

#Sayısal dağılım analizi
plt.figure(figsize=(14,4))

plt.subplot(1,3,1)
plt.hist(df["Quantity"], bins=40, color="skyblue", log=True)
plt.title("Quantity(Miktar) Dağılımı")

plt.subplot(1,3,2)
plt.hist(df["Price"], bins=40, color="lightgreen", log=True)
plt.title("Price(Fiyat) Dağılımı")

plt.subplot(1,3,3)
plt.hist(df["TotalPrice"], bins=40, color="salmon", log=True)
plt.title("TotalPrice(ToplamFiyat Dağılımı")

plt.tight_layout()
# plt.show()

#boxplot aykırı değer analizi
plt.figure(figsize=(12,4))

plt.subplot(1,3,1)
plt.boxplot(df["Quantity"], vert=True)
plt.title("Quantity(Miktar) Boxplot")

plt.subplot(1,3,2)
plt.boxplot(df["Price"], vert=True)
plt.title("Price(Fiyat) Boxplot")

plt.subplot(1,3,3)
plt.boxplot(df["TotalPrice"], vert=True)
plt.title("TotalPrice(ToplamFiyat Boxplot")
plt.tight_layout()
# plt.show()

#kolerasyon Matrisi(Heamap)
numeric_cols = ["Quantity", "Price", "TotalPrice"]
corr = df[numeric_cols].corr()

plt.figure(figsize=(6,4))
sns.heatmap(corr, annot=True, cmap="Blues", fmt=".2f")
plt.title("Quantity - Price - TotalPrice Korelasyon Matrisi")
plt.tight_layout()
# plt.show()

#ürün bazlı çok değişkenli analiz(bubble chart)
product_stats = df.groupby("Description").agg({
    "Quantity": "sum",
    "TotalPrice": "sum",
    "Price": "sum",
}).reset_index()

plt.figure(figsize=(10,6))

plt.scatter(
    product_stats["Quantity"],
    product_stats["TotalPrice"],
    s=product_stats["Price"] / 2,
    alpha=0.6,
    c=product_stats["Price"],
    cmap ="viridis"
)
plt.xlabel("Toplam Satış Adedi (Quantity)")
plt.ylabel("Toplam Ciro (TotalPrice)")
plt.title("Ürünlerde Quantity - Revenue - Price İlişkisi (Bubble Chart)")
plt.colorbar(label="Ortalama Fiyat")
plt.tight_layout()
# plt.show()

#RFM anallizi: Recency(YAKINLIK),Frequency(SIKLIK), Monetary(Para)
#Recency(R):Müşteri ne kadar süredir alışveriş yapamamış.
#InvoiceDate tarih tipinde mi emin olalım
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
#InvoiceDate sütunuu tarih/zaman tipine çevir

#RFM referans tarih: Genelde veri setindeki en son tarih +1 gün alınır.
snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
# print("Snapshot Date:", snapshot_date)

#her müşteri en son ne zaman alışveriş yapmış
#her müşteri için son alışveriş tarihini bulmak: Bu tarihten spanpshot_date i çıkarmak, aradaki gün farkını hesaplamak

#her müşteri için Recency hesaplama
recency_df = df.groupby("Customer ID").agg({
    "InvoiceDate": lambda x: (snapshot_date -x.max()).days
}).reset_index()
recency_df.rename(columns={"InvoiceDate": "Recency"}, inplace=True)
# print(recency_df.head())
# print(recency_df.describe())

#frequrncy hesaplama
#müşteri kaç kez alışveriş yaptı? Yani kaç farklı fatura kesmiş? bu yüzden ınvoice kolonu kullanıyoruz.
#frequency müşteri sadakati hakkında bilgi verir.
frequency_df = df.groupby("Customer ID")["Invoice"].nunique().reset_index()
frequency_df.rename(columns={"Invoice": "Frequency"}, inplace=True)
# print(frequency_df.head())
# print(frequency_df.describe())

#Monetary hesaplama mantığı
#her müşteri toplam ne kadar harcamış? Yani bu müşteri toplam kaç € harcamış.Bu metrik daha sonra en değerli müşterileri belirlemekte çok önemli
#monetary = toplam totalprice yani quantity * price ın toplamı zaten totalprice kolonu var.Şimdi bunu müşteri bazında özetleyeceğiz.
# TotalPrice = Quantity * Price olduğu için,bir müşterinin toplam harcamasını bulmak için sum() kullanıyoruz.
monetary_df = df.groupby("Customer ID")["TotalPrice"].sum().reset_index()
#kolon adını monetary yapıcaz
monetary_df.rename(columns={"TotalPrice": "Monetary"}, inplace=True)

# print(monetary_df.head())
# print(monetary_df.describe())

#RFM tablosunun oluşturulması
#recency ve frequency tablolarını customer ıd üzerinden birleştirmek
rfm = recency_df.merge(frequency_df, on="Customer ID")
#monetary tablosunu da ekle
rfm = rfm.merge(monetary_df, on="Customer ID")

# print(rfm.head())
# print(rfm.describe())
# print(rfm.shape)

#RFM SCORING (PUALAMA)

#recency skoru (küçük değer = yüksek puan)
rfm['R_Score'] = pd.qcut(rfm["Recency"], 5, labels=[5,4,3,2,1]).astype(int)

#frequency skoru(büyük değer=yüksek puan)
rfm['F_Score'] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)

#momentary skoru ( büyük değer = yüksek puan)
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5]).astype(int)

#rfm toplam skoru
rfm['RFM_Score'] = ( rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str) )

# print("\nRFM skorlaması tamamlandı. İlk 5 müşteri:")
# print(rfm[['Customer ID', 'Recency', 'Frequency', 'Monetary', 'R_Score', 'F_Score', 'M_Score', 'RFM_Score']].head())

#segment fonksiyonu
#rfm segment oluşturma
def segment_et(row):
    r =row['R_Score']
    f =row['F_Score']
    m = row['Monetary']

    #1)en değerli grup: champions
    if(r >= 4) and (f >= 4) and (m >= 4):
        return "Champions"

    #2) sadık müşteriler
    elif(r >= 3) and (f >=3):
        return " Loyal Champions"

    #3) potansiyel sadıklar (yeni ama iyi sinyal veriyor)
    elif(r >= 4) and (f <= 2):
        return "Potential Loyalist"

    #4) eskiden çok aktifmiş ama artık gelmiyor -> riskli
    elif(r <=2) and (f >= 4):
        return "At Risk"

    #5) hem az gelmiş, hem az kalmış, hem az harcamış -> kayıp / düşük değerli
    elif (r <=2) and (f<= 2) and (m <= 2):
        return "Lost"

    #6) diğer arada kalanlar
    else:
        return "Others"

#fonksiyonu tüm satırlara uygulayıp segment sütununu oluşturalım
rfm['Segment'] = rfm.apply(segment_et, axis=1)
print("\nSegment sütunu eklendi. İlk 10 müşteri:")
print(rfm[['Customer ID', 'R_Score', 'F_Score', 'M_Score', 'RFM_Score', 'Segment']].head(10))






















