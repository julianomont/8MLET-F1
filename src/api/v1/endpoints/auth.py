"""
Endpoints de autenticação.
Implementa login e refresh de tokens JWT.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from src.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_token,
    get_user_by_username
)

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login",
    description="Autentica o usuário e retorna tokens de acesso e refresh."
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Realiza login e retorna tokens JWT.
    
    - **username**: Nome de usuário
    - **password**: Senha do usuário
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Dados a incluir no token
    token_data = {"sub": user.username, "user_id": user.id, "is_admin": user.is_admin}
    
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data)
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh Token",
    description="Renova o token de acesso usando o refresh token."
)
def refresh_token(
    refresh_data: RefreshRequest,
    db: Session = Depends(get_db)
):
    """
    Renova o access token usando um refresh token válido.
    
    - **refresh_token**: Token de refresh obtido no login
    """
    payload = verify_token(refresh_data.refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verifica se usuário ainda existe e está ativo
    username = payload.get("sub")
    user = get_user_by_username(db, username)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inválido ou inativo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Gera novos tokens
    token_data = {"sub": user.username, "user_id": user.id, "is_admin": user.is_admin}
    
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data)
    )
