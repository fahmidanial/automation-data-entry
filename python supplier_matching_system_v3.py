import pandas as pd
import os

def match_suppliers(pembekal_data, aset_spa_data):
    """
    Match supplier names between two datasets and update the kod_pembekal field
    
    Parameters:
    pembekal_data (DataFrame): Contains supplier list with ID and name
    aset_spa_data (DataFrame): Contains asset list with empty supplier IDs
    
    Returns:
    DataFrame: Updated aset_spa_data with supplier IDs filled in
    """
    updated_aset_spa = aset_spa_data.copy()
    supplier_map = dict(zip(pembekal_data['Nama Pembekal'], pembekal_data['ID Pembekal']))
    
    def get_supplier_id(supplier_name):
        if pd.isna(supplier_name) or supplier_name == '':
            return ''
        return supplier_map.get(supplier_name, '')
    
    updated_aset_spa['kod_pembekal'] = updated_aset_spa['pembekal'].apply(get_supplier_id)
    return updated_aset_spa

def read_supplier_list(file_path):
    """
    Read supplier list from text file and return as DataFrame
    """
    suppliers = []
    with open(file_path, 'r', encoding='utf-8') as file:
        # Skip the header line
        next(file)
        for line in file:
            # Split on first tab only to handle supplier names with spaces
            parts = line.strip().split('\t', 1)
            if len(parts) == 2:
                supplier_id, supplier_name = parts
                suppliers.append([supplier_id, supplier_name])
    
    return pd.DataFrame(suppliers, columns=['ID Pembekal', 'Nama Pembekal'])

def main():
    # Specify the path to your supplier list text file
    supplier_file = "C:\\Users\\Swizard\\Desktop\\Automation\\Original Senarai Pembekal.txt"  # Replace with actual path
    
    try:
        # Read the supplier list from text file
        pembekal_data = read_supplier_list(supplier_file)
        print(f"Successfully loaded {len(pembekal_data)} suppliers from text file")
    except Exception as e:
        print(f"Error reading supplier file: {e}")
        print("Using sample data instead")
        pembekal_data = pd.DataFrame({
            'ID Pembekal': ['UP00001', 'UP00002', 'UP00003'],
            'Nama Pembekal': ['ABLENET SYSTEMS SDN BHD', 'ABU SEMAN MAT AIL', 'ABX EXPRESS (KUCHING) SDN BHD']
        })
    
    excel_file = r"C:\\Users\\Swizard\\Desktop\\Automation\\Original Senarai Aset SPA.xlsx"
    
    try:
        print(f"Attempting to read Excel file from: {excel_file}")
        aset_spa_data = pd.read_excel(excel_file)
        print(f"Successfully loaded Excel file with {len(aset_spa_data)} rows.")
        print(f"Columns in the Excel file: {list(aset_spa_data.columns)}")
        
        if 'pembekal' not in aset_spa_data.columns:
            print(f"Warning: 'pembekal' column not found in the Excel file.")
            print(f"Available columns are: {list(aset_spa_data.columns)}")
            
            if 'Pembekal' in aset_spa_data.columns:
                print("Using 'Pembekal' column instead of 'pembekal'")
                aset_spa_data = aset_spa_data.rename(columns={'Pembekal': 'pembekal'})
            else:
                print("Using sample data instead.")
                aset_spa_data = create_sample_aset_spa_data()
        
        if 'kod_pembekal' not in aset_spa_data.columns:
            aset_spa_data['kod_pembekal'] = ''
            
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        print("Using sample data instead.")
        aset_spa_data = create_sample_aset_spa_data()
    
    print("\nOriginal Senarai Pembekal (first 5 rows):")
    print(pembekal_data.head())
    print("\nOriginal Senarai Aset SPA (first 5 rows):")
    print(aset_spa_data.head())
    
    updated_aset_spa = match_suppliers(pembekal_data, aset_spa_data)
    
    print("\nUpdated Senarai Aset SPA with Supplier IDs (first 5 rows):")
    print(updated_aset_spa.head())
    
    output_file = r"C:\\Users\\Swizard\\Desktop\\Automation\\Updated Senarai Aset SPA.xlsx"
    updated_aset_spa.to_excel(output_file, index=False)
    print(f"\nResults saved to {output_file}")
    
    return updated_aset_spa

def create_sample_aset_spa_data():
    """Create a sample dataset for testing when the Excel file is not available"""
    return pd.DataFrame({
        'pembekal': [
            'ABLENET SYSTEMS SDN BHD', 
            'MALAYSIA AIRLINES BERHAD', 
            'ABX EXPRESS (KUCHING) SDN BHD',
            'ACER SALES & SERVICES SDN BHD',
            'ACTION POINT TECHNOLOGY'
        ],
        'kod_pembekal': ['', '', '', '', '']
    })

if __name__ == "__main__":
    main()