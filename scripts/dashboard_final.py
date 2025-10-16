import pandas as pd
import matplotlib.pyplot as plt

# ======================================
# 📊 TABLEAU DE BORD ANALYTIQUE GLOBAL
# - Source : merge.xlsx
# - Sorties : dashboard.xlsx + graphiques
# ======================================

# 📁 1) Lecture du fichier principal
chemin = r"C:\Users\Saleh\clien\Data\merge.xlsx"
df = pd.read_excel(chemin)

# 🧹 2) Nettoyage des types
df['montant'] = pd.to_numeric(df['montant'], errors='coerce')
df['date_commande'] = pd.to_datetime(df['date_commande'], errors='coerce')

# ======================================
# 🔹 3) Indicateurs de base (KPIs)
# ======================================
nb_clients = df['id_client'].nunique()
nb_commandes = df['id_commande'].nunique()
ca_total = df['montant'].sum()
moyenne = df['montant'].mean()

# ======================================
# 🌍 4) Ventes par pays
ventes_pays = df.groupby('pays')['montant'].sum().sort_values(ascending=False).head(10)

# 💳 5) Taux de paiement confirmé
total_paiements = len(df['id_paiement'].dropna())
confirmes = len(df[df['confirmation'] == 'Confirmé'])
taux_paiement_confirme = (confirmes / total_paiements * 100) if total_paiements > 0 else 0

# 🧑‍🤝‍🧑 6) Clients les plus actifs
clients_actifs = df.groupby('id_client')['id_commande'].nunique().sort_values(ascending=False).head(10)

# ======================================
# 📈 7) Graphiques
# ======================================

# Graphique 1 : Ventes par pays
plt.figure(figsize=(10,5))
ventes_pays.plot(kind='bar')
plt.title("Top 10 - Chiffre d’affaires par pays")
plt.xlabel("Pays")
plt.ylabel("Montant total (€)")
plt.tight_layout()
plt.savefig(r"C:\Users\Saleh\clien\images\ventes_par_pays.png")
plt.show()

# Graphique 2 : Clients les plus actifs
plt.figure(figsize=(10,5))
clients_actifs.plot(kind='bar', color='orange')
plt.title("Top 10 - Clients les plus actifs (nombre de commandes)")
plt.xlabel("ID Client")
plt.ylabel("Nombre de commandes")
plt.tight_layout()
plt.savefig(r"C:\Users\Saleh\clien\images\clients_actifs.png")
plt.show()

# ======================================
# 💾 8) Sauvegarde du rapport Excel
# ======================================
dashboard = pd.DataFrame({
    'Indicateur': [
        'Nombre de clients uniques',
        'Nombre total de commandes',
        'Chiffre d’affaires total (€)',
        'Montant moyen par commande (€)',
        'Taux de paiement confirmé (%)'
    ],
    'Valeur': [
        nb_clients,
        nb_commandes,
        round(ca_total,2),
        round(moyenne,2),
        round(taux_paiement_confirme,2)
    ]
})

with pd.ExcelWriter(r"C:\Users\Saleh\clien\Data\dashboard.xlsx") as writer:
    dashboard.to_excel(writer, sheet_name="KPIs", index=False)
    ventes_pays.to_excel(writer, sheet_name="Ventes_par_Pays")
    clients_actifs.to_excel(writer, sheet_name="Clients_Actifs")

print("✅ Tableau de bord enregistré sous : dashboard.xlsx")
print("📊 Graphiques enregistrés : ventes_par_pays.png, clients_actifs.png")
