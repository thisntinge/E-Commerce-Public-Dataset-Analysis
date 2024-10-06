import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

order_items_url = "https://raw.githubusercontent.com/thisntinge/E-Commerce-Public-Dataset-Analysis/refs/heads/main/data/order_items_dataset.csv"
order_items_dataset_df = pd.read_csv(order_items_url)

order_payments_url = "https://raw.githubusercontent.com/thisntinge/E-Commerce-Public-Dataset-Analysis/refs/heads/main/data/order_payments_dataset.csv"
order_payments_dataset_df = pd.read_csv(order_payments_url)

st.sidebar.title("Proyek Analisis Data E-Commerce Sharing Dataset")
st.sidebar.subheader("\n\n\n\n\n")
st.sidebar.write("Inge Najwa Aqiilah")
st.sidebar.write("inge.najwaa@student.uns.ac.id")
st.sidebar.write("ingenajwa")

st.title("Top 10 Sellers by Freight Value")

freight_cost_by_seller = order_items_dataset_df.groupby("seller_id").agg({
    "freight_value": "sum"
}).reset_index()

top_10_sellers = freight_cost_by_seller.sort_values(by="freight_value", ascending=False).head(10)

plt.figure(figsize=(10, 6))
colors = ['#08306b'] + ['#deebf7'] * 9
sns.barplot(x="freight_value", y="seller_id", data=top_10_sellers, palette=colors)

plt.title("Top 10 Sellers by Freight Value", fontsize=16)
plt.xlabel("Total Freight Value", fontsize=12)
plt.ylabel("Seller ID", fontsize=12)

st.pyplot(plt)

highest_freight_seller = top_10_sellers.iloc[0]
seller_id = highest_freight_seller['seller_id']
freight_value = highest_freight_seller['freight_value']

st.markdown(f"**Kesimpulan:** Seller dengan ID '{seller_id}' telah mengeluarkan biaya ongkos kirim tertinggi, yaitu sebesar **{freight_value:.2f}**.")

st.title("Total Customers by Payment Type")

pivot_table = order_payments_dataset_df.groupby("payment_type").agg({
    "payment_type": "count"
}).rename(columns={"payment_type": "Total Customers"})

df_for_visualization = pivot_table.reset_index()

colors = ['#08306b' if payment == 'credit_card' else '#deebf7' for payment in df_for_visualization['payment_type']]

plt.figure(figsize=(8, 5))
sns.barplot(x="payment_type", y="Total Customers", data=df_for_visualization, palette=colors)

plt.title("Total Customers by Payment Type", fontsize=14)
plt.xlabel("Payment Type", fontsize=12)
plt.ylabel("Total Customers", fontsize=12)
plt.xticks(rotation=45)

st.pyplot(plt)

credit_card_customers = pivot_table.loc[pivot_table.index == 'credit_card', 'Total Customers'].values[0]

st.markdown(f"**Kesimpulan:** Pembayaran menggunakan **kartu kredit** adalah metode yang paling banyak digunakan dengan total **{credit_card_customers}** pelanggan yang memilih metode ini.")

st.title("Rata-rata Cicilan oleh Pengguna Kartu Kredit")

credit_card_payments = order_payments_dataset_df[order_payments_dataset_df['payment_type'] == 'credit_card']

average_installments = credit_card_payments['payment_installments'].mean()

st.markdown(f"Rata-rata cicilan yang diambil oleh customer ketika menggunakan kartu kredit adalah: **{average_installments:.2f} kali**.")

st.latex(r'''
\text{Rata-rata Cicilan} = \frac{\sum_{i=1}^{n} x_i}{n}
''')

st.markdown("""
Dimana:
- \(x_i\) adalah jumlah cicilan yang diambil oleh masing-masing customer.
- \(n\) adalah total customer yang menggunakan kartu kredit sebagai metode pembayaran.
""")