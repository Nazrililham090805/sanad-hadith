import pandas as pd
import ast
import re

# =========================
# LOAD CLEANED DATA
# =========================

hasil2 = pd.read_csv(
    'sanadset_cleaned.csv',
    header=0
)

hasil2['Sanad_no_harakat'] = hasil2['Sanad_no_harakat'].apply(
    ast.literal_eval
)

print(hasil2.shape)

# =========================
# EXPLODE SANAD
# =========================

sanad_exploded = hasil2.explode('Sanad_no_harakat')

print(sanad_exploded.shape)

# =========================
# EXTRACT RELATIONS
# =========================

print('Ekstraksi relasi guru-murid...')

edges = []

for i, sanad in enumerate(hasil2['Sanad_no_harakat']):

    if isinstance(sanad, list):

        for j in range(len(sanad) - 1):

            murid = sanad[j]
            guru = sanad[j + 1]

            edges.append((murid, guru))

    if i % 10000 == 0:
        print(f'Progress: {i}')

# =========================
# DATAFRAME EDGES
# =========================

df_edges = pd.DataFrame(
    edges,
    columns=['Murid', 'Guru']
)

print(df_edges.head())

# =========================
# REMOVE SELF LOOP
# =========================

df_edges = df_edges[
    df_edges['Murid'] != df_edges['Guru']
]

# =========================
# CLEAN SYMBOLS
# =========================

pattern = r'[,،#()=\"{}\-\?\.:\|]+|<IDF>|</IDF>'

for col in ['Murid', 'Guru']:

    df_edges[col] = (
        df_edges[col]
        .astype(str)
        .str.replace(pattern, '', regex=True)
    )

# =========================
# DROP NULL
# =========================

df_edges = df_edges.dropna(
    subset=['Murid', 'Guru']
)

# =========================
# REMOVE NUMBERS
# =========================

df_edges = df_edges[
    ~df_edges['Murid'].str.contains(r'\d', na=False) &
    ~df_edges['Guru'].str.contains(r'\d', na=False)
]

# =========================
# REMOVE NARRATION WORDS
# =========================

hapus_kata = [
    'ثنا',
    'حدثنا',
    'قال حدثنا',
    'وقال',
    'عن'
]

for kata in hapus_kata:

    df_edges = df_edges[
        (df_edges['Murid'] != kata) &
        (df_edges['Guru'] != kata)
    ]

# =========================
# WEIGHTED EDGES
# =========================

df_edges_weighted = (
    df_edges
    .groupby(['Murid', 'Guru'])
    .size()
    .reset_index(name='weight')
)

df_edges_weighted['inv_weight'] = (
    df_edges_weighted['weight']
    .apply(lambda x: 1/x if x > 0 else 0)
)

# =========================
# CLEAN TEXT
# =========================

def clean_text(s):

    if pd.isna(s):
        return s

    s = str(s).strip()
    s = re.sub(r'\s+', ' ', s)

    return s

df_edges_weighted['Murid'] = (
    df_edges_weighted['Murid']
    .apply(clean_text)
)

df_edges_weighted['Guru'] = (
    df_edges_weighted['Guru']
    .apply(clean_text)
)

# =========================
# DROP NULL
# =========================

df_edges_weighted.dropna(inplace=True)

print(df_edges_weighted.shape)

# =========================
# SAVE EDGES
# =========================

df_edges_weighted.to_csv(
    'edges.csv',
    index=False,
    encoding='utf-8-sig'
)

print('edges.csv berhasil disimpan')