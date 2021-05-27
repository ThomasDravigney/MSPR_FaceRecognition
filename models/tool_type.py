from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.entity import Entity


class ToolType(Entity):
    __tablename__ = 'tool_types'

    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    tools = relationship("Tool", back_populates="tool_type")