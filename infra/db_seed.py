import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///test_data.db"
Base = declarative_base()

class UserTestPersona(Base):
    __tablename__ = 'user_personas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    env = Column(String(50), nullable=False, index=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)

def seed_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Only seed if the table is currently empty to avoid duplicating records
    if session.query(UserTestPersona).count() == 0:
        personas = [
            # Add this line right here:
            UserTestPersona(env="qa", username="qa_automation_user", password="password_qa_123", is_active=True),
            
            UserTestPersona(env="staging", username="stage_user", password="password_stage_123", is_active=True),
            UserTestPersona(env="prod", username="prod_automation_user", password="secure_prod_pass_99", is_active=True),
            UserTestPersona(env="prod", username="locked_user", password="invalid_password_xyz", is_active=False)
        ]
        session.add_all(personas)
        session.commit()

if __name__ == "__main__":
    seed_database()
    print("Database schema seeded successfully.")