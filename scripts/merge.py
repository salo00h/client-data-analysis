import pandas as pd

# 📁 تحديد المسار
path = r"C:\Users\Saleh\clien\Data"

# 📘 قراءة الملفات
clients = pd.read_excel(f"{path}\\clients.xlsx")
commandes = pd.read_excel(f"{path}\\commandes.xlsx")
paiements = pd.read_excel(f"{path}\\paiements.xlsx")

# 🔗 الدمج
# 1️⃣ ربط commandes مع clients
merged_1 = pd.merge(commandes, clients, on="id_client", how="left")

# 2️⃣ ربط الناتج مع paiements
merged_final = pd.merge(merged_1, paiements, on="id_commande", how="left")

# 💾 حفظ الملف النهائي في نفس المجلد
merged_final.to_excel(f"{path}\\merge.xlsx", index=False)

print("✅ تم الدمج بنجاح! تم إنشاء الملف merge.xlsx في نفس المجلد.")
