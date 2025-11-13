"""
Database handler for Excel operations
"""
import pandas as pd
import openpyxl
from typing import List, Optional
from models import JobCard, Aircraft


class JobCardDatabase:
    """Handler for Job Card Excel database"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.jobcards: List[JobCard] = []
        self.aircraft: List[Aircraft] = []
        self.load_data()
    
    def load_data(self):
        """Load data from Excel file"""
        try:
            # Load job cards from Sheet1
            df_jobcards = pd.read_excel(self.file_path, sheet_name='Sheet1', engine='openpyxl')
            self.jobcards = []
            
            for _, row in df_jobcards.iterrows():
                try:
                    jobcard = JobCard.from_dict(row.to_dict())
                    self.jobcards.append(jobcard)
                except Exception as e:
                    print(f"Error loading job card: {e}")
                    continue
            
            # Load aircraft from Sheet2
            df_aircraft = pd.read_excel(self.file_path, sheet_name='Sheet2 ', engine='openpyxl')
            self.aircraft = []
            
            for _, row in df_aircraft.iterrows():
                try:
                    aircraft = Aircraft(
                        ac_reg=str(row['A/C REG']),
                        msn=str(row['MSN']),
                        ac_type=str(row['A/C TYPE'])
                    )
                    self.aircraft.append(aircraft)
                except Exception as e:
                    print(f"Error loading aircraft: {e}")
                    continue
            
            print(f"Loaded {len(self.jobcards)} job cards and {len(self.aircraft)} aircraft")
        
        except Exception as e:
            print(f"Error loading database: {e}")
            raise
    
    def save_data(self):
        """Save data back to Excel file"""
        try:
            # Convert job cards to DataFrame
            jobcard_dicts = [jc.to_dict() for jc in self.jobcards]
            df_jobcards = pd.DataFrame(jobcard_dicts)
            
            # Convert aircraft to DataFrame
            aircraft_dicts = [
                {'A/C REG': ac.ac_reg, 'MSN': ac.msn, 'A/C TYPE': ac.ac_type}
                for ac in self.aircraft
            ]
            df_aircraft = pd.DataFrame(aircraft_dicts)
            
            # Load existing workbook to preserve other sheets
            wb = openpyxl.load_workbook(self.file_path)
            
            # Write to Excel using openpyxl
            with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df_jobcards.to_excel(writer, sheet_name='Sheet1', index=False)
                df_aircraft.to_excel(writer, sheet_name='Sheet2 ', index=False)
            
            print(f"Saved {len(self.jobcards)} job cards and {len(self.aircraft)} aircraft")
        
        except Exception as e:
            print(f"Error saving database: {e}")
            raise
    
    def get_all_jobcards(self) -> List[JobCard]:
        """Get all job cards"""
        return self.jobcards
    
    def get_jobcards_by_check_type(self, check_type: str) -> List[JobCard]:
        """Filter job cards by check type"""
        return [jc for jc in self.jobcards if jc.check_type == check_type]
    
    def get_jobcards_by_aircraft(self, ac_reg: str) -> List[JobCard]:
        """Get job cards for specific aircraft"""
        return [jc for jc in self.jobcards if jc.get_aircraft_status(ac_reg) is not None]
    
    def search_jobcards(self, query: str) -> List[JobCard]:
        """Search job cards by keyword"""
        query = query.lower()
        results = []
        
        for jc in self.jobcards:
            if (query in jc.card_number.lower() or
                query in jc.task_reference.lower() or
                query in jc.task_title.lower() or
                query in jc.description.lower() or
                query in jc.zone.lower()):
                results.append(jc)
        
        return results
    
    def add_jobcard(self, jobcard: JobCard):
        """Add new job card"""
        self.jobcards.append(jobcard)
    
    def update_jobcard(self, index: int, jobcard: JobCard):
        """Update existing job card"""
        if 0 <= index < len(self.jobcards):
            self.jobcards[index] = jobcard
    
    def delete_jobcard(self, index: int):
        """Delete job card"""
        if 0 <= index < len(self.jobcards):
            del self.jobcards[index]
    
    def get_all_aircraft(self) -> List[Aircraft]:
        """Get all aircraft"""
        return self.aircraft
    
    def get_check_types(self) -> List[str]:
        """Get unique check types"""
        check_types = set(jc.check_type for jc in self.jobcards)
        return sorted(list(check_types))
    
    def get_aircraft_regs(self) -> List[str]:
        """Get all aircraft registrations"""
        return [ac.ac_reg for ac in self.aircraft]
    
    def export_filtered_data(self, jobcards: List[JobCard], output_path: str):
        """Export filtered job cards to Excel"""
        try:
            jobcard_dicts = [jc.to_dict() for jc in jobcards]
            df = pd.DataFrame(jobcard_dicts)
            df.to_excel(output_path, index=False, engine='openpyxl')
            print(f"Exported {len(jobcards)} job cards to {output_path}")
        except Exception as e:
            print(f"Error exporting data: {e}")
            raise
