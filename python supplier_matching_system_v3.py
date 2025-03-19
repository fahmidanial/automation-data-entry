import pandas as pd
import os

def match_suppliers(pembekal_data, aset_spa_data):
    """
    Match supplier names between two datasets and update the kod_pembekal field.
    Handles minor spacing differences and case mismatches.
    """
    updated_aset_spa = aset_spa_data.copy()
    
    # Normalize supplier names: remove spaces, convert to uppercase
    pembekal_data['Nama Pembekal Normalized'] = pembekal_data['Nama Pembekal'].str.upper().str.replace(" ", "")
    supplier_map = pembekal_data.groupby('Nama Pembekal Normalized')['ID Pembekal'].apply(lambda x: '/'.join(x)).to_dict()
    
    def get_supplier_id(supplier_name):
        if pd.isna(supplier_name) or supplier_name.strip() == '':
            return ''
        normalized_name = supplier_name.upper().replace(" ", "")
        return supplier_map.get(normalized_name, '')

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
            'ACTION POINT TECHNOLOGY'
        ],
        'kod_pembekal': ['', '', '', '', '']
    })

def main():
    supplier_file = "C:\\Users\\Swizard\\Desktop\\Automation\\Original Senarai Pembekal.txt"
    
    try:
        pembekal_data = read_supplier_list(supplier_file)
        print(f"Successfully loaded {len(pembekal_data)} suppliers from text file")
    except Exception as e:
        print(f"Error reading supplier file: {e}")
        pembekal_data = pd.DataFrame({
            'ID Pembekal': ['UP02164', 'UP01888', 'UP00003', 'UP00002'],
            'Nama Pembekal': ['2Y COMMUNICATIONS ENGINEERING', 'SKY WORLD CLASSIC', 'ABX EXPRESS (KUCHING) SDN BHD', 'ABU SEMAN MAT AIL']
        })
    
    excel_file = "C:\\Users\\Swizard\\Desktop\\Automation\\Original Senarai Aset SPA.xlsx"
    
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
    
    updated_aset_spa = match_suppliers(pembekal_data, aset_spa_data)
    
    output_file = "C:\\Users\\Swizard\\Desktop\\Automation\\Updated Senarai Aset SPA.xlsx"
    updated_aset_spa.to_excel(output_file, index=False)
    print(f"Results saved to {output_file}")
    
    return updated_aset_spa

if __name__ == "__main__":
    main()
