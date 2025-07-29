from PyQt6.QtCore import QThread, pyqtSignal
import httpx
import asyncio


class ISP(QThread):
    checkisp = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        self.msleep(1000)
        asyncio.run(self.check_isp())

    async def check_isp(self):
        try:
            async with httpx.AsyncClient() as client:
                get_isp = await client.get("https://ipinfo.io/json")
                if get_isp.status_code == 200:
                    data = get_isp.json()
                    self.checkisp.emit(str(data.get("org")))
                else:
                    self.checkisp.emit('None')
        except httpx.RequestError as e:
            self.checkisp.emit('None')
