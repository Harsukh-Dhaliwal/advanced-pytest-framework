import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from infra.security import encrypt_value

DATABASE_URL = "sqlite:///test_data.db"
Base = declarative_base()

class UserTestPersona(Base):
    __tablename__ = 'user_personas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    env = Column(String(50), nullable=False, index=True)
    username = Column(String(100), nullable=False)
    password = Column(String(200), nullable=False)  # Increased length to accept encryption cipher strings
    is_active = Column(Boolean, default=True)

def seed_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    if session.query(UserTestPersona).count() == 0:
        personas = [
            # Passwords are encrypted before committing them to the database
            UserTestPersona(env="qa", username="qa_automation_user", password=encrypt_value("password_qa_123"), is_active=True),
            UserTestPersona(env="staging", username="stage_user", password=encrypt_value("password_stage_123"), is_active=True),
            UserTestPersona(env="prod", username="prod_automation_user", password=encrypt_value("secure_prod_pass_99"), is_active=True),
            UserTestPersona(env="prod", username="locked_user", password=encrypt_value("invalid_password_xyz"), is_active=False)
        ]
        session.add_all(personas)
        session.commit()
    session.close()

if __name__ == "__main__":
    seed_database()
    print("Secure database schema seeded successfully.")