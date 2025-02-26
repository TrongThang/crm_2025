from crm_app.models.Quyen import Quyen
from crm_app import db
from crm_app.services.helpers import get_word_before_dash
from sqlalchemy import text

def config_data_quyen_chuc_vu(lst_quyen):
    lst_result = {}
    for row in lst_quyen:
        type = row.type
        code = row.code

        quyen = lst_result.setdefault(type, {
            'show_in_menu': row.show_in_menu,
            'type': type,
            'allow_all': 0,
            'view': 0,
            'create': 0,
            'update': 0,
            'delete': 0,
        })

        if code == type:
            quyen['allow_all'] = 1
        elif code.startswith("view"):
            quyen['view'] = 1
        elif code.startswith("create"):
            quyen['create'] = 1
        elif code.startswith("update"):
            quyen['update'] = 1
        elif code.startswith("delete"):
            quyen['delete'] = 1

    return list(lst_result.values())

def get_quyen_chuc_vu(chuc_vu_id):
    if chuc_vu_id:
        query = text(f"""
                    SELECT code, type, show_in_menu, quyen.created_at, quyen.updated_at, quyen.deleted_at
                    FROM quyen 
                        LEFT JOIN 
                            chuc_vu ON quyen.chuc_vu_id = chuc_vu.id
                        LEFT JOIN 
                            chuc_nang ON quyen.chuc_nang_id = chuc_nang.id
                    WHERE chuc_vu.id = {chuc_vu_id}
                """)
        
        data = db.session.execute(query).fetchall()
        result = config_data_quyen_chuc_vu(data)
        return result

def add_quyen_chuc_vu(lst_quyen):

    pass
