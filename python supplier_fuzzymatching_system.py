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
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)  # Remove punctuation
    name = re.sub(r'\s+', ' ', name).strip()  # Normalize spaces
    return name

def match_suppliers(pembekal_data, aset_spa_data, similarity_threshold=95):
    """
    Match supplier names between two datasets and update the kod_pembekal field.
    Uses exact matching first, then fuzzy matching for remaining unmatched entries.
    """
    updated_aset_spa = aset_spa_data.copy()
    
    # Normalize supplier names for exact matching: remove spaces, convert to uppercase
    pembekal_data['Nama Pembekal Normalized'] = pembekal_data['Nama Pembekal'].str.upper().str.replace(" ", "")
    supplier_map = pembekal_data.groupby('Nama Pembekal Normalized')['ID Pembekal'].apply(lambda x: '/'.join(x)).to_dict()
    
    # Create a cleaned list for fuzzy matching, filtering out empty strings
    pembekal_data['Nama Pembekal Cleaned'] = pembekal_data['Nama Pembekal'].apply(clean_name)
    supplier_names_cleaned = [name for name in pembekal_data['Nama Pembekal Cleaned'].tolist() if name]
    supplier_ids = pembekal_data['ID Pembekal'].tolist()
    
    def get_supplier_id(supplier_name):
        if pd.isna(supplier_name) or supplier_name.strip() == '':
            return ''
        
        # Step 1: Exact match using normalized name (no spaces, uppercase)
        normalized_name = supplier_name.upper().replace(" ", "")
        exact_match = supplier_map.get(normalized_name, '')
        if exact_match:
            return exact_match  # Return exact match immediately, skip fuzzy
        
        # Step 2: Fuzzy match only if no exact match
        cleaned_name = clean_name(supplier_name)
        if cleaned_name and supplier_names_cleaned:
            result = process.extractOne(cleaned_name, supplier_names_cleaned, scorer=fuzz.token_sort_ratio)
            if result:
                if len(result) == 3:  # (match, score, index)
                    best_match, score, index = result
                elif len(result) == 2:  # (match, score)
                    best_match, score = result
                    index = supplier_names_cleaned.index(best_match)
                else:
                    return ''
                
                if score >= similarity_threshold:
                    return supplier_ids[index]
        
        return ''  # No match found

    updated_aset_spa['kod_pembekal'] = updated_aset_spa['pembekal'].apply(get_supplier_id)
    return updated_aset_spa

def read_supplier_list(file_path):
    """
    Read supplier list from an Excel file and return as DataFrame.
    
    Args:
        file_path (str): Path to the supplier list Excel file.
    
    Returns:
        pd.DataFrame: DataFrame with columns 'ID Pembekal' and 'Nama Pembekal'.
    """
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        print(f"Excel file loaded successfully with {len(df)} rows.")
        
        # Print column names for debugging
        print("Columns found in supplier file:", df.columns.tolist())
        
        # Define expected column names (adjust these based on your file)
        expected_id_col = 'ID Pembekal'  # Change this to match your actual ID column name (lowercase)
        expected_name_col = 'Nama Pembekal'  # Change this to match your actual name column name (lowercase)
        
        # Check for expected columns (case-insensitive)
        columns = [col.lower() for col in df.columns]
        if expected_id_col not in columns or expected_name_col not in columns:
            # Try to find similar column names
            actual_id_col = next((col for col in df.columns if 'id' in col.lower() and 'pembekal' in col.lower()), None)
            actual_name_col = next((col for col in df.columns if 'nama' in col.lower() and 'pembekal' in col.lower()), None)
            
            if not actual_id_col or not actual_name_col:
                # If still not found, try broader matches or log all columns
                actual_id_col = next((col for col in df.columns if 'id' in col.lower() or 'code' in col.lower()), None)
                actual_name_col = next((col for col in df.columns if 'nama' in col.lower() or 'name' in col.lower()), None)
                
                if not actual_id_col or not actual_name_col:
                    raise ValueError(f"Could not find columns resembling 'ID Pembekal' and 'Nama Pembekal'. Available columns: {df.columns.tolist()}")
            
            # Rename columns to standard names
            df = df.rename(columns={actual_id_col: 'ID Pembekal', actual_name_col: 'Nama Pembekal'})
        else:
            # Standardize column names if they exist with different casing
            df.columns = [col if col.lower() != expected_id_col else 'ID Pembekal' for col in df.columns]
            df.columns = [col if col.lower() != expected_name_col else 'Nama Pembekal' for col in df.columns]
        
        # Filter to only the required columns and drop rows with missing values in either column
        df = df[['ID Pembekal', 'Nama Pembekal']].dropna()
        
        print(f"Valid suppliers after cleaning: {len(df)}")
        return df
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return pd.DataFrame(columns=['ID Pembekal', 'Nama Pembekal'])
    
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return pd.DataFrame(columns=['ID Pembekal', 'Nama Pembekal'])

def main():
    supplier_file = "C:\\Users\\USER\\Desktop\\SW\\Automation\\automation-data-entry\\Original Senarai Pembekal.xlsx"
    
    try:
        pembekal_data = read_supplier_list(supplier_file)
        if pembekal_data.empty:
            raise ValueError("No supplier data loaded.")
        print(f"Successfully loaded {len(pembekal_data)} suppliers from Excel file")
    except Exception as e:
        print(f"Error reading supplier file: {e}")
        # Fallback to sample data if file not found or invalid
        pembekal_data = pd.DataFrame({
            'ID Pembekal': ['UP00879', 'UP02164', 'UP02332', 'UP00187', 'UP00006', 'UP00004', 'UP00001', 'UP00009', 'UP00010', 'UP00018'],
            'Nama Pembekal': [
                '1MEDIA IPTV SDN BHD', 
                '2Y COMMUNICATIONS ENGINEERING', 
                'A M STAR RESOURCES', 
                'A&T TRADE & SERVICES', 
                'ABDUL GHAFUR BIN MAIDIN', 
                'ABLE SUCCESS SDN BHD', 
                'ABLENET SYSTEMS SDN BHD', 
                'ACBS ENGINEERING SDN. BHD.', 
                'ACER SALES & SERVICES SDN BHD', 
                'ACS SOLUTION SDN BHD'
            ]
        })
        print("Using fallback sample data.")
    
    excel_file = "C:\\Users\\USER\\Desktop\\SW\\Automation\\automation-data-entry\\Original Senarai Aset SPA.xlsx"
    
    try:
        print(f"Attempting to read Excel file from: {excel_file}")
        aset_spa_data = pd.read_excel(excel_file)
        print(f"Successfully loaded Excel file with {len(aset_spa_data)} rows.")
        
        if 'pembekal' not in aset_spa_data.columns:
            if 'Pembekal' in aset_spa_data.columns:
                aset_spa_data = aset_spa_data.rename(columns={'Pembekal': 'pembekal'})
            else:
                raise ValueError("No 'pembekal' or 'Pembekal' column found in Excel file")
        
        if 'kod_pembekal' not in aset_spa_data.columns:
            aset_spa_data['kod_pembekal'] = ''
            
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        # Fallback to sample data for testing
        aset_spa_data = pd.DataFrame({
            'pembekal': ['1MEDIA IPTV SDN BHD', 'A&T TRADE & SERVICES', 'Unknown Supplier', 'ACER SALES & SERVICES SDN BHD'],
            'kod_pembekal': ['', '', '', '']
        })
        print("Using fallback sample data for aset_spa_data.")
    
    updated_aset_spa = match_suppliers(pembekal_data, aset_spa_data, similarity_threshold=95)
    
    output_file = "C:\\Users\\USER\\Desktop\\SW\\Automation\\automation-data-entry\\Updated Senarai Aset SPA.xlsx"
    updated_aset_spa.to_excel(output_file, index=False)
    print(f"Results saved to {output_file}")
    
    # Print results for verification
    print("\nUpdated Aset SPA Data (first 20 rows):")
    print(updated_aset_spa[['pembekal', 'kod_pembekal']].head(20))

if __name__ == "__main__":
    main()