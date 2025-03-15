import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

# [Include your existing functions here: match_suppliers, read_supplier_list, create_sample_aset_spa_data]
def match_suppliers(pembekal_data, aset_spa_data):
    """
    Match supplier names between two datasets and update the kod_pembekal field.
    If a supplier has multiple IDs, concatenate them with '/'.
    """
    updated_aset_spa = aset_spa_data.copy()
    
    # Create a mapping where supplier names map to concatenated IDs
    supplier_map = pembekal_data.groupby('Nama Pembekal')['ID Pembekal'].apply(lambda x: '/'.join(x)).to_dict()
    
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
            'ABLENET SYSTEMS SDN BHD', 
            'MALAYSIA AIRLINES BERHAD', 
            'ABX EXPRESS (KUCHING) SDN BHD',
            'ACER SALES & SERVICES SDN BHD',
            'ACTION POINT TECHNOLOGY'
        ],
        'kod_pembekal': ['', '', '', '', '']
    })

class SupplierMatcherGUI:
    def __init__(self, master):
        self.master = master
        master.title("Supplier Matching Tool")

        # File path variables
        self.supplier_list_path = tk.StringVar()
        self.asset_spa_path = tk.StringVar()
        self.output_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Supplier List Selection
        ttk.Label(self.master, text="Supplier List (TXT):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.master, textvariable=self.supplier_list_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.master, text="Browse", command=self.browse_supplier_list).grid(row=0, column=2, padx=5, pady=5)

        # Asset SPA Selection
        ttk.Label(self.master, text="Asset SPA File (XLSX):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.master, textvariable=self.asset_spa_path, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.master, text="Browse", command=self.browse_asset_spa).grid(row=1, column=2, padx=5, pady=5)

        # Output File Selection
        ttk.Label(self.master, text="Output File:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.master, textvariable=self.output_path, width=50).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.master, text="Browse", command=self.browse_output).grid(row=2, column=2, padx=5, pady=5)

        # Process Button
        ttk.Button(self.master, text="Process Matching", command=self.process_matching).grid(row=3, column=0, columnspan=3, pady=10)

        # Status Label
        self.status_label = ttk.Label(self.master, text="")
        self.status_label.grid(row=4, column=0, columnspan=3, pady=5)

    def browse_supplier_list(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.supplier_list_path.set(file_path)

    def browse_asset_spa(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.asset_spa_path.set(file_path)

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.output_path.set(file_path)

    def process_matching(self):
        try:
            # Validate input files
            if not self.supplier_list_path.get():
                raise ValueError("Please select a supplier list file")
            if not self.asset_spa_path.get():
                raise ValueError("Please select an asset SPA file")
            if not self.output_path.get():
                raise ValueError("Please select an output file")

            # Read data
            pembekal_data = read_supplier_list(self.supplier_list_path.get())
            aset_spa_data = pd.read_excel(self.asset_spa_path.get())

            # Process data
            updated_data = match_suppliers(pembekal_data, aset_spa_data)

            # Save output
            updated_data.to_excel(self.output_path.get(), index=False)
            self.status_label.config(text=f"Successfully saved to {self.output_path.get()}")
            messagebox.showinfo("Success", "Matching completed successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SupplierMatcherGUI(root)
    root.mainloop()