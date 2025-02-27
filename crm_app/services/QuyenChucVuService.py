from crm_app.models.Quyen import Quyen
from crm_app.models.ChucNang import ChucNang
from crm_app import db
from crm_app.services.helpers import get_word_before_dash
from sqlalchemy import text
from flask import make_response
from crm_app.docs.containts import *
from datetime import datetime

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
    print('chuc_vu_id', chuc_vu_id)
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
    
def modify_quyen_chuc_vu(chuc_vu_id, lst_quyen):
    """ 
        lst_quyen từ front-end gửi về phải có dạng \n
        [
            {
                "type": "san-pham",
                "code": "san-pham",
                "value": 0
            }, 
            {
                "type": "san-pham",
                "code": "create-san-pham",
                "value": 1
            }, 
        ]

        Chức năgng
        Kiểm tra có tồn tại hay không -> 
        Nếu True -> Không có -> Thêm
        Nếu False -> có -> Xoá
        
        [
            {
                "code": "create-san-pham"
                "value": 1
            },
        ]
        Lấy toàn bộ chức năng
        -> Nếu mã code trong quyền -> xoá || upset
        -> Nếu mã code không trong quyền -> thêm
    """
    query = text(f"""
                    SELECT chuc_nang.chuc_nang_id, code
                    FROM quyen
                        LEFT JOIN chuc_nang ON quyen.chuc_nang_id = chuc_nang.id
                    WHERE
                        chuc_vu_id = :chuc_vu_id
                """)
    result = db.execute(query, {'chuc_vu_id': chuc_vu_id}).fetchall()

    # code_to_id['san-pham'] => 1
    code_to_id = {row['code']: row['chuc_nang_id'] for row in result}

    if lst_quyen and chuc_vu_id:
        for item in lst_quyen:
            if item.code == item.type:
                new_quyen = Quyen()
            id = code_to_id[item.code]
            if id:
                if item.value == 0:
                    new_quyen = Quyen(chuc_vu_id=chuc_vu_id, chuc_nang_id=chuc_nang_id, deleted_at=datetime.now())
                else:
                    new_quyen = Quyen(chuc_vu_id=chuc_vu_id, chuc_nang_id=chuc_nang_id, deleted_at=None)

                db.session.merge(new_quyen)
            else:
                new_quyen = Quyen(chuc_vu_id=chuc_vu_id, chuc_nang_id=chuc_nang_id, delete_at = None)
        db.session.commit()
    
        return make_response(get_error_response(ERROR_CODES.SUCCESS), 200)