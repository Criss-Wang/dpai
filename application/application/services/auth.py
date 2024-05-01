import os

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class APIConfig:
    def __init__(self):
        super().__init__()
        self.bearer_token = os.environ["BEARER_TOKEN"]


class TokenBearer(HTTPBearer):
    """
    FastAPI middleware to check for a valid authorization token in the Bearer header.
    """

    def __init__(self, token: str, auto_error: bool = True):
        super(TokenBearer, self).__init__(auto_error=auto_error)
        self._token = token

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            TokenBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            if credentials.credentials == self._token:
                return credentials.credentials
            else:
                raise HTTPException(
                    status_code=403, detail="Invalid authorization code."
                )
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


def create_token_bearer() -> TokenBearer:
    """
    Factory function to instantiate the TokenBearer middleware
    :return: the initialized middleware
    """
    config = APIConfig()
    return TokenBearer(token=config.bearer_token)


class AuthenticationError(Exception):
    pass
