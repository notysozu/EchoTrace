from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import httpx
from core.config import get_settings

settings = get_settings()
security = HTTPBearer(auto_error=False)

_jwks_cache: Optional[dict] = None


async def _get_jwks() -> dict:
    global _jwks_cache
    if _jwks_cache is None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://{settings.auth0_domain}/.well-known/jwks.json"
            )
            resp.raise_for_status()
            _jwks_cache = resp.json()
    return _jwks_cache


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token = credentials.credentials
    try:
        jwks = await _get_jwks()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"], "kid": key["kid"],
                    "use": key["use"], "n": key["n"], "e": key["e"],
                }
        if not rsa_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="RSA key not found")

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=settings.auth0_audience,
            issuer=f"https://{settings.auth0_domain}/",
        )
        return payload
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}")


async def optional_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    """Same as verify_token but returns None if no auth header instead of raising."""
    if not credentials:
        return None
    return await verify_token(credentials)
