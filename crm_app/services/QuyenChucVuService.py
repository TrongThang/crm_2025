from crm_app.models.Quyen import Quyen
from crm_app.models.ChucNang import ChucNang
from crm_app.models.ChucVu import ChucVu
from crm_app import db
from crm_app.services.helpers import get_word_before_dash
from sqlalchemy import text
from flask import make_response, current_app
from crm_app.docs.containts import *
from crm_app.services.utils import isExistId
from datetime import datetime
from crm_app import redis_client
import json
from collections import defaultdict

def config_data_quyen_chuc_vu(chuc_vu_quyen, quyen_all):
    """return
        [
            {
                "show_in_menu": "nhân viên",
                "type": "nhan-vien",
                "quyen": [
                    {
                        "ten": "Xem danh sách",
                        "code": "view",
                        "id":  1,
                        "trang_thai": 1
                    },
                    {
                        "ten": "Cập nhật nhân viên",
                        "code": "update",
                        "id":  2,
                        "trang_thai": 0
                    }
                ]
            }
        ]
    """
    lst_result = {}
    print(chuc_vu_quyen)
    quyen_dict_chuc_vu = {row['id']: {'id': row['id'], 'deleted_at': row['deleted_at']} for row in chuc_vu_quyen}
    print("quyen_dict:", quyen_dict_chuc_vu)
    for chuc_nang in quyen_all:
        chuc_nang_id = chuc_nang['id']  # id của chức năng
        code = chuc_nang['code']  # code của chức năng
        type = chuc_nang['type']  # type của chức năng
        show_in_menu = chuc_nang['show_in_menu']  # show_in_menu
        ten = chuc_nang['ten']  # ten

        quyen = lst_result.setdefault(type, {
            'hien_thi_menu': show_in_menu,
            'loai_quyen': type,
            'quyen': []
        })  

        # Kiểm tra xem quyền có tồn tại trong danh sách `chuc_vu_quyen` không
        print(f"if {chuc_nang_id} in {chuc_nang_id in quyen_dict_chuc_vu} and  is None")
        
        trang_thai = 1 if chuc_nang_id in quyen_dict_chuc_vu and quyen_dict_chuc_vu[chuc_nang_id]['deleted_at'] is None else 0

        quyen['quyen'].append({
            'ten': ten, 
            'code': code,
            'id': chuc_nang_id,
            'trang_thai': trang_thai
        })

    return list(lst_result.values())

#GET
def get_all_employee_role():
    query = text(
    """
        SELECT id, chuc_vu_id
        FROM nhan_vien
        WHERE deleted_at IS NULL
    """
    )

    result = db.session.execute(query).mappings().fetchall()

    return result

def get_all_permission_role():
    with current_app.app_context():
        query = text(
        """
            SELECT chuc_vu_id, chuc_nang_id
            FROM quyen
            WHERE deleted_at IS NULL
        """
        )

        result_chuc_vu = db.session.execute(query).mappings().fetchall()

        
        chuc_vu_quyen_dict = defaultdict(list)
        for row in result_chuc_vu:
            chuc_vu_quyen_dict[row["chuc_vu_id"]].append(row["chuc_nang_id"])

    # Output: {5: [1, 2], 6: [2], ...}
    return chuc_vu_quyen_dict

def get_quyen_chuc_vu(chuc_vu_id):
    if chuc_vu_id:      
        query = text(f"""
                    SELECT chuc_nang.id, code, ten, type, show_in_menu, quyen.created_at, quyen.updated_at, quyen.deleted_at
                    FROM quyen 
                        LEFT JOIN 
                            chuc_nang ON quyen.chuc_nang_id = chuc_nang.id
                    WHERE quyen.chuc_vu_id = {chuc_vu_id}
                """)
        
        chuc_vu_quyen = db.session.execute(query).mappings().fetchall()

        query_all = text(f"""
            SELECT id, code, type, show_in_menu, ten
            FROM chuc_nang
        """)
        quyen_all = db.session.execute(query_all).mappings().fetchall()
        print(quyen_all)
        result = config_data_quyen_chuc_vu(chuc_vu_quyen=chuc_vu_quyen, quyen_all=quyen_all)
        return result

def check_action(chuc_vu_id, chuc_nang_id):
    query = text(""" SELECT id FROM quyen WHERE chuc_vu_id = :chuc_vu_id AND chuc_nang_id = :chuc_nang_id AND deleted_at IS NULL """)

    id = db.session.execute(query, {chuc_nang_id: chuc_vu_id, chuc_nang_id: chuc_nang_id}).scalar()

    if id:
        return True

    return False


def modify_quyen_chuc_vu(chuc_vu_id, list_quyen):
    """ 
        lst_quyen từ front-end gửi về phải có dạng \n
        [
            {
                "id": 3,
                "active": 0
            }, 
            {
                "id": 4,
                "active": 1
            }, 
        ]
    """

    if not isExistId(id=chuc_vu_id, model=ChucVu):
        return make_response(get_error_response(ERROR_CODES.CHUC_VU_NOT_FOUND), 401)
    
    query = text(f"""
                    SELECT quyen.id as id_quyen, chuc_nang.id as chuc_nang_id
                    FROM quyen
                        LEFT JOIN chuc_nang ON quyen.chuc_nang_id = chuc_nang.id
                    WHERE
                        chuc_vu_id = :chuc_vu_id
                    ORDER BY chuc_nang_id 
                """)
    result = db.session.execute(query, {'chuc_vu_id': chuc_vu_id}).mappings().fetchall()

    # code_to_id['29'] => 1
    chuc_nang_to_id_quyen = {row["chuc_nang_id"]: row["id_quyen"] for row in result}
    if list_quyen and chuc_vu_id:
        # Kiểm tra các item trong lst_quyen -> Nếu như có id_quyen trong danh sách thì sẽ kiểm tra value
        # Nếu = 0 
        #   + Có quyền đó trong danh sách =>  upset deleted_at = datetime.now() -> Đã xoá
        #   + Không có => thêm mới một quyền vào
        for item in list_quyen:
            chuc_nang_id = item["id"] 
            
            if not isExistId(id=chuc_nang_id, model=ChucNang):
                return make_response(get_error_response(ERROR_CODES.CHUC_NANG_NOT_FOUND), 401)
            
            id_quyen = chuc_nang_to_id_quyen.get(chuc_nang_id)
            print("id quyền trước kiểm tra:", id_quyen)
            if id_quyen:
                quyen = Quyen(id = id_quyen, chuc_vu_id=chuc_vu_id, chuc_nang_id=chuc_nang_id, deleted_at = None)
                if item["active"] == 0:
                    quyen.deleted_at = datetime.now()
                else:
                    quyen.deleted_at = None
                db.session.merge(quyen)
            else:
                new_quyen = Quyen(chuc_vu_id=chuc_vu_id, chuc_nang_id=chuc_nang_id, deleted_at = None)
                db.session.add(new_quyen)
        db.session.commit()

        updated_query = text("""
                SELECT chuc_nang_id
                FROM quyen
                WHERE chuc_vu_id = :chuc_vu_id AND deleted_at IS NULL
            """)
        
        updated_result = db.session.execute(updated_query, {'chuc_vu_id': chuc_vu_id}).mappings().fetchall()

        quyen_list = [row['chuc_nang_id'] for row in updated_result]

        # Lưu vào Redis (ví dụ: key theo dạng "quyen:{chuc_vu_id}")
        redis_key = f"quyen:{chuc_vu_id}"
        redis_client.smembers(redis_key, json.dumps(quyen_list))

        redis_data = redis_client.get(redis_key)
        quyen_list_from_redis = json.loads(redis_data) if redis_data else []

        print("Redis được lưu:", redis_data)  # In ra dạng bytes
        print("Danh sách quyền từ Redis:", quyen_list_from_redis)
        
        return make_response(get_error_response(ERROR_CODES.SUCCESS), 200)