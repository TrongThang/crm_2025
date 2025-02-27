from sqlalchemy import Column, Integer, TIMESTAMP
from datetime import datetime
from crm_app import db

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(TIMESTAMP)

    def soft_delete(self):
        """Đánh dấu bản ghi là đã bị xóa."""
        print(datetime.now())
        self.deleted_at = datetime.now()
        # db.session.add(self)
        db.session.commit()

    def restore(self):
        """Khôi phục bản ghi đã bị xóa mềm."""
        self.deleted_at = None
        db.session.commit()

    @classmethod
    def get_active(cls):
        """Lấy danh sách bản ghi chưa bị xóa mềm."""
        return cls.query.filter(cls.deleted_at.is_(None)).all()
    
    def delete_permanently(cls, obj_id):
        """Xóa cứng bản ghi (xóa khỏi database)."""
        obj = cls.query.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False
    
    @classmethod
    def serialize_list(cls, data):
        """Chuyển đổi danh sách các đối tượng thành danh sách dictionary."""
        return [item.to_dict() for item in data]