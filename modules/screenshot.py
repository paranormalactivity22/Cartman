from modules.proxy import ProxyManager
from PyQt5.QtNetwork import QNetworkProxy
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QApplication

class Screenshot(QWebEngineView):
    def __init__(self):
        super().__init__()

    def capture(self, url : str, output_file : str, _proxy : ProxyManager) -> None:
        # Objects
        self._proxy = _proxy
        if url.startswith("http"):
            self.url = url
        else:
            self.url = "http://" + url
    
        # String
        self.output_file = output_file
        
        # open link
        self.open_web()
        
    def open_web(self):
        if self._proxy.getProxyLen() > 0:
            current_proxy = self._proxy.getRandomProxy()
            current_proxy = current_proxy.split(":")
        
            proxy = QNetworkProxy()
            proxy.setType(QNetworkProxy.HttpProxy)
            proxy.setHostName(current_proxy[0])
            proxy.setPort(int(current_proxy[1]))

            QNetworkProxy.setApplicationProxy(proxy)

        try:
            self.load(QUrl(self.url))
            self.loadFinished.connect(self.on_loaded)
            # Create hidden view without scrollbars
            self.setAttribute(Qt.WA_DontShowOnScreen)
            self.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
            self.show()
        except RuntimeError as e:
            print(f"[!] Failed to take a screenshot on {self.url}. Exception : {e}")
        
    def on_loaded(self) -> None:
        self.resize(QSize(1366, 768))
        # Wait for resize
        QTimer.singleShot(2000, self.take_screenshot) # 7500

    def take_screenshot(self) -> None:
        self.grab().save(self.output_file, b'PNG')
        self.app.quit()

class makeScreenshot():
    def __init__(self, qApp : QApplication, info : dict, proxy : ProxyManager) -> None:
        self.screenshoter = Screenshot()
        self.screenshoter.app = qApp
        self.screenshoter.capture(info["url"], f"screenshots/{info['hash']}.png", proxy)
        self.screenshoter.app.exec_()
        print("[#] Screenshot done!")