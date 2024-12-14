from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional
import logging
import json
from datetime import datetime

logger = logging.getLogger("compliance")

class ComplianceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Log access attempt
        await self._log_access(request)
        
        # Verify required headers
        if not self._verify_headers(request):
            return Response(
                content=json.dumps({
                    "detail": "Missing required security headers"
                }),
                status_code=400
            )
        
        # Add security headers to response
        response = await call_next(request)
        return self._add_security_headers(response)
    
    async def _log_access(self, request: Request) -> None:
        """Log access attempts for audit trail"""
        timestamp = datetime.utcnow().isoformat()
        user = await self._get_user_from_request(request)
        logger.info(
            f"Access: {timestamp} | User: {user} | "
            f"Path: {request.url.path} | Method: {request.method}"
        )
    
    def _verify_headers(self, request: Request) -> bool:
        """Verify required security headers"""
        required_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection"
        ]
        return all(header in request.headers for header in required_headers)
    
    def _add_security_headers(self, response: Response) -> Response:
        """Add security headers to response"""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response
    
    async def _get_user_from_request(self, request: Request) -> Optional[str]:
        """Extract user information from request"""
        try:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                # Extract user from JWT token
                token = auth_header.split(" ")[1]
                # Implement JWT decoding here
                return "user_from_token"
        except Exception:
            pass
        return None 