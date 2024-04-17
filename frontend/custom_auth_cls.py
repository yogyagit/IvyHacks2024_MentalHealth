from typing import Any, Dict, List, Optional, Tuple, cast

import httpx
from typing_extensions import Literal, TypedDict

from httpx_oauth.errors import GetIdEmailError
from httpx_oauth.oauth2 import BaseOAuth2
from httpx_oauth.clients.google import GoogleOAuth2

AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
ACCESS_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
REVOKE_TOKEN_ENDPOINT = "https://accounts.google.com/o/oauth2/revoke"
BASE_SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
]
PROFILE_ENDPOINT = "https://people.googleapis.com/v1/people/me"

class GoogleOAuth2_custom(GoogleOAuth2):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        scope: Optional[List[str]] = BASE_SCOPES,
        name="google",
    ):
        super().__init__(
            client_id,
            client_secret,
        )

    async def get_id_details(self, token: str) -> Tuple[str, str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                PROFILE_ENDPOINT,
                #params={"personFields": "emailAddresses"},
                params={"personFields": ["emailAddresses", "names"]},
                headers={**self.request_headers, "Authorization": f"Bearer {token}"},
            )

            if response.status_code >= 400:
                raise GetIdEmailError(response.json())

            data = cast(Dict[str, Any], response.json())

            user_id = data["resourceName"]
            user_first_name = data["names"][0]["givenName"]
            user_last_name = data["names"][0]["familyName"]

            user_email = next(
                email["value"]
                for email in data["emailAddresses"]
                if email["metadata"]["primary"]
            )

            return user_id, user_email, user_first_name, user_last_name