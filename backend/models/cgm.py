from sqlalchemy import Column, Integer, String, DateTime, Enum
# from backend.db.session import Base
from sqlalchemy.sql import func
from backend.models.base import Base

class CGMHistory(Base):
    __tablename__ = "ch_cgm_history"

    user_uid = Column(Integer, nullable=False)
    std_time = Column(DateTime, nullable=False)
    cgm_type = Column(String(50), nullable=False)
    bg = Column(Integer, nullable=False)
    # id = Column(Integer, primary_key=True, autoincrement=True)
    # collector = Column(String(50), nullable=False)
    # device_number = Column(String(100))
    # device_serial = Column(String(100))
    # regist_time = Column(DateTime, nullable=False)
    # modifier_uid = Column(Integer)
    # modifiy_time = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<CGMHistory(id={self.id}, user_uid={self.user_uid}, std_time={self.std_time})>"