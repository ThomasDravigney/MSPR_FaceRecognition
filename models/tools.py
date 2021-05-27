from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.entity import Entity


class Tool(Entity):
    __tablename__ = 'tools'

    Id = Column(Integer, primary_key=True)
    Serial_number = Column(String)
    Name = Column(String)
    TypeId = Column(Integer, ForeignKey('tool_types.Id'))
    tool_type = relationship("ToolType", back_populates="tools")
    AgentId = Column(Integer, ForeignKey('security_agent.Id'))
    security_agent = relationship("SecurityAgent", back_populates="tools")