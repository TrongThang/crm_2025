from crm_app.models.Quyen import Quyen
from crm_app.models.ChucNang import ChucNang
from crm_app.models.ChucVu import ChucVu
from crm_app import db
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

        trang_thai = 1 if chuc_nang_id in quyen_dict_chuc_vu and quyen_dict_chuc_vu[chuc_nang_id]['deleted_at'] is None else 0

        quyen['quyen'].append({
            'ten': ten, 
            'code': code,
            'ID': chuc_nang_id,
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
            SELECT chuc_vu_id, code
            FROM quyen
                LEFT JOIN chuc_nang ON chuc_nang.id = quyen.chuc_nang_id
            WHERE chuc_nang.deleted_at IS NULL 
                AND quyen.deleted_at IS NULL
        """
        )

        query_all = text(
        """
            SELECT code
            FROM chuc_nang
            WHERE chuc_nang.deleted_at IS NULL
        """
        )

        result_chuc_vu = db.session.execute(query).mappings().fetchall()

        
        chuc_vu_quyen_dict = defaultdict(list)
        for row in result_chuc_vu:
            chuc_vu_quyen_dict[row["chuc_vu_id"]].append(row["code"])

        all_chuc_vu = db.session.execute(query_all).mappings().fetchall()
        for row in all_chuc_vu:
            chuc_vu_quyen_dict[1].append(row["code"])
        print(all_chuc_vu)
    # Output: {5: ['view-san-pham', 'create-san-pham', 'create-nhan-vien'], 6: ['view-ton-kho'], ...}
    return chuc_vu_quyen_dict

def get_quyen_chuc_vu(chuc_vu_id):
    if not chuc_vu_id:
        with current_app.app_context():
            query = text(
            """
                SELECT chuc_vu_id, code, chuc_nang.ten as ten_chuc_nang
                FROM quyen
                    LEFT JOIN chuc_nang ON chuc_nang.id = quyen.chuc_nang_id
                WHERE chuc_nang.deleted_at IS NULL 
                    AND quyen.deleted_at IS NULL
            """
            )

            result_chuc_vu = db.session.execute(query, {"chuc_vu_id":chuc_vu_id}).mappings().fetchall()

            permissions_list = []
            for row in result_chuc_vu:
                permissions_list.append({
                    "code": row["code"],
                    "ten_chuc_nang": row["ten_chuc_nang"]
                })

            return permissions_list
    if chuc_vu_id:      
        query = text(f"""
                    SELECT chuc_nang.id, code, ten, type, show_in_menu, quyen.created_at, quyen.updated_at, quyen.deleted_at
                    FROM quyen 
                        LEFT JOIN 
                            chuc_nang ON quyen.chuc_nang_id = chuc_nang.id
                    WHERE quyen.chuc_vu_id = {chuc_vu_id} AND quyen.deleted_at IS NULL
                """)
        
        chuc_vu_quyen = db.session.execute(query).mappings().fetchall()

        query_all = text(f"""
            SELECT id, code, type, show_in_menu, ten
            FROM chuc_nang
        """)
        quyen_all = db.session.execute(query_all).mappings().fetchall()
        result = config_data_quyen_chuc_vu(chuc_vu_quyen=chuc_vu_quyen, quyen_all=quyen_all)
        response_data = {"data": result}
        return get_error_response(ERROR_CODES.SUCCESS, result=response_data)

def modify_quyen_chuc_vu(chuc_vu_id, list_quyen):
    """ 
        {
            "chuc_vu_id": 2,
            "quyen": [
                {
                    "id": 3, 
                    "code": "view-san-pham",
                    "active": 0
                }, 
                {
                    "id": 5,
                    "code": "create-nhan-vien",
                    "active": 0
                },
                {
                    "id": 9,
                    "code": "delete-nhan-vien",
                    "active": 1
                },
                    {
                    "id": 18,
                    "code": "view-don-vi-tinh",
                    "active": 1
                }
            ]
        }
    """
    try:
        if not isExistId(id=chuc_vu_id, model=ChucVu):
            return make_response(get_error_response(ERROR_CODES.CHUC_VU_NOT_FOUND), 401)
        
        query = text(f"""
                        SELECT quyen.id as id_quyen, chuc_nang.id as chuc_nang_id, code
                        FROM quyen
                            LEFT JOIN chuc_nang ON quyen.chuc_nang_id = chuc_nang.id
                        WHERE
                            chuc_vu_id = :chuc_vu_id AND quyen.deleted_at IS NULL
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
            lst_new_quyen = set({})
            lst_deleted_quyen = set({})
            for item in list_quyen:
                chuc_nang_id = item["ID"]
                active = item["active"]
                if not isExistId(id=chuc_nang_id, model=ChucNang):
                    return make_response(get_error_response(ERROR_CODES.CHUC_NANG_NOT_FOUND), 401)
                
                id_quyen = chuc_nang_to_id_quyen.get(chuc_nang_id)
                if id_quyen:
                    quyen = Quyen(id = id_quyen, chuc_vu_id=chuc_vu_id, chuc_nang_id=chuc_nang_id, deleted_at = None)
                    if active == 0:
                        lst_deleted_quyen.add(chuc_nang_id)
                    db.session.merge(quyen)
                elif active == 1:
                    quyen = Quyen.query.filter_by(chuc_vu_id=chuc_vu_id, chuc_nang_id=chuc_nang_id, deleted_at = None).first()
                    if not quyen:
                        # new_quyen = Quyen(chuc_vu_id=chuc_vu_id, chuc_nang_id=chuc_nang_id, deleted_at = None)
                        # db.session.add(new_quyen)
                        # db.session.flush()
                        lst_new_quyen.add(chuc_nang_id)
            print('ds thêm quyền:', lst_new_quyen)
            print('ds xoá quyền:', lst_deleted_quyen)
            for id in lst_deleted_quyen:
                quyen_delete = Quyen.query.filter_by(chuc_vu_id=chuc_vu_id, chuc_nang_id=id, deleted_at = None).first()
                print('id xoá:',quyen_delete.id)
                if quyen_delete:
                    quyen_delete.soft_delete()
            
            for id in lst_new_quyen:
                print("id thêm:", id)
                quyen = Quyen.query.filter_by(chuc_vu_id=chuc_vu_id, chuc_nang_id=id, deleted_at = None).first()
                if not quyen:
                    new_quyen = Quyen(chuc_vu_id=chuc_vu_id, chuc_nang_id=id) 
                    db.session.add(new_quyen)
                    db.session.flush()

            print('Hoàn thành cập nhật quyền!!')
            db.session.commit()

            # Cập nhật vào redis thay đổi các quyền của chức vụ
            result = update_permission_in_redis(chuc_vu_id=chuc_vu_id, lst_add_permission=lst_new_quyen, lst_remove_permission=lst_deleted_quyen)

            return make_response(get_error_response(ERROR_CODES.SUCCESS), 200)
    except Exception as e:
        return make_response(str(e), 500)

def update_permission_in_redis(chuc_vu_id, lst_add_permission = None, lst_remove_permission = None):
    redis_key = f"quyen:{chuc_vu_id}"
    # Xóa quyền không còn sử dụng
    if lst_remove_permission:
        for remove_permission_code in lst_remove_permission:
            redis_client.srem(redis_key, remove_permission_code)
            print(f"Xoá quyền: {remove_permission_code}")

    # Thêm quyền mới
    if lst_add_permission:
        for add_permission_code in lst_add_permission:
            redis_client.sadd(redis_key, add_permission_code)
            print(f"Thêm quyền: {add_permission_code}")

    # Kiểm tra lại danh sách quyền trong Redis
    updated_permissions = redis_client.smembers(redis_key)
    updated_permissions = {p.decode("utf-8") for p in updated_permissions}
    print("Danh sách quyền sau khi cập nhật:", updated_permissions)

    return (updated_permissions, True)