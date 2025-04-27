from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QColor, QFont
from PyQt5.QtCore import QTimer, Qt
import sys


def create_icon_with_text(text):
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QColor("#2D89EF"))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, 64, 64)

    # 绘制文字
    painter.setPen(Qt.white)
    font = QFont("Arial", 20)
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
    painter.end()

    return QIcon(pixmap)


class TrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tray = QSystemTrayIcon()
        self.tray.setToolTip("状态中...")
        self.tray.setIcon(create_icon_with_text("0%"))

        # 菜单
        menu = QMenu()
        exit_action = QAction("退出")
        exit_action.triggered.connect(self.app.quit)
        menu.addAction(exit_action)
        self.tray.setContextMenu(menu)

        self.tray.show()

        # 定时更新图标
        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_icon)
        self.timer.start(1000)

    def update_icon(self):
        self.counter = (self.counter + 5) % 105
        self.tray.setIcon(create_icon_with_text(f"{self.counter}%"))

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = TrayApp()
    app.run()
