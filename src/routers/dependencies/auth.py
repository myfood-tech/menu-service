from typing import List, Union

from fastapi import Header, HTTPException

import os

from src.modules.admin_auth import AdminAuther


async def check_username_token_header__return_status(
        x_token: Union[str, None] = Header(default=None),
        x_username: Union[str, None] = Header(default=None)
    ):
    
    if os.environ.get("STAGE", "") == "dev":
        print("ALERT: STAGE IS DEV – NO AUTH")
        check_token = "admin_dev_pass"
        if x_token != check_token:
            print(f"AdminAuth | dev_user: {x_username} access_rejected")
            return 403
    else:
        status_code = AdminAuther.check_token(x_username, x_token)
        if status_code != 200:
            print(f"AdminAuth | user: {x_username} access_rejected")
            return status_code
    print(f"AdminAuth | user: {x_username} access_granted")
    return 200

async def check_username_token_header(
        x_token: Union[str, None] = Header(default=None),
        x_username: Union[str, None] = Header(default=None)
    ):
    status_code = await check_username_token_header__return_status(x_token, x_username)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail="Token check failed")

