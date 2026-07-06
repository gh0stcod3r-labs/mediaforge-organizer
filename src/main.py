#!/usr/bin/env python3
"""
MediaForge Organizer - Main entry point
"""
import sys
import logging
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from mediaforge.app import ModernMediaForgeWindow, _get_icon_path


logger = logging.getLogger(__name__)


def main():
    """Launch the MediaForge Organizer application."""
    logger.info("Launching MediaForge from src.main")
    qt_app = QApplication(sys.argv)
    icon_path = _get_icon_path()
    if icon_path:
        qt_app.setWindowIcon(QIcon(str(icon_path)))
    window = ModernMediaForgeWindow()
    window.show()
    sys.exit(qt_app.exec())


if __name__ == "__main__":
    main()
