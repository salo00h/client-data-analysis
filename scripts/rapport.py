import pandas as pd

# 📁 Lecture du fichier fusionné
path = r"C:\Users\Saleh\clien\Data\merge.xlsx"
df = pd.read_excel(path)

# 🔎 Aperçu général
print("=== APERÇU GÉNÉRAL ===")
print(df.head(5))
print("\nNombre total de lignes :", len(df))
print("Nombre total de colonnes :", len(df.columns))

# 📊 Statistiques descriptives de base
print("\n=== STATISTIQUES DESCRIPTIVES ===")
print(df.describe())

# 👥 Nombre de clients uniques
nb_clients = df['id_client'].nunique()
print("\nNombre de clients uniques :", nb_clients)

# 📦 Nombre de commandes et paiements
nb_commandes = df['id_commande'].nunique()
nb_paiements = df['id_paiement'].nunique()
print("Nombre total de commandes :", nb_commandes)
print("Nombre total de paiements :", nb_paiements)

# 💰 Total et moyenne des montants payés
total_montant = df['montant'].sum()
moyenne_montant = df['montant'].mean()
print("\nMontant total payé :", round(total_montant, 2))
print("Montant moyen payé :", round(moyenne_montant, 2))

# 🌍 Répartition des ventes par pays
ventes_pays = df.groupby('pays')['montant'].sum().sort_values(ascending=False)
print("\n=== VENTES PAR PAYS ===")
print(ventes_pays.head(10))

# 🧾 Statut des commandes
statuts = df['statut_commande'].value_counts()
print("\n=== STATUTS DES COMMANDES ===")
print(statuts)

# 🔥 Taux de commandes payées vs non payées
nb_non_payees = df['montant'].isnull().sum()
taux_non_payees = (nb_non_payees / len(df)) * 100
print(f"\nTaux de commandes non payées : {taux_non_payees:.2f}%")

# 💾 Sauvegarde du rapport résumé dans Excel
rapport = {
    'Indicateur': ['Clients uniques', 'Commandes', 'Paiements', 
                   'Montant total', 'Montant moyen', 'Taux non payées (%)'],
    'Valeur': [nb_clients, nb_commandes, nb_paiements, 
               round(total_montant,2), round(moyenne_montant,2), round(taux_non_payees,2)]
}

rapport_df = pd.DataFrame(rapport)
rapport_df.to_excel(r"C:\Users\Saleh\clien\Data\rapport.xlsx", index=False)

print("\n✅ Rapport sauvegardé sous : rapport.xlsx")
