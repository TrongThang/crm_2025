from crm_app import redis_client, db
from crm_app.models.ChucVu import ChucVu
from crm_app.models.NhanVien import NhanVien
from crm_app.models.Quyen import Quyen
from sqlalchemy import text
from collections import defaultdict
from crm_app.services.QuyenChucVuService import get_all_employee_role, get_all_permission_role
from flask import current_app
import json

def init_permissions_role_to_redis():
    is_restart = redis_client.get("is_restart")
    
    if not is_restart:
        permission_role_list = get_all_permission_role()
        print('permission_role_list:', permission_role_list.items())
        for chuc_vu_id, quyen_list in permission_role_list.items():
            save_permissions_to_redis(chuc_vu_id=chuc_vu_id, quyen_list=quyen_list)

        print('Cập nhật lại các quyền của chức vụ vào redis mới khởi chạy')


def init_role_employee_to_redis():
    is_restart = redis_client.get("is_restart")
    
    if not is_restart:
        nhan_vien_list = get_all_employee_role()
        for nhan_vien in nhan_vien_list:
            print('nhan-vien-list:', nhan_vien_list)
            nhan_vien_id = nhan_vien.get("id")
            chuc_vu_id = nhan_vien.get("chuc_vu_id")
            save_employee_roles_to_redis(nhan_vien_id=nhan_vien_id, chuc_vu_id=chuc_vu_id)

        print('Cập nhật lại các chức vụ của nhân viên vào redis mới khởi chạy')

def save_permissions_to_redis(chuc_vu_id, quyen_list):
    """
        Lưu quyền cho từng chức vụ
        Ví dụ: quyen: 1 -> {3, 2, 4, 5, 6, 7} (1 là mã chức vụ) - {} là một tập hợp các quyền hạn của chức vụ đó
    """
    redis_key = f"quyen:{chuc_vu_id}"
    ds_quyen = [q for q in quyen_list if q is not None]
    print('ds_quyen:', ds_quyen)
    redis_client.delete(redis_key)

    redis_client.sadd(redis_key, json.dumps(ds_quyen))

    print(f"Lưu quyền thành công cho chức vụ {chuc_vu_id}: {ds_quyen}")

def save_employee_roles_to_redis(nhan_vien_id, chuc_vu_id):
    """
        Lưu chức vụ cho nhân viên
        Ví dụ: nhan_vien: 5 -> 1 (1 là mã chức vụ)
    """
    redis_key = f"nhan_vien:{nhan_vien_id}"

    redis_client.delete(redis_key)

    redis_client.set(redis_key, chuc_vu_id)

    print(f"Lưu chức vụ thành công cho nhân viên {nhan_vien_id}: {chuc_vu_id}")

def get_permission_by_role(chuc_vu_id):
    print("chuc_vu_id:",chuc_vu_id)
    """
        Lấy danh sách quyền theo mã chức vụ
        params: chuc_vu_id: mã chức vụ
        OUTPUT: {'view-nhan-vien', 'create-nhan-vien', 'create-san-pham'}
    """
    redis_key = f"quyen:{chuc_vu_id}"

    return redis_client.smembers(redis_key)

def get_role_by_employee(nhan_vien_id):
    """
        Lấy mã chức vụ theo mã nhân viên truyền vào
        params: nhan_vien_id: mã nhân viên
        output: '3'
    """
    redis_key = f"nhan_vien:{nhan_vien_id}"

    chuc_vu_id = redis_client.get(redis_key)
    print('redis chuc vu:', chuc_vu_id)
    return chuc_vu_id
