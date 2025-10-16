import pandas as pd

# 📁 Lecture du fichier fusionné
path = r"C:\Users\Saleh\clien\Data\merge.xlsx"
df = pd.read_excel(path)

# ================================
# 📊 ANALYSE DE PERFORMANCE COMMERCIALE
# ================================

print("=== ANALYSE DE PERFORMANCE COMMERCIALE ===\n")

# 💰 1️⃣ Chiffre d’affaires total (CA)
df['montant'] = pd.to_numeric(df['montant'], errors='coerce')
ca_total = df['montant'].sum()
print(f"💰 Chiffre d’affaires total : {ca_total:.2f} €")

# 📦 2️⃣ Nombre total de commandes
nb_commandes = df['id_commande'].nunique()
print(f"📦 Nombre total de commandes : {nb_commandes}")

# 🚚 3️⃣ Répartition des statuts de commandes
statuts = df['statut_commande'].value_counts()
print("\n📊 Répartition des statuts de commandes :")
print(statuts)

# 📦 4️⃣ Taux de commandes livrées
nb_livrees = df[df['statut_commande'] == 'Livrée']['id_commande'].nunique()
taux_livrees = (nb_livrees / nb_commandes) * 100
print(f"\n🚀 Taux de commandes livrées : {taux_livrees:.2f}%")

# ❌ 5️⃣ Taux d’annulation
nb_annulees = df[df['statut_commande'] == 'Annulée']['id_commande'].nunique()
taux_annulees = (nb_annulees / nb_commandes) * 100
print(f"❌ Taux d’annulation : {taux_annulees:.2f}%")

# 💳 6️⃣ Taux de paiement confirmé
taux_paiement_confirme = (
    df[df['confirmation'] == 'Confirmé']['id_paiement'].count() / df['id_paiement'].count()
) * 100
print(f"💳 Taux de paiement confirmé : {taux_paiement_confirme:.2f}%")

# 📈 7️⃣ Montant moyen par commande
montant_moyen = df.groupby('id_commande')['montant'].sum().mean()
print(f"📈 Montant moyen par commande : {montant_moyen:.2f} €")

# ================================
# 💾 Sauvegarde du rapport de performance
# ================================

rapport = {
    'Indicateur': [
        'Chiffre d’affaires total (€)',
        'Nombre total de commandes',
        'Taux de commandes livrées (%)',
        'Taux d’annulation (%)',
        'Taux de paiement confirmé (%)',
        'Montant moyen par commande (€)'
    ],
    'Valeur': [
        round(ca_total, 2),
        nb_commandes,
        round(taux_livrees, 2),
        round(taux_annulees, 2),
        round(taux_paiement_confirme, 2),
        round(montant_moyen, 2)
    ]
}

rapport_df = pd.DataFrame(rapport)
rapport_df.to_excel(r"C:\Users\Saleh\clien\Data\performance_commerciale.xlsx", index=False)

print("\n✅ Rapport de performance commerciale sauvegardé : performance_commerciale.xlsx")
