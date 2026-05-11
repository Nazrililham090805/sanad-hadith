import pandas as pd
import networkx as nx
from datetime import datetime

# =========================
# GLOBAL PROGRESS
# =========================
progress = 0

def log(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg} | Progress: {progress}%")

def update_progress(value):
    global progress
    progress = value


# =========================
# LOAD DATA
# =========================
update_progress(5)
log("Load data edges")

edges_path = "data/processed/edges.csv"
edges_df = pd.read_csv(edges_path)

update_progress(15)
log(f"Data berhasil dibaca | Jumlah edges: {len(edges_df)}")


# =========================
# BUILD DIRECTED GRAPH
# Edge: Student → Teacher
# artinya: Student menerima riwayat dari Teacher
# =========================
log("Membangun directed graph")

G = nx.from_pandas_edgelist(
    edges_df,
    source='Student',
    target='Teacher',
    edge_attr='Weight',
    create_using=nx.DiGraph()
)

update_progress(35)
log(f"Graph selesai | Nodes: {G.number_of_nodes()} | Edges: {G.number_of_edges()}")


# =========================
# IN-DEGREE CENTRALITY
# Peran Perawi sebagai GURU
# In-degree = berapa banyak murid yang meriwayatkan DARI perawi ini
# Edge masuk ke node = murid yang menuju ke guru ini
# Perawi dengan in-degree tinggi = otoritas sebagai sumber riwayat
# =========================
log("Menghitung In-Degree Centrality (peran sebagai Guru)")

in_degree_raw = dict(G.in_degree())          # jumlah mentah (count)
in_degree_centrality = nx.in_degree_centrality(G)  # dinormalisasi 0–1

update_progress(55)
log("In-Degree selesai")


# =========================
# OUT-DEGREE CENTRALITY
# Peran Perawi sebagai MURID
# Out-degree = berapa banyak guru yang diriwayatkan OLEH perawi ini
# Edge keluar dari node = guru-guru yang dituju murid ini
# Perawi dengan out-degree tinggi = luas dalam meriwayatkan hadis
# =========================
log("Menghitung Out-Degree Centrality (peran sebagai Murid)")

out_degree_raw = dict(G.out_degree())        # jumlah mentah (count)
out_degree_centrality = nx.out_degree_centrality(G)  # dinormalisasi 0–1

update_progress(75)
log("Out-Degree selesai")


# =========================
# COMBINE
# =========================
log("Menggabungkan hasil")

centrality_df = pd.DataFrame({
    'Narrator'              : list(G.nodes),

    # --- Peran sebagai GURU ---
    'In_Degree_Count'       : [in_degree_raw.get(n, 0) for n in G.nodes],
    'In_Degree_Centrality'  : [round(in_degree_centrality.get(n, 0), 6) for n in G.nodes],

    # --- Peran sebagai MURID ---
    'Out_Degree_Count'      : [out_degree_raw.get(n, 0) for n in G.nodes],
    'Out_Degree_Centrality' : [round(out_degree_centrality.get(n, 0), 6) for n in G.nodes],
})

update_progress(90)
log("Data siap disimpan")


# =========================
# TOP RESULT
# =========================
print("\n" + "="*55)
print("TOP 10 — IN-DEGREE (Perawi paling banyak dijadikan Guru)")
print("="*55)
print(
    centrality_df[['Narrator', 'In_Degree_Count', 'In_Degree_Centrality']]
    .sort_values(by='In_Degree_Centrality', ascending=False)
    .head(10)
    .to_string(index=False)
)

print("\n" + "="*55)
print("TOP 10 — OUT-DEGREE (Perawi paling banyak meriwayatkan)")
print("="*55)
print(
    centrality_df[['Narrator', 'Out_Degree_Count', 'Out_Degree_Centrality']]
    .sort_values(by='Out_Degree_Centrality', ascending=False)
    .head(10)
    .to_string(index=False)
)


# =========================
# SAVE
# =========================
output_path = "data/processed/centrality_degree.csv"
centrality_df.to_csv(output_path, index=False, encoding='utf-8-sig')

update_progress(100)
log(f"Selesai 🚀 | Disimpan ke: {output_path}")