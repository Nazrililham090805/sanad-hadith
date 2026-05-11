import pandas as pd
import subprocess
import sys
from pathlib import Path


def main():
    
    print("\n" + "=" * 60)
    print("DATA CLEANING & TRANSFORMATION PIPELINE")
    print("=" * 60)
    
    cleaned_path = "data/processed/sanadset_cleaned.csv"
    edges_path   = "data/processed/edges.csv"
    
    # =====================================
    # STEP 1: PREPROCESSING
    # =====================================
    
    print("\n[STEP 1] PREPROCESSING")
    print("-" * 60)
    
    result = subprocess.run(
        [sys.executable, "src/preprocessing.py"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ ERROR en preprocessing:")
        print(result.stderr)
        return
    
    print(result.stdout)
    
    # =====================================
    # STEP 2: DISPLAY CLEANED DATA
    # =====================================
    
    print("\n[STEP 2] CLEANED DATA PREVIEW")
    print("-" * 60)
    
    if Path(cleaned_path).exists():
        df_cleaned = pd.read_csv(cleaned_path)
        print(f"\n✅ Cleaned Data Summary:")
        print(f"   - Total filas: {len(df_cleaned)}")
        print(f"   - Total columnas: {len(df_cleaned.columns)}")
        print(f"   - Columnas: {df_cleaned.columns.tolist()}")
        
        print(f"\n📊 Data Types:")
        print(df_cleaned.dtypes)
        
        print(f"\n📋 Primeras 5 filas:")
        print(df_cleaned[['Hadith', 'Sanad']].head())
        
    else:
        print("❌ No se encontró el archivo de datos limpios")
        return
    
    # =====================================
    # STEP 3: TRANSFORMATION
    # =====================================
    
    print("\n[STEP 3] TRANSFORMATION")
    print("-" * 60)
    
    result = subprocess.run(
        [sys.executable, "src/transformation.py"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ ERROR en transformation:")
        print(result.stderr)
        return
    
    print(result.stdout)
    
    # =====================================
    # STEP 4: DISPLAY EDGES
    # =====================================
    
    print("\n[STEP 4] EDGES DATA PREVIEW")
    print("-" * 60)
    
    if Path(edges_path).exists():
        df_edges = pd.read_csv(edges_path)
        print(f"\n✅ Edges Summary:")
        print(f"   - Total edges: {len(df_edges)}")
        print(f"   - Columnas: {df_edges.columns.tolist()}")
        
        print(f"\n📊 Data Types:")
        print(df_edges.dtypes)
        
        print(f"\n📋 Primeras 10 edges:")
        print(df_edges.head(10))
        
        print(f"\n📈 Weight Statistics:")
        print(df_edges['weight'].describe())
        
    else:
        print("❌ No se encontró el archivo de edges")
        return
    
    # =====================================
    # DONE
    # =====================================
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE SELESAI EXITOSAMENTE")
    print("=" * 60)
    print(f"\n📁 Output Files:")
    print(f"   ✓ {cleaned_path}")
    print(f"   ✓ {edges_path}")
    print("\n")


if __name__ == "__main__":
    main()