import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


file_path = "data/online_retail_II.xlsx"
df= pd.read_excel(file_path)

#müşteri ID boşsa sil
df = df.dropna(subset=["Customer ID"])

#iade ve hatalı kayıtları çıkar
df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]

#toplam harcama
df["TotalPrice"] = df["Quantity"] * df["Price"]

#tarihleri hazırla
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

#rfm'yi müşteri bazında oluştur
rfm = df.groupby("Customer ID").agg({
    "InvoiceDate": lambda x: (snapshot_date - x.max()).days, #Recency
    "Invoice": "nunique",                                    #Frequency
    "TotalPrice": "sum"                                      #Monetary
}).reset_index()

rfm.columns = ["Customer ID", "Recency", "Frequency", "Monetary"]
# print(rfm.head())
# print(rfm.describe())

#aykırı değerleri yumuşatma(ML'e hazırlık)
#monetary ve frequency çok çarpık, k-means mesafeye duyarlı, silmeden etkisini sınırlıyoruz.

#alt%1 ve üst %99 dışını sınırlandırıyoruz.
#adım1: aykırı değerleri yumuşatma(%1 - %99)
for col in ["Recency", "Frequency", "Monetary"]:
    lower = rfm[col].quantile(0.01)
    upper = rfm[col].quantile(0.99)

    rfm[col] = np.where(rfm[col] < lower, lower, rfm[col])
    rfm[col] = np.where(rfm[col] > upper, upper, rfm[col])
#kontrol
# print(rfm.describe())

#ölçeklendirme(k-means için zorunlu)
#monetary >> Frequency >> Recency
#ölçeklenmezse k-means paraya göre kümeler
#ölçeklendirme
X = rfm[["Recency", "Frequency", "Monetary"]]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# print(X_scaled[:5])

#elbow method ( k adaylarını bulacağız)

wcss = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(8,5))
plt.plot(list(K_range), wcss, marker="o")
plt.xlabel("K (Küme Sayısı)")
plt.ylabel("WCSS")
plt.title("Elbow Method")
plt.tight_layout()
# plt.show()

#silhouette skorlarını hesapla(kararın doğru olup olamdığına bakıyoruz)
for k in range(2, 7):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
    labels = kmeans.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    # print(f"K={k} için Silhouette Score: {score:.3f}")

#k-means uygula(artık model kuruyoruz)
#final k-means modeli (k=4)
best_k =4

kmeans = KMeans(n_clusters=best_k, random_state=42, n_init="auto")
rfm["Cluster"] = kmeans.fit_predict(X_scaled)

#kontrol
# print(rfm["Cluster"].value_counts().sort_index())
# print(rfm.head())

#cluster profillerini çıkar(ortalamalar)
#cluster profillerini çıkarma(ortalama RFM değerleri)

cluster_summary = (
    rfm.groupby("Cluster")[["Recency", "Frequency", "Monetary"]]
    .mean()
    .round(2)
)

cluster_counts = rfm["Cluster"].value_counts().sort_index()

# print("Cluster ortalamaları:\n", cluster_summary)
# print("\nCluster müşteri sayıları:\n", cluster_counts)

#cluster'lara isim veriyoruz
#bu segmentasyonun tamamlandığı an
# K-Means cluster profilleri:
# Cluster 2 → Champions (çok yakın zamanda, çok sık alışveriş yapan ve yüksek harcama yapan müşteriler)
# Cluster 3 → Loyal Customers (yakın zamanda alışveriş yapan, sık ve yüksek harcama yapan sadık müşteriler)
# Cluster 0 → Regular Customers (orta seviyede alışveriş yapan, ana müşteri kitlesi)
# Cluster 1 → At Risk Customers (uzun süredir alışveriş yapmayan, kaybedilme riski taşıyan müşteriler)

#cluster'lara anlamlı segment isimleri verme
segment_map = {
    0: "Regular Customers", #orta seviye, ana kitle
    1: "At Risk Customers", #uzun süredir gelmeyen
    2: "Champions",         #Çok yakın, çok sık, çok harcayan
    3:"Loyal Customers",    #yakın, sık, yüksek harcayan
}
rfm["Segment_KMeans"] = rfm["Cluster"].map(segment_map)
#kontrol
print(rfm[["Customer ID", "Cluster", "Segment_KMeans"]].head())

segment_summary = (
    rfm.groupby("Segment_KMeans")[["Recency", "Frequency", "Monetary"]]
    .mean()
    .round(2)
)
print(segment_summary)

