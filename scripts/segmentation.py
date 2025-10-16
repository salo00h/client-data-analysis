import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ======================================
# 🧩 SEGMENTATION DES CLIENTS (Version locale)
# ======================================

# 📁 1) Lecture du fichier fusionné
chemin_fichier = r"C:\Users\Saleh\clien\Data\merge.xlsx"
df = pd.read_excel(chemin_fichier)

# 🧹 2) Nettoyage des types
df['montant'] = pd.to_numeric(df['montant'], errors='coerce')
df['revenu_annuel'] = pd.to_numeric(df['revenu_annuel'], errors='coerce')
df['âge'] = pd.to_numeric(df['âge'], errors='coerce')

# ======================================
# 🔢 3) Segmentation selon l’activité
# ======================================
cmds_par_client = df.groupby('id_client')['id_commande'].nunique().rename('nb_commandes')
clients_base = df[['id_client', 'nom', 'prénom', 'pays', 'ville', 'âge', 'revenu_annuel']].drop_duplicates('id_client')
clients_avec_act = clients_base.merge(cmds_par_client, left_on='id_client', right_index=True, how='left').fillna({'nb_commandes': 0})

def etiqueter_activite(n):
    n = int(n)
    if n == 0:
        return "Inactif"
    elif n == 1:
        return "Faible"
    elif 2 <= n <= 4:
        return "Moyen"
    else:
        return "Élevé"

clients_avec_act['segment_activité'] = clients_avec_act['nb_commandes'].apply(etiqueter_activite)

# ======================================
# 💶 4) Segmentation selon le revenu
# ======================================
revenus_valides = clients_avec_act['revenu_annuel'].dropna()
if len(revenus_valides) >= 3:
    q1, q2 = revenus_valides.quantile([0.33, 0.66]).values
else:
    q1, q2 = 30000, 60000

def etiqueter_revenu(x):
    if pd.isna(x):
        return "Inconnu"
    if x <= q1:
        return "Faible"
    elif x <= q2:
        return "Moyen"
    else:
        return "Élevé"

clients_avec_act['segment_revenu'] = clients_avec_act['revenu_annuel'].apply(etiqueter_revenu)

# ======================================
# 👤 5) Segmentation par âge
# ======================================
bins_age = [-np.inf, 24, 34, 44, 54, np.inf]
labels_age = ["<25", "25-34", "35-44", "45-54", "55+"]
clients_avec_act['segment_âge'] = pd.cut(clients_avec_act['âge'], bins=bins_age, labels=labels_age)

# ======================================
# 📈 6) Calcul des KPIs
# ======================================
paiements = df[['id_commande', 'id_paiement', 'confirmation', 'montant']].copy()
commandes = df[['id_commande', 'id_client', 'statut_commande', 'montant']].copy()

ca_par_commande = commandes.groupby('id_commande', as_index=False)['montant'].sum().rename(columns={'montant':'montant_commande'})
paiement_confirme_par_commande = paiements.groupby('id_commande').apply(
    lambda g: (g['confirmation'] == 'Confirmé').sum()
).rename('paiements_confirmes').reset_index()

resume_commande = ca_par_commande.merge(commandes[['id_commande','id_client']].drop_duplicates(),
                                        on='id_commande', how='left') \
                                 .merge(paiement_confirme_par_commande, on='id_commande', how='left') \
                                 .fillna({'paiements_confirmes': 0})

resume_commande = resume_commande.merge(
    clients_avec_act[['id_client','segment_activité','segment_revenu','segment_âge']],
    on='id_client', how='left'
)

def kpis_par_segment(df_seg, nom_segment):
    nb_clients = df_seg['id_client'].nunique()
    nb_cmds = df_seg['id_commande'].nunique()
    ca = df_seg['montant_commande'].sum()
    panier_moyen = ca / nb_cmds if nb_cmds > 0 else 0
    taux_pay_conf = ((df_seg['paiements_confirmes'] > 0).sum() / nb_cmds * 100) if nb_cmds > 0 else 0
    return pd.DataFrame({
        'segment': [nom_segment],
        'clients_uniques': [nb_clients],
        'commandes': [nb_cmds],
        'CA_total': [round(ca,2)],
        'panier_moyen': [round(panier_moyen,2)],
        'taux_paiement_confirmé_%': [round(taux_pay_conf,2)]
    })

# --- KPIs par activité
kpis_activite = pd.concat([
    kpis_par_segment(
        resume_commande[resume_commande['segment_activité']==seg],
        seg
    ) for seg in clients_avec_act['segment_activité'].dropna().unique()
])

# --- KPIs par revenu
kpis_revenu = pd.concat([
    kpis_par_segment(
        resume_commande[resume_commande['segment_revenu']==seg],
        seg
    ) for seg in clients_avec_act['segment_revenu'].dropna().unique()
])

# --- KPIs par âge
kpis_age = pd.concat([
    kpis_par_segment(
        resume_commande[resume_commande['segment_âge']==seg],
        seg
    ) for seg in clients_avec_act['segment_âge'].dropna().unique()
])

# ======================================
# 💾 7) Sauvegarde des résultats
# ======================================
fichier_sortie = r"C:\Users\Saleh\clien\Data\segmentation.xlsx"
with pd.ExcelWriter(fichier_sortie) as writer:
    clients_avec_act.to_excel(writer, sheet_name="Clients_Segmentés", index=False)
    kpis_activite.to_excel(writer, sheet_name="KPIs_Activité", index=False)
    kpis_revenu.to_excel(writer, sheet_name="KPIs_Revenu", index=False)
    kpis_age.to_excel(writer, sheet_name="KPIs_Âge", index=False)

# ======================================
# 📊 8) Visualisation
# ======================================
plt.figure(figsize=(8,4))
if not kpis_revenu.empty:
    plt.bar(kpis_revenu['segment'], kpis_revenu['CA_total'])
    plt.title("CA par segment de revenu")
    plt.xlabel("Segment de revenu")
    plt.ylabel("Chiffre d'affaires total (€)")
    plt.tight_layout()
    plt.savefig(r"C:\Users\Saleh\clien\images\ca_par_segment_revenu.png", dpi=300)
    plt.show()

plt.figure(figsize=(8,4))
if not kpis_activite.empty:
    ordre = ["Inactif", "Faible", "Moyen", "Élevé"]
    k2 = kpis_activite.copy()
    k2['ordre'] = k2['segment'].map({v:i for i,v in enumerate(ordre)})
    k2 = k2.sort_values('ordre')
    plt.bar(k2['segment'], k2['CA_total'])
    plt.title("CA par segment d’activité")
    plt.xlabel("Segment d’activité")
    plt.ylabel("Chiffre d'affaires total (€)")
    plt.tight_layout()
    plt.savefig(r"C:\Users\Saleh\clien\images\ca_par_segment_activite.png", dpi=300)
    plt.show()

plt.figure(figsize=(8,4))
if not kpis_age.empty:
    ordre_age = {"<25":0, "25-34":1, "35-44":2, "45-54":3, "55+":4}
    k3 = kpis_age.copy()
    k3['ordre'] = k3['segment'].map(ordre_age)
    k3 = k3.sort_values('ordre')
    plt.bar(k3['segment'], k3['CA_total'])
    plt.title("CA par segment d’âge")
    plt.xlabel("Segment d’âge")
    plt.ylabel("Chiffre d'affaires total (€)")
    plt.tight_layout()
    plt.savefig(r"C:\Users\Saleh\clien\images\ca_par_segment_age.png", dpi=300)
    plt.show()

print("✅ Fichier Excel enregistré :", fichier_sortie)
print("🖼️ Graphiques sauvegardés dans le même dossier.")
