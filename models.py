"""
Data models for Aircraft Job Card Database
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Aircraft:
    """Aircraft registration data"""
    ac_reg: str
    msn: str
    ac_type: str
    
    def __str__(self):
        return f"{self.ac_reg} ({self.ac_type})"


@dataclass
class JobCard:
    """Job Card data model"""
    check_type: str
    item_no: int
    card_number: str
    task_reference: str
    task_title: str
    description: str
    zone: str
    ac_type: str
    type_of_insp: str
    pk_ysv: Optional[str] = None
    pk_ysg: Optional[str] = None
    pk_ysz: Optional[str] = None
    pk_ysh: Optional[str] = None
    pk_ysn: Optional[str] = None
    pk_yrd: Optional[str] = None
    pk_yst: Optional[str] = None
    
    def get_aircraft_status(self, ac_reg: str) -> Optional[str]:
        """Get status for specific aircraft"""
        ac_map = {
            'PK-YSV': self.pk_ysv,
            'PK-YSG': self.pk_ysg,
            'PK-YSZ': self.pk_ysz,
            'PK-YSH': self.pk_ysh,
            'PK-YSN': self.pk_ysn,
            'PK-YRD': self.pk_yrd,
            'PK-YST': self.pk_yst,
        }
        return ac_map.get(ac_reg)
    
    def set_aircraft_status(self, ac_reg: str, status: str):
        """Set status for specific aircraft"""
        if ac_reg == 'PK-YSV':
            self.pk_ysv = status
        elif ac_reg == 'PK-YSG':
            self.pk_ysg = status
        elif ac_reg == 'PK-YSZ':
            self.pk_ysz = status
        elif ac_reg == 'PK-YSH':
            self.pk_ysh = status
        elif ac_reg == 'PK-YSN':
            self.pk_ysn = status
        elif ac_reg == 'PK-YRD':
            self.pk_yrd = status
        elif ac_reg == 'PK-YST':
            self.pk_yst = status
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'CHECK TYPE': self.check_type,
            'ITEM NO': self.item_no,
            'CARD NUMBER1': self.card_number,
            'TASK REFERENCE': self.task_reference,
            'TASK TITLE': self.task_title,
            'DESCRIPTION': self.description,
            'ZONE': self.zone,
            'A/C TYPE': self.ac_type,
            'TYPE OF INSP': self.type_of_insp,
            'PK-YSV': self.pk_ysv,
            'PK-YSG': self.pk_ysg,
            'PK-YSZ': self.pk_ysz,
            'PK-YSH': self.pk_ysh,
            'PK-YSN': self.pk_ysn,
            'PK-YRD': self.pk_yrd,
            'PK-YST': self.pk_yst,
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create JobCard from dictionary"""
        return cls(
            check_type=str(data.get('CHECK TYPE', '')),
            item_no=int(data.get('ITEM NO', 0)),
            card_number=str(data.get('CARD NUMBER1', '')),
            task_reference=str(data.get('TASK REFERENCE', '')),
            task_title=str(data.get('TASK TITLE', '')),
            description=str(data.get('DESCRIPTION', '')),
            zone=str(data.get('ZONE', '')),
            ac_type=str(data.get('A/C TYPE', '')),
            type_of_insp=str(data.get('TYPE OF INSP', '')),
            pk_ysv=data.get('PK-YSV'),
            pk_ysg=data.get('PK-YSG'),
            pk_ysz=data.get('PK-YSZ'),
            pk_ysh=data.get('PK-YSH'),
            pk_ysn=data.get('PK-YSN'),
            pk_yrd=data.get('PK-YRD'),
            pk_yst=data.get('PK-YST'),
        )
