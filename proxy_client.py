import requests
import random
from utils.utils import *
from dataclasses import dataclass


@dataclass
class ProxyData:
    protocol: str
    proxy: str

class ProxyClient:
    def __init__(
        self, 
        proxies: list[ProxyData],
        *, 
        retries: int, 
        timeout: int = 60
    ) -> None:
        self.proxies = proxies
        self.retries = retries
        self.timeout = timeout
        self.user_agent = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" }

    @staticmethod
    def proxy_request(method: str, url: str, proxy: ProxyData, **kwargs) -> requests.Response:
        return requests.request(
            method,
            url,
            proxies={ "http": f"{proxy.protocol}://{proxy.proxy}", "https": f"{proxy.protocol}://{proxy.proxy}" },
            **kwargs
        )
    
    @debug("<ProxyClient.retry>: {debug_exc}")
    def retry(
        self,
        method,
        url: str,
        **kwargs
    ) -> requests.Response | None:
        for _ in range(self.retries):
            all_proxies = list(self.proxies)

            while all_proxies:
                random.shuffle(all_proxies)
                proxy = all_proxies.pop()

                try:
                    req = self.proxy_request(method, url, proxy, timeout=self.timeout, headers=self.user_agent, **kwargs)
                    req.raise_for_status()
                except requests.RequestException: continue

                return req
        
        #raise requests.RequestException(f"All {self.retries} retries exhausted. Request failed")


            
def map_proxies(protocol: str, proxies: list[str]) -> list[ProxyData]:
    return [
        ProxyData(protocol, i) 
        for i in proxies
    ]
