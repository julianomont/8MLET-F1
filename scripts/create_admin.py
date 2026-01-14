#!/usr/bin/env python3
"""
Script para criar usuário administrador.
Executa uma vez para configurar o admin inicial.
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.database import SessionLocal, engine, Base
from src.models.user import UserModel
from src.services.auth_service import get_password_hash


def create_admin_user():
    """Cria o usuário administrador padrão."""
    # Garante que as tabelas existem
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Verifica se já existe um admin
        existing_admin = db.query(UserModel).filter(UserModel.username == "admin").first()
        
        if existing_admin:
            print("✓ Usuário admin já existe!")
            print(f"  Username: {existing_admin.username}")
            print(f"  Email: {existing_admin.email}")
            print(f"  Admin: {existing_admin.is_admin}")
            return
        
        # Cria o usuário admin
        admin_user = UserModel(
            username="admin",
            email="admin@booksapi.com",
            hashed_password=get_password_hash("admin-8MLET"),
            is_active=True,
            is_admin=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✓ Usuário admin criado com sucesso!")
        print(f"  Username: admin")
        print(f"  Password: admin-8MLET")
        print(f"  Email: admin@booksapi.com")
        print("\n⚠ IMPORTANTE: Altere a senha padrão em produção!")
        
    except Exception as e:
        print(f"✗ Erro ao criar admin: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_user()
