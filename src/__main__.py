from PyQt6.QtWidgets import QApplication
from src.view.DiceRollerWindow import DiceRollerWindow

if __name__ == "__main__":
    app: QApplication = QApplication([])
    app.setStyle("Fusion")
    window: DiceRollerWindow = DiceRollerWindow()
    window.show()
    app.exec()
