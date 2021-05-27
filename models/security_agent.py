from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.entity import Entity


class SecurityAgent(Entity):
    __tablename__ = 'security_agent'

    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    First_name = Column(String)
    CNI = Column(String)
    AI = Column(Integer)
    tools = relationship("Tool", back_populates="security_agent")

