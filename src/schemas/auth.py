"""
Schemas de autenticação.
Define os modelos de dados para login, tokens e usuários.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    """Schema para requisição de login."""
    username: str                    # Nome de usuário
    password: str                    # Senha


class TokenResponse(BaseModel):
    """Schema para resposta com tokens JWT."""
    access_token: str               # Token de acesso
    refresh_token: str              # Token de refresh
    token_type: str = "bearer"      # Tipo do token


class RefreshRequest(BaseModel):
    """Schema para requisição de refresh de token."""
    refresh_token: str              # Token de refresh


class UserResponse(BaseModel):
    """Schema para resposta com dados do usuário."""
    id: int                         # ID do usuário
    username: str                   # Nome de usuário
    email: Optional[str] = None     # E-mail
    is_active: bool                 # Usuário ativo
    is_admin: bool                  # É administrador
    created_at: Optional[datetime] = None  # Data de criação

    class Config:
        from_attributes = True       # Permite conversão de ORM
