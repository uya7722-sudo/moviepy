"""
Main Window for Aircraft Job Card Database
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List
from models import JobCard
from database import JobCardDatabase
from ui.jobcard_form import JobCardForm


class MainWindow:
    """Main application window"""
    
    def __init__(self, root: tk.Tk, database: JobCardDatabase):
        self.root = root
        self.db = database
        self.current_jobcards: List[JobCard] = []
        self.filtered_jobcards: List[JobCard] = []
        
        self.root.title("Aircraft Job Card Database")
        self.root.geometry("1400x700")
        
        self.create_widgets()
        self.refresh_data()
    
    def create_widgets(self):
        """Create main window widgets"""
        # Top frame for filters and controls
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N))
        
        # Title
        ttk.Label(top_frame, text="Aircraft Job Card Database", 
                 font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Filter controls
        ttk.Label(top_frame, text="Check Type:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.check_type_var = tk.StringVar()
        self.check_type_combo = ttk.Combobox(top_frame, textvariable=self.check_type_var, width=15)
        self.check_type_combo.grid(row=1, column=1, padx=5)
        self.check_type_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        ttk.Label(top_frame, text="Aircraft:").grid(row=1, column=2, sticky=tk.W, padx=5)
        self.aircraft_var = tk.StringVar()
        self.aircraft_combo = ttk.Combobox(top_frame, textvariable=self.aircraft_var, width=15)
        self.aircraft_combo.grid(row=1, column=3, padx=5)
        self.aircraft_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        ttk.Label(top_frame, text="Search:").grid(row=1, column=4, sticky=tk.W, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(top_frame, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=1, column=5, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.apply_filters())
        
        # Button frame
        button_frame = ttk.Frame(top_frame)
        button_frame.grid(row=2, column=0, columnspan=6, pady=10)
        
        ttk.Button(button_frame, text="Add Job Card", command=self.add_jobcard).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Job Card", command=self.edit_jobcard).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Job Card", command=self.delete_jobcard).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Filters", command=self.clear_filters).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to Excel", command=self.export_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Changes", command=self.save_changes).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(top_frame, textvariable=self.status_var, foreground='blue')
        self.status_label.grid(row=3, column=0, columnspan=6, pady=5)
        
        # Treeview frame
        tree_frame = ttk.Frame(self.root, padding="10")
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create treeview with scrollbars
        self.tree = ttk.Treeview(tree_frame, columns=(
            'check_type', 'item_no', 'card_number', 'task_ref', 'task_title', 
            'zone', 'ac_type', 'type_insp'
        ), show='headings', height=25)
        
        # Define columns
        self.tree.heading('check_type', text='Check Type')
        self.tree.heading('item_no', text='Item No')
        self.tree.heading('card_number', text='Card Number')
        self.tree.heading('task_ref', text='Task Reference')
        self.tree.heading('task_title', text='Task Title')
        self.tree.heading('zone', text='Zone')
        self.tree.heading('ac_type', text='A/C Type')
        self.tree.heading('type_insp', text='Type of Insp')
        
        # Set column widths
        self.tree.column('check_type', width=100)
        self.tree.column('item_no', width=70)
        self.tree.column('card_number', width=120)
        self.tree.column('task_ref', width=150)
        self.tree.column('task_title', width=300)
        self.tree.column('zone', width=100)
        self.tree.column('ac_type', width=100)
        self.tree.column('type_insp', width=120)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Bind double-click to edit
        self.tree.bind('<Double-1>', lambda e: self.edit_jobcard())
    
    def refresh_data(self):
        """Refresh data from database"""
        try:
            self.db.load_data()
            self.current_jobcards = self.db.get_all_jobcards()
            
            # Update filter dropdowns
            check_types = ['All'] + self.db.get_check_types()
            self.check_type_combo['values'] = check_types
            self.check_type_var.set('All')
            
            aircraft_regs = ['All'] + self.db.get_aircraft_regs()
            self.aircraft_combo['values'] = aircraft_regs
            self.aircraft_var.set('All')
            
            self.apply_filters()
            self.update_status(f"Loaded {len(self.current_jobcards)} job cards")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")
    
    def apply_filters(self):
        """Apply filters to job cards"""
        filtered = self.current_jobcards
        
        # Filter by check type
        check_type = self.check_type_var.get()
        if check_type and check_type != 'All':
            filtered = [jc for jc in filtered if jc.check_type == check_type]
        
        # Filter by aircraft
        aircraft = self.aircraft_var.get()
        if aircraft and aircraft != 'All':
            filtered = [jc for jc in filtered if jc.get_aircraft_status(aircraft) is not None]
        
        # Search filter
        search_query = self.search_var.get().lower()
        if search_query:
            filtered = [jc for jc in filtered if (
                search_query in jc.card_number.lower() or
                search_query in jc.task_reference.lower() or
                search_query in jc.task_title.lower() or
                search_query in jc.description.lower() or
                search_query in jc.zone.lower()
            )]
        
        self.filtered_jobcards = filtered
        self.update_treeview()
        self.update_status(f"Showing {len(filtered)} of {len(self.current_jobcards)} job cards")
    
    def update_treeview(self):
        """Update treeview with filtered job cards"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add filtered job cards
        for jc in self.filtered_jobcards:
            self.tree.insert('', tk.END, values=(
                jc.check_type,
                jc.item_no,
                jc.card_number,
                jc.task_reference,
                jc.task_title,
                jc.zone,
                jc.ac_type,
                jc.type_of_insp
            ))
    
    def clear_filters(self):
        """Clear all filters"""
        self.check_type_var.set('All')
        self.aircraft_var.set('All')
        self.search_var.set('')
        self.apply_filters()
    
    def add_jobcard(self):
        """Add new job card"""
        dialog = JobCardForm(
            self.root, 
            check_types=self.db.get_check_types(),
            aircraft_regs=self.db.get_aircraft_regs()
        )
        self.root.wait_window(dialog)
        
        if dialog.result:
            self.db.add_jobcard(dialog.result)
            self.current_jobcards = self.db.get_all_jobcards()
            self.apply_filters()
            self.update_status("Job card added successfully")
    
    def edit_jobcard(self):
        """Edit selected job card"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a job card to edit")
            return
        
        # Get selected index
        item = selection[0]
        index = self.tree.index(item)
        
        # Get the actual job card from filtered list
        if index >= len(self.filtered_jobcards):
            return
        
        jobcard = self.filtered_jobcards[index]
        
        # Find index in main list
        main_index = self.current_jobcards.index(jobcard)
        
        dialog = JobCardForm(
            self.root, 
            jobcard=jobcard,
            check_types=self.db.get_check_types(),
            aircraft_regs=self.db.get_aircraft_regs()
        )
        self.root.wait_window(dialog)
        
        if dialog.result:
            self.db.update_jobcard(main_index, dialog.result)
            self.current_jobcards = self.db.get_all_jobcards()
            self.apply_filters()
            self.update_status("Job card updated successfully")
    
    def delete_jobcard(self):
        """Delete selected job card"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a job card to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this job card?"):
            return
        
        # Get selected index
        item = selection[0]
        index = self.tree.index(item)
        
        # Get the actual job card from filtered list
        if index >= len(self.filtered_jobcards):
            return
        
        jobcard = self.filtered_jobcards[index]
        
        # Find index in main list
        main_index = self.current_jobcards.index(jobcard)
        
        self.db.delete_jobcard(main_index)
        self.current_jobcards = self.db.get_all_jobcards()
        self.apply_filters()
        self.update_status("Job card deleted successfully")
    
    def export_data(self):
        """Export filtered data to Excel"""
        if not self.filtered_jobcards:
            messagebox.showwarning("Warning", "No data to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.db.export_filtered_data(self.filtered_jobcards, file_path)
                messagebox.showinfo("Success", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting data: {e}")
    
    def save_changes(self):
        """Save changes to database"""
        try:
            self.db.save_data()
            messagebox.showinfo("Success", "Changes saved successfully")
            self.update_status("Changes saved to database")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving changes: {e}")
    
    def update_status(self, message: str):
        """Update status label"""
        self.status_var.set(message)
