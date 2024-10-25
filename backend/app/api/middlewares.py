import base64
import time

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from eth_account import Account

from hexbytes import HexBytes
from eth_account.messages import encode_defunct
from eth_account import Account
from app.config.settings import settings
from app.config.logger import get_logger

logger = get_logger(__name__)

def is_inner_call(path: str):
    for api in ['/get_user_point']:
        if path.find(api) != -1:
            return True

    return False

class Authentication(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        try:
            if is_inner_call(request.scope["path"]):
                if request.client.host == "127.0.0.1":
                    response = await call_next(request)
                    return response
                else:
                    return JSONResponse(
                            status_code=501,
                            content={
                                "status": 501,
                                "message": "Unauthorized call"
                            }
                        )

            # provider = HTTPProvider(configs.http_provider)
            # w3 = Web3(provider)

            # Recover address from signature
            base64Credentials = request.headers["Authorization"].split(" ")[1]
            credentials = base64.b64decode(bytes(base64Credentials,'utf-8')).decode().split(":")
            address,data,signature = credentials
            mesage = encode_defunct(text=data)
            recoveredAddress = Account.recover_message(mesage,signature=HexBytes(signature))

            signed_timestamp = int(data) / 1000
            current_timestamp = time.time()
            diff_seconds = current_timestamp - signed_timestamp

            if diff_seconds > 30 * 2 * 24 * 3600:
                return JSONResponse(
                        content={
                            "status": 440,
                            "message": "Signature expired"
                        }
                    )

            if recoveredAddress.lower() != address.lower():
                return JSONResponse(
                        content={
                            "status": 401,
                            "message": "Authentication failed"
                        }
                    )
            logger.info(f"Request from: {address.lower()}")

            if address.lower() != settings.ADMIN_ADDRESS.lower():
                return JSONResponse(
                        content={
                            "status": 401,
                            "message": "Authentication failed: only admin"
                        }
                    )

            request.state.user_address = address.lower()
            response = await call_next(request)
            return response

        except Exception as e:
            return JSONResponse(
                    status_code=500,
                    content={
                        "status": 500,
                        "message": f"Auth failed, error:{e}"
                    }
                )