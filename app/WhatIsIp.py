from PyQt6.QtCore import QThread, pyqtSignal
import httpx
import asyncio

class IP(QThread):
    checkip = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def run(self):
        self.msleep(1000)
        asyncio.run(self.check_ip())

    async def check_ip(self):
        try:
            async with httpx.AsyncClient() as client:
                get_ip =  await client.get('https://api.ipify.org/')
                if get_ip.status_code == 200:
                    self.checkip.emit(str(get_ip.text))
                else:
                    self.checkip.emit('None')
        except httpx.RequestError as e:
            self.checkip.emit('None')
    