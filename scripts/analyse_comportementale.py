import pandas as pd

# 📁 Lecture du fichier fusionné
path = r"C:\Users\Saleh\clien\Data\merge.xlsx"
df = pd.read_excel(path)

# 🧹 Nettoyage rapide
df['montant'] = pd.to_numeric(df['montant'], errors='coerce')
df['revenu_annuel'] = pd.to_numeric(df['revenu_annuel'], errors='coerce')

print("=== ANALYSE COMPORTEMENTALE DES CLIENTS ===\n")

# 1️⃣ Top clients
clients_top = (
    df.groupby(['id_client', 'nom', 'prénom'])['montant']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print("🏆 Top 10 des clients les plus dépensiers :\n", clients_top, "\n")

# 2️⃣ Dépenses moyennes par pays
depenses_pays = (
    df.groupby('pays')['montant']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)
print("🌍 Dépense moyenne par pays :\n", depenses_pays, "\n")

# 3️⃣ Dépenses moyennes par ville
depenses_ville = (
    df.groupby('ville')['montant']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)
print("🏙️ Dépense moyenne par ville :\n", depenses_ville, "\n")

# 4️⃣ Corrélation
depense_par_client = (
    df.groupby('id_client')[['revenu_annuel', 'montant']]
    .sum()
    .dropna()
)
correlation = depense_par_client['revenu_annuel'].corr(depense_par_client['montant'])
print(f"📈 Corrélation entre le revenu annuel et le montant dépensé : {correlation:.3f}\n")

# ⚙️ Sheet pour la corrélation
corr_df = pd.DataFrame({
    "Indicateur": ["Corrélation revenu / dépense"],
    "Valeur": [round(correlation, 3)]
})

# 5️⃣ Sauvegarde complète
with pd.ExcelWriter(r"C:\Users\Saleh\clien\Data\analyse_comportementale.xlsx") as writer:
    clients_top.to_excel(writer, sheet_name="Top_Clients")
    depenses_pays.to_excel(writer, sheet_name="Depenses_Pays")
    depenses_ville.to_excel(writer, sheet_name="Depenses_Ville")
    depense_par_client.to_excel(writer, sheet_name="Depense_vs_Revenu")
    corr_df.to_excel(writer, sheet_name="Correlation", index=False)

print("✅ Rapport d'analyse comportementale enregistré : analyse_comportementale.xlsx")
