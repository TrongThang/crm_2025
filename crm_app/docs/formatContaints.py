from enum import Enum
class FORMAT_DATE:
    DATETIME = "%d/%m/%Y %H:%M"
    DATE_ONLY = "%d/%m/%Y"
    MYSQL_DATE_ONLY = "%Y-%m-%d"

class STATUS(Enum):
    IMPORT_INVOICE = {
        "FINISH": 1,
        "DELIVERY": 0
    },
    EXPORT_INVOICE = {
        "FINISH": 1,
        "DELIVERY": 0
    },
    PRODUCT = {
        "IN_THE_BUSINESS": 1,
        "STOP_BUSINESS": 0
    }

    WAREHOUSE = {
        "HAVE_DELIVERED": 1,
        "DELIVERY": 0
    }

def get_status_by_object(status_type: STATUS):
    if isinstance(status_type.value, dict):
        return status_type.value
    
    return None