import sys
import os

# Add current directory to path so it can find 'app'
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.models.user import User, Company
from app.core.security import get_password_hash

def seed_data():
    db = SessionLocal()
    try:
        # 1. Create the Company
        company_name = "Wysele Corp"
        company = db.query(Company).filter(Company.name == company_name).first()
        if not company:
            company = Company(name=company_name)
            db.add(company)
            db.commit()
            db.refresh(company)
            print(f"✅ Company created: {company.name}")

        # 2. Create the Root Super Admin
        admin_email = "admin@wysele.com"
        admin = db.query(User).filter(User.email == admin_email).first()
        
        if not admin:
            # Updated to match the new 3-part name fields
            admin = User(
                email=admin_email,
                hashed_password=get_password_hash("admin123"),
                first_name="System",
                middle_name=None,
                last_name="Admin",
                role="ADMIN", # This user acts as the Super Admin via config.py
                company_id=company.id,
                is_active=True
            )
            db.add(admin)
            db.commit()
            print(f"🚀 Root Admin created successfully: {admin_email}")
        else:
            print("ℹ️ Admin already exists in database.")

    except Exception as e:
        print(f"❌ Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()