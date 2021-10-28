# Classes to control the LED strings via async remote HTTP request.

import aiohttp
import asyncio
from dataclasses import dataclass, asdict

# Data class for light settings. NB we never use saturation or color temp, 
# so they're removed.
@dataclass
class LEDPreset:
    palette: int = 0
    primary_pattern: int = 0
    secondary_pattern: int = 0
    brightness: float = 0.9

class LEDs:
    currentSettings = {}

    allowedSettings = (
        "brightness",
        "palette",
        "primary_pattern",
        "primary_scale",
        "primary_speed",
        "secondary_pattern",
        "secondary_scale",
        "secondary_speed"
    )

    def apply(self, new_preset: LEDPreset):
        requests_to_send = {}
        for k, v in asdict(new_preset).items():
            if k not in self.currentSettings or self.currentSettings[k] != v:
                if k not in self.allowedSettings:
                    print("Cowardly refusing to set unknown key: " + k)
                    continue
                requests_to_send[k] = v
        asyncio.run(self.send_requests(requests_to_send))

    async def send_request(self, session, k, v):
        url = 'http://localhost/setparam?key={}&value={}'.format(k, v)
        async with session.get(url) as resp:
            response_text = await resp.text()
        if resp.status == 200:
            return k
        print('Failed to set {}, response status {}: {}'.format(
            k, resp.status, response_text))

    async def send_requests(self, requests_to_send=dict):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for k, v in requests_to_send.items():
                tasks.append(asyncio.ensure_future(
                    self.send_request(session, k, v)))
            keys_set = await asyncio.gather(*tasks)
            if keys_set is not None:
                for key in keys_set:
                    self.currentSettings[key] = requests_to_send[key]
