import aiohttp
from typing import Literal, Optional, Dict, Any

async def get(url, res_method: Literal["read", "json"], headers: Optional[Dict[str, str]] = None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if res_method == "read":
                return await response.read()
            elif res_method == "json":
                return await response.json()