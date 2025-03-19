import pandas as pd
import os
import re
from thefuzz import fuzz, process

def clean_name(name):
    """
    Preprocess supplier names by normalizing spaces, removing punctuation, and converting to lowercase.
    """
    if pd.isna(name) or name.strip() == '':
        return ''
    # Convert to lowercase, remove punctuation, normalize spaces
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)  # Remove punctuation
    name = re.sub(r'\s+', ' ', name).strip()  # Normalize spaces
    return name

def match_suppliers(pembekal_data, aset_spa_data, similarity_threshold=90):
    """
    Match supplier names between two datasets and update the kod_pembekal field.
    Uses exact matching first, then fuzzy matching for remaining unmatched entries.
    """
    updated_aset_spa = aset_spa_data.copy()
    
    # Normalize supplier names for exact matching: remove spaces, convert to uppercase
    pembekal_data['Nama Pembekal Normalized'] = pembekal_data['Nama Pembekal'].str.upper().str.replace(" ", "")
    supplier_map = pembekal_data.groupby('Nama Pembekal Normalized')['ID Pembekal'].apply(lambda x: '/'.join(x)).to_dict()
    
    # Create a cleaned list for fuzzy matching
    pembekal_data['Nama Pembekal Cleaned'] = pembekal_data['Nama Pembekal'].apply(clean_name)
    supplier_names_cleaned = pembekal_data['Nama Pembekal Cleaned'].tolist()
    supplier_ids = pembekal_data['ID Pembekal'].tolist()
    
    def get_supplier_id(supplier_name):
        if pd.isna(supplier_name) or supplier_name.strip() == '':
            return ''
        
        # Step 1: Exact match using normalized name (no spaces, uppercase)
        normalized_name = supplier_name.upper().replace(" ", "")
        exact_match = supplier_map.get(normalized_name, '')
        if exact_match:
            return exact_match
        
        # Step 2: Fuzzy match if exact match fails
        cleaned_name = clean_name(supplier_name)
        if cleaned_name:
            best_match, score, index = process.extractOne(cleaned_name, supplier_names_cleaned, scorer=fuzz.token_set_ratio)
            if score >= similarity_threshold:
                return supplier_ids[index]
        
        return ''  # Return empty string if no match found

    updated_aset_spa['kod_pembekal'] = updated_aset_spa['pembekal'].apply(get_supplier_id)
    return updated_aset_spa

def read_supplier_list(file_path):
    """
    Read supplier list from text file and return as DataFrame
    """
    suppliers = []
    with open(file_path, 'r', encoding='utf-8') as file:
        next(file)  # Skip header
        for line in file:
            parts = line.strip().split('\t', 1)
            if len(parts) == 2:
                supplier_id, supplier_name = parts
                suppliers.append([supplier_id, supplier_name])
    
    return pd.DataFrame(suppliers, columns=['ID Pembekal', 'Nama Pembekal'])

def create_sample_aset_spa_data():
    """Create a sample dataset for testing when the Excel file is not available"""
    return pd.DataFrame({
        'pembekal': [
            '2Y COMMUNICATIONS ENGINEERING', 
            'SKYWORLD CLASSIC', 
            'ABX EXPRESS (KUCHING) SDN BHD',
            'ACER SALES & SERVICES SDN BHD',
            'ACTION POINT TECHNOLOGY',
            'CG COMPUTER SDN BHD',
            'DELCOL WATER SOLUTIONS (M) SDN BHD',
            'DG SOLUTION ENTERPRISE',
            'DISPLAY ASIA SDN BHD',
            'DNA COMPUTER SDN BHD'
        ],
        'kod_pembekal': ['', '', '', '', '', '', '', '', '', '']
    })

def main():
    supplier_file = "C:\\Users\\USER\\Desktop\\SW\\Automation\\automation-data-entry\\Original Senarai Pembekal.txt"
    
    try:
        pembekal_data = read_supplier_list(supplier_file)
        print(f"Successfully loaded {len(pembekal_data)} suppliers from text file")
    except Exception as e:
        print(f"Error reading supplier file: {e}")
        pembekal_data = pd.DataFrame({
            'ID Pembekal': ['UP02164', 'UP01888', 'UP00003', 'UP00002', 'UP00005', 'UP00006', 'UP00007', 'UP00008', 'UP00009', 'UP00010'],
            'Nama Pembekal': [
                '2Y COMMUNICATIONS ENGINEERING', 
                'SKY WORLD CLASSIC', 
                'ABX EXPRESS (KUCHING) SDN BHD', 
                'ABU SEMAN MAT AIL',
                'CG COMPUTERS SDN. BHD.',
                'DELCOL WATER SOLUTION SDN BHD',
                'DG SOLUTION',
                'DISPLAY ASIA SDN. BHD.',
                'DNA COMPUTER SERVICE CENTRE',
                'F H SALES AND SERVICE'
            ]
        })
    
    excel_file = "C:\\Users\\USER\\Desktop\\SW\\Automation\\automation-data-entry\\Original Senarai Aset SPA.xlsx"
    
    try:
        print(f"Attempting to read Excel file from: {excel_file}")
        aset_spa_data = pd.read_excel(excel_file)
        print(f"Successfully loaded Excel file with {len(aset_spa_data)} rows.")
        
        if 'pembekal' not in aset_spa_data.columns:
            if 'Pembekal' in aset_spa_data.columns:
                aset_spa_data = aset_spa_data.rename(columns={'Pembekal': 'pembekal'})
            else:
                aset_spa_data = create_sample_aset_spa_data()
        
        if 'kod_pembekal' not in aset_spa_data.columns:
            aset_spa_data['kod_pembekal'] = ''
            
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        aset_spa_data = create_sample_aset_spa_data()
    
    updated_aset_spa = match_suppliers(pembekal_data, aset_spa_data, similarity_threshold=90)
    
    output_file = "C:\\Users\\USER\\Desktop\\SW\\Automation\\automation-data-entry\\Updated Senarai Aset SPA.xlsx"
    updated_aset_spa.to_excel(output_file, index=False)
    print(f"Results saved to {output_file}")
    
    # Print results for verification
    print("\nUpdated Aset SPA Data:")
    print(updated_aset_spa[['pembekal', 'kod_pembekal']])

if __name__ == "__main__":
    main()