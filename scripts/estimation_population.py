import pandas as pd

# ======================================
# 📊 ESTIMATION DE LA POPULATION TOTALE
# - Source : merge.xlsx
# - Objectif : estimer la population totale du marché
# ======================================

# 📁 Lecture du fichier fusionné
chemin = r"C:\Users\Saleh\clien\Data\merge.xlsx"
df = pd.read_excel(chemin)

# 🧹 Nettoyage rapide
df['montant'] = pd.to_numeric(df['montant'], errors='coerce')

# ======================================
# 1️⃣ Calcul du taux d’activité moyen observé
# ======================================
# On considère qu’un client actif est celui qui a au moins une commande
clients_commandes = df.groupby('id_client')['id_commande'].nunique()
nb_clients_total = df['id_client'].nunique()
nb_clients_actifs = (clients_commandes > 0).sum()

taux_activite_moyen = nb_clients_actifs / nb_clients_total
print(f"👥 Taux d’activité moyen observé : {taux_activite_moyen*100:.2f}%")

# ======================================
# 2️⃣ Total des commandes observées
# ======================================
total_commandes = df['id_commande'].nunique()
print(f"📦 Total des commandes observées : {total_commandes}")

# ======================================
# 3️⃣ Estimation de la population totale
# ======================================
population_estimee = total_commandes / taux_activite_moyen
print(f"📈 Population totale estimée : {round(population_estimee):,}")

# ======================================
# 4️⃣ Sauvegarde du résultat dans Excel
# ======================================
rapport = pd.DataFrame({
    'Indicateur': ['Nombre clients (échantillon)',
                   'Clients actifs',
                   'Taux d’activité moyen',
                   'Commandes observées',
                   'Population totale estimée'],
    'Valeur': [nb_clients_total,
               nb_clients_actifs,
               round(taux_activite_moyen*100,2),
               total_commandes,
               round(population_estimee)]
})

rapport.to_excel(r"C:\Users\Saleh\clien\Data\population_estimee.xlsx", index=False)
print("✅ Rapport enregistré sous : population_estimee.xlsx")
