import pandas as pd

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






















