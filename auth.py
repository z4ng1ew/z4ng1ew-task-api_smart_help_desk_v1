# auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from config import KEYCLOAK_CLIENT_SECRET, KEYCLOAK_REALM, KEYCLOAK_SERVER_URL
# Кэшируем JWKS (публичные ключи) — чтобы не ходить в Keycloak на каждый запрос
from jose import jwk
import httpx
import time


# URL для получения JWKS (публичные ключи для проверки подписи токена)
JWKS_URL = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"

# Алгоритм подписи — всегда RS256 для Keycloak
ALGORITHM = "RS256"

# Схема авторизации — Bearer token
security = HTTPBearer()



_jwks = None
_jwks_fetched_at = 0

def get_jwks():
    global _jwks, _jwks_fetched_at
    if _jwks is None or time.time() - _jwks_fetched_at > 3600:  # обновляем раз в час
        response = requests.get(JWKS_URL)
        response.raise_for_status()
        _jwks = response.json()
        _jwks_fetched_at = time.time()
    return _jwks

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        # Получаем публичные ключи
        jwks = get_jwks()
        
        # Декодируем заголовок токена — чтобы узнать kid (key id)
        header = jwt.get_unverified_header(credentials.credentials)
        kid = header.get("kid")
        
        # Ищем ключ с таким kid
        key = None
        for jwk_item in jwks["keys"]:
            if jwk_item["kid"] == kid:
                key = jwk.construct(jwk_item)
                break
        
        if key is None:
            raise JWTError("Key not found")
        
        # В функции verify_token, при вызове jwt.decode:
        payload = jwt.decode(
            credentials.credentials,
            key,
            algorithms=[ALGORITHM],
            audience="task-service",  # <-- ИЗМЕНИТЬ с "account" на "task-service"
            issuer=f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}"
        )
        
        return payload
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
        )