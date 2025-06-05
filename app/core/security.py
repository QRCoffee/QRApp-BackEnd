from fastapi.security import HTTPBearer

JWTSecurity = HTTPBearer(
    bearerFormat="Bearer",
    scheme_name="AccessToken",
    auto_error=False,
) 