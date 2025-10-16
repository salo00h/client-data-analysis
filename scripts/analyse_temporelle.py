import pandas as pd
import matplotlib.pyplot as plt

# 📁 Lecture du fichier fusionné
path = r"C:\Users\Saleh\clien\Data\merge.xlsx"
df = pd.read_excel(path)

# ================================
# 🕒 ANALYSE TEMPORELLE DES VENTES
# ================================

print("=== ANALYSE TEMPORELLE DES VENTES ===\n")

# 🧹 1️⃣ Nettoyage et préparation des dates
df['date_commande'] = pd.to_datetime(df['date_commande'], errors='coerce')
df['date_paiement'] = pd.to_datetime(df['date_paiement'], errors='coerce')

# 💰 2️⃣ Calcul du montant total par mois (CA mensuel)
df['mois'] = df['date_commande'].dt.to_period('M')
ventes_mensuelles = df.groupby('mois')['montant'].sum()

print("📅 Chiffre d’affaires par mois :\n", ventes_mensuelles, "\n")

# 📈 3️⃣ Création d’un graphique de tendance mensuelle
plt.figure(figsize=(10,5))
ventes_mensuelles.plot(kind='line', marker='o')
plt.title("📊 Évolution mensuelle du chiffre d’affaires")
plt.xlabel("Mois")
plt.ylabel("Montant total (€)")
plt.grid(True)
plt.tight_layout()
plt.savefig(r"C:\Users\Saleh\clien\images\ventes_mensuelles.png", dpi=300)
plt.show()

# 🌦️ 4️⃣ Analyse par saison (trimestre)
df['trimestre'] = df['date_commande'].dt.to_period('Q')
ventes_trimestrielles = df.groupby('trimestre')['montant'].sum()

print("🌤️ Chiffre d’affaires par trimestre :\n", ventes_trimestrielles, "\n")

# 📊 5️⃣ Graphique du chiffre d’affaires par trimestre
plt.figure(figsize=(8,4))
ventes_trimestrielles.plot(kind='bar', color='skyblue')
plt.title("Chiffre d’affaires par trimestre")
plt.xlabel("Trimestre")
plt.ylabel("Montant total (€)")
plt.tight_layout()
plt.savefig(r"C:\Users\Saleh\clien\images\ventes_trimestrielles.png", dpi=300)
plt.show()

# 💾 6️⃣ Sauvegarde des données temporelles
with pd.ExcelWriter(r"C:\Users\Saleh\clien\analyse_temporelle.xlsx") as writer:
    ventes_mensuelles.to_excel(writer, sheet_name="Ventes_Mensuelles")
    ventes_trimestrielles.to_excel(writer, sheet_name="Ventes_Trimestrielles")

print("✅ Rapport temporel sauvegardé : analyse_temporelle.xlsx")
