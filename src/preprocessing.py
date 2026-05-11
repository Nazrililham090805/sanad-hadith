import pandas as pd
import ast
import re

# =========================
# LOAD DATASET
# =========================

file_path = "data/raw/sanadset.csv"

df0 = pd.read_csv(
    file_path,
    header=None,
    encoding='utf-8',
    engine='python',
    on_bad_lines='skip'
)

if len(df0.columns) >= 2:
    df0.columns = ['Hadith', 'Sanad']

print(df0.info())

# =========================
# FILTER DATA
# =========================

df0 = df0[df0['Sanad'] != 'No SANAD'].copy()

print(df0.head())

# =========================
# SAFE LITERAL EVAL
# =========================

def safe_literal_eval(val):
    try:
        return ast.literal_eval(val)
    except:
        return val

if isinstance(df0['Sanad'].iloc[0], str):
    df0['Sanad'] = df0['Sanad'].apply(safe_literal_eval)

# =========================
# REMOVE HARAKAT
# =========================

def remove_harakat(text):
    pattern = r'[\u064B-\u065F\u0670\u06D6-\u06ED]'

    if isinstance(text, list):
        return [re.sub(pattern, '', t) for t in text]

    elif isinstance(text, str):
        return re.sub(pattern, '', text)

    return text

hasil1 = df0.copy()

hasil1['Sanad_no_harakat'] = hasil1['Sanad'].apply(remove_harakat)

# =========================
# NORMALISASI ALIF YA
# =========================

def normalisasi_alif_ya(lst):

    if isinstance(lst, list):

        hasil = []

        for word in lst:

            word = re.sub('[إأآا]', 'ا', word)
            word = re.sub('[يى]', 'ي', word)

            hasil.append(word)

        return hasil

    return lst

hasil1['Sanad_no_harakat'] = hasil1['Sanad_no_harakat'].apply(
    normalisasi_alif_ya
)

# =========================
# ENSURE LIST
# =========================

def ensure_list(cell):

    if isinstance(cell, list):
        return cell

    if isinstance(cell, str):

        try:
            return ast.literal_eval(cell)

        except:
            return [cell]

    return []

hasil1['Sanad_no_harakat'] = hasil1['Sanad_no_harakat'].apply(
    ensure_list
)

# =========================
# CLEAN SPACES
# =========================

hasil1['Sanad_no_harakat'] = hasil1['Sanad_no_harakat'].apply(
    lambda lst: [word.strip() for word in lst]
)

# =========================
# GANTI KATA KEKERABATAN
# =========================

def ganti_kata_kekerabatan(lst):

    mapping = {
        'ابيه': 'اب',
        'اباه': 'اب',
        'ابو': 'اب',
        'اخيه': 'اخ',
        'عمه': 'عم',
        'امه': 'ام'
    }

    result = []

    for word in lst:

        if word in mapping:
            result.append(mapping[word])

        else:
            result.append(word)

    return result

hasil1['Sanad_no_harakat'] = hasil1['Sanad_no_harakat'].apply(
    ganti_kata_kekerabatan
)

# =========================
# NORMALIZE NAMES
# =========================

def normalize_names(lst):

    normalized = []

    for word in lst:

        word = word.strip()
        word = re.sub(r'\s+', ' ', word)

        normalized.append(word)

    return normalized

hasil1['Sanad_no_harakat'] = hasil1['Sanad_no_harakat'].apply(
    normalize_names
)

# =========================
# REMOVE INVALID DATA
# =========================

hasil1 = hasil1[
    ~hasil1['Sanad_no_harakat'].apply(lambda lst: 'ابو' in lst)
]

# =========================
# SAVE CLEANED DATA
# =========================

hasil1.to_csv('sanadset_cleaned.csv',
    index=False,
    encoding='utf-8-sig'
)

print('sanadset_cleaned.csv berhasil disimpan')