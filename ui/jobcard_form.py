"""
Job Card Form Dialog
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models import JobCard
from typing import Optional, List


class JobCardForm(tk.Toplevel):
    """Dialog for adding/editing job cards"""
    
    def __init__(self, parent, jobcard: Optional[JobCard] = None, 
                 check_types: List[str] = None, aircraft_regs: List[str] = None):
        super().__init__(parent)
        
        self.jobcard = jobcard
        self.result = None
        self.check_types = check_types or ['1A CHECK', '2A CHECK', '4A CHECK', '8A CHECK']
        self.aircraft_regs = aircraft_regs or []
        
        self.title("Edit Job Card" if jobcard else "Add Job Card")
        self.geometry("700x600")
        self.resizable(False, False)
        
        self.create_widgets()
        
        if jobcard:
            self.populate_data()
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
    
    def create_widgets(self):
        """Create form widgets"""
        # Main frame with scrollbar
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Basic Information
        ttk.Label(main_frame, text="Basic Information", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Check Type
        ttk.Label(main_frame, text="Check Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.check_type_var = tk.StringVar()
        self.check_type_combo = ttk.Combobox(main_frame, textvariable=self.check_type_var, 
                                             values=self.check_types, width=30)
        self.check_type_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Item No
        ttk.Label(main_frame, text="Item No:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.item_no_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.item_no_var, width=32).grid(
            row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Card Number
        ttk.Label(main_frame, text="Card Number:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.card_number_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.card_number_var, width=32).grid(
            row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Task Reference
        ttk.Label(main_frame, text="Task Reference:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.task_ref_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.task_ref_var, width=32).grid(
            row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Task Title
        ttk.Label(main_frame, text="Task Title:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.task_title_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.task_title_var, width=32).grid(
            row=5, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Description
        ttk.Label(main_frame, text="Description:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.description_text = tk.Text(main_frame, width=32, height=3)
        self.description_text.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Zone
        ttk.Label(main_frame, text="Zone:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.zone_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.zone_var, width=32).grid(
            row=7, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # A/C Type
        ttk.Label(main_frame, text="A/C Type:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.ac_type_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.ac_type_var, width=32).grid(
            row=8, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Type of Inspection
        ttk.Label(main_frame, text="Type of Insp:").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.type_insp_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.type_insp_var, width=32).grid(
            row=9, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Aircraft Status Section
        ttk.Label(main_frame, text="Aircraft Status", font=('Arial', 10, 'bold')).grid(
            row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        
        # Create status entries for each aircraft
        self.aircraft_status_vars = {}
        row = 11
        for ac_reg in self.aircraft_regs:
            ttk.Label(main_frame, text=f"{ac_reg}:").grid(row=row, column=0, sticky=tk.W, pady=5)
            var = tk.StringVar()
            ttk.Entry(main_frame, textvariable=var, width=32).grid(
                row=row, column=1, sticky=(tk.W, tk.E), pady=5)
            self.aircraft_status_vars[ac_reg] = var
            row += 1
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
    
    def populate_data(self):
        """Populate form with existing job card data"""
        if not self.jobcard:
            return
        
        self.check_type_var.set(self.jobcard.check_type)
        self.item_no_var.set(str(self.jobcard.item_no))
        self.card_number_var.set(self.jobcard.card_number)
        self.task_ref_var.set(self.jobcard.task_reference)
        self.task_title_var.set(self.jobcard.task_title)
        self.description_text.insert('1.0', self.jobcard.description)
        self.zone_var.set(self.jobcard.zone)
        self.ac_type_var.set(self.jobcard.ac_type)
        self.type_insp_var.set(self.jobcard.type_of_insp)
        
        # Populate aircraft status
        for ac_reg, var in self.aircraft_status_vars.items():
            status = self.jobcard.get_aircraft_status(ac_reg)
            if status:
                var.set(status)
    
    def save(self):
        """Save job card"""
        try:
            # Validate required fields
            if not self.check_type_var.get():
                messagebox.showerror("Error", "Check Type is required")
                return
            
            if not self.item_no_var.get():
                messagebox.showerror("Error", "Item No is required")
                return
            
            # Create job card
            jobcard = JobCard(
                check_type=self.check_type_var.get(),
                item_no=int(self.item_no_var.get()),
                card_number=self.card_number_var.get(),
                task_reference=self.task_ref_var.get(),
                task_title=self.task_title_var.get(),
                description=self.description_text.get('1.0', tk.END).strip(),
                zone=self.zone_var.get(),
                ac_type=self.ac_type_var.get(),
                type_of_insp=self.type_insp_var.get()
            )
            
            # Set aircraft status
            for ac_reg, var in self.aircraft_status_vars.items():
                status = var.get().strip()
                if status:
                    jobcard.set_aircraft_status(ac_reg, status)
            
            self.result = jobcard
            self.destroy()
        
        except ValueError:
            messagebox.showerror("Error", "Item No must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving job card: {e}")
    
    def cancel(self):
        """Cancel and close dialog"""
        self.result = None
        self.destroy()
