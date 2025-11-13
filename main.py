#!/usr/bin/env python3
"""
Aircraft Job Card Database Application
Main entry point
"""
import tkinter as tk
from tkinter import messagebox
import sys
import os
from database import JobCardDatabase
from ui.main_window import MainWindow


def main():
    """Main application entry point"""
    # Database file path
    db_path = '/vercel/sandbox/uploads/Aircraft_Jobcard_Database.xlsm'
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        sys.exit(1)
    
    try:
        # Initialize database
        print("Loading database...")
        database = JobCardDatabase(db_path)
        print(f"Database loaded: {len(database.jobcards)} job cards, {len(database.aircraft)} aircraft")
        
        # Create main window
        root = tk.Tk()
        app = MainWindow(root, database)
        
        # Run application
        root.mainloop()
    
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
