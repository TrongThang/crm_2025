from crm_app.services.utils import *
from crm_app.services.helpers import build_where_query
from crm_app.models.ChucVu import ChucVu
from crm_app import db

def get_chuc_vu(filter):
    build_where = build_where_query(filter=filter) if filter else ''

    query = text(f"""
                    SELECT chuc_vu.id, chuc_vu.ten as ten, created_at, updated_at, deleted_at, chuc_nang.ten as ten_quyen
                    FROM chuc_vu
                        LEFT JOIN 
                            quyen ON quyen.chuc_vu_id = chuc_vu.id
                        LEFT JOIN
                            chuc_nang ON quyen.chuc_nang_id = chuc_nang.id
                    {build_where}
                """)
    data = db.session.execute(query).fetchall()
    chuc_vu_dict = {}

    for row in data:
        id_chuc_vu = row.id
        if id_chuc_vu not in chuc_vu_dict:
            chuc_vu_dict[id_chuc_vu] = {
                'id': row.id,
                'ten': row.ten, 
                'ten_quyen': [],
                'created_at': row.created_at,
                'updated_at': row.updated_at,
                'deleted_at': row.deleted_at,
            }
            if row.ten_quyen:
                chuc_vu_dict[id_chuc_vu]["ten_quyen"].append(row.ten_quyen)

    result = list(chuc_vu_dict.values())

    return result

def post_chuc_vu(ten):
    error = validate_name(name=ten)
    if error:
        return error
    
    chuc_vu = ChucVu(ten=ten)

    db.session.add(chuc_vu)
    db.session.commit()
    return

def put_chuc_vu(id, ten):
    chuc_vu = ChucVu.query.get(id)
    if chuc_vu is None:
        return 
    error = validate_name(name=ten)
    if error:
        return error
    
    chuc_vu = ChucVu(ten=ten)

    db.session.add(chuc_vu)
    db.session.commit()
    
    return get_error_response(ERROR_CODES.SUCCESS)


def delete_chuc_vu(id):
    chuc_vu = ChucVu.query.get(id)
    if chuc_vu is None:
        return
    db.session.delete(chuc_vu)
    db.session.commit()
    return get_error_response(ERROR_CODES.SUCCESS)