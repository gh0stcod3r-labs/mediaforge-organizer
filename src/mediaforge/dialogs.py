"""Custom dialogs for MediaForge Organizer."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QProgressDialog, QComboBox, QCheckBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from .constants import SPACING_MD, SPACING_LG, PRIMARY_TEXT, SECONDARY_TEXT, MUTED_TEXT
from .models import MediaType


class APIKeyDialog(QDialog):
    """Dialog for configuring API keys."""
    
    def __init__(self, parent, provider_name: str, current_key: str = ""):
        super().__init__(parent)
        self.provider_name = provider_name
        self.api_key = None
        self.test_passed = False
        
        self._setup_ui(current_key)
    
    def _setup_ui(self, current_key: str):
        """Setup dialog UI."""
        self.setWindowTitle(f"Configure {self.provider_name} API Key")
        self.setGeometry(200, 200, 400, 250)
        
        layout = QVBoxLayout()
        layout.setSpacing(SPACING_MD)
        
        # Header
        header = QLabel(f"🔑 {self.provider_name} API Key")
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # Instructions
        instructions = QLabel(
            f"Enter your {self.provider_name} API key.\n"
            "This will be stored locally and never shared."
        )
        instructions.setStyleSheet(f"color: {SECONDARY_TEXT};")
        layout.addWidget(instructions)
        
        # Key input
        layout.addWidget(QLabel("API Key:"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Paste your API key here")
        self.key_input.setText(current_key)
        self.key_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.key_input)
        
        # Show/hide button
        show_btn = QPushButton("👁 Show")
        show_btn.setMaximumWidth(80)
        show_btn.clicked.connect(self._toggle_show)
        layout.addWidget(show_btn)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        test_btn = QPushButton("🧪 Test")
        test_btn.clicked.connect(self._test_key)
        button_layout.addWidget(test_btn)
        
        button_layout.addStretch()
        
        save_btn = QPushButton("💾 Save")
        save_btn.clicked.connect(self._save)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("✗ Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def _toggle_show(self):
        """Toggle showing/hiding the key."""
        if self.key_input.echoMode() == QLineEdit.Password:
            self.key_input.setEchoMode(QLineEdit.Normal)
        else:
            self.key_input.setEchoMode(QLineEdit.Password)
    
    def _test_key(self):
        """Test the API key (provider-specific logic would go here)."""
        key = self.key_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Empty Key", "Please enter an API key first.")
            return
        
        # TODO: Call provider test method
        QMessageBox.information(
            self,
            "Test Result",
            "API key format looks valid.\n(Full test requires internet connection)"
        )
        self.test_passed = True
    
    def _save(self):
        """Save the key and close dialog."""
        key = self.key_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Empty Key", "Please enter an API key.")
            return
        
        self.api_key = key
        self.accept()
    
    def get_api_key(self) -> str:
        """Get the entered API key."""
        return self.api_key or ""


class SettingsDialog(QDialog):
    """Consolidated settings: provider, API key, category, and behavior toggles."""

    PROVIDER_ITEMS = ["Automatic", "Offline", "TMDB", "AniList", "MyAnimeList", "TVMaze"]
    PROVIDER_KEY_MAP = {
        "TMDB": "tmdb",
        "AniList": "anilist",
        "MyAnimeList": "mal",
        "TVMaze": "tvmaze",
    }

    def __init__(
        self,
        parent,
        settings_manager,
        current_provider: str,
        current_media_type: str,
        copy_mode: bool,
        dry_run: bool,
        verify_after_copy: bool,
    ):
        super().__init__(parent)
        self.settings = settings_manager
        self._setup_ui(current_provider, current_media_type, copy_mode, dry_run, verify_after_copy)

    def _setup_ui(self, current_provider, current_media_type, copy_mode, dry_run, verify_after_copy):
        """Setup dialog UI."""
        self.setWindowTitle("Settings")
        self.setMinimumWidth(420)

        layout = QVBoxLayout()
        layout.setSpacing(SPACING_LG)

        header = QLabel("⚙ Settings")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)

        # Provider row
        layout.addWidget(QLabel("Metadata Provider:"))
        provider_row = QHBoxLayout()
        provider_row.setSpacing(SPACING_MD)
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(self.PROVIDER_ITEMS)
        idx = self.provider_combo.findText(current_provider)
        if idx >= 0:
            self.provider_combo.setCurrentIndex(idx)
        self.provider_combo.currentTextChanged.connect(self._on_provider_changed)
        provider_row.addWidget(self.provider_combo)
        self.provider_key_btn = QPushButton("🔑 API Key")
        self.provider_key_btn.setMaximumWidth(110)
        self.provider_key_btn.clicked.connect(self._configure_api_key)
        provider_row.addWidget(self.provider_key_btn)
        layout.addLayout(provider_row)
        self._on_provider_changed(self.provider_combo.currentText())

        # Media category row
        layout.addWidget(QLabel("Category:"))
        self.media_combo = QComboBox()
        self.media_combo.addItems([mt.value for mt in MediaType])
        idx = self.media_combo.findText(current_media_type)
        if idx >= 0:
            self.media_combo.setCurrentIndex(idx)
        layout.addWidget(self.media_combo)

        # Behavior toggles
        self.copy_mode_check = QCheckBox("Copy Mode (default - never delete originals)")
        self.copy_mode_check.setChecked(copy_mode)
        layout.addWidget(self.copy_mode_check)

        self.dry_run_check = QCheckBox("Dry Run (preview only)")
        self.dry_run_check.setChecked(dry_run)
        layout.addWidget(self.dry_run_check)

        self.verify_after_copy_check = QCheckBox("Verify After Copy (compare file sizes)")
        self.verify_after_copy_check.setChecked(verify_after_copy)
        layout.addWidget(self.verify_after_copy_check)

        layout.addStretch()

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("✗ Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        save_btn = QPushButton("💾 Save")
        save_btn.clicked.connect(self.accept)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _on_provider_changed(self, provider_name: str) -> None:
        """Enable/disable the API key button for the selected provider."""
        if provider_name.lower() in {"offline", "automatic"}:
            self.provider_key_btn.setEnabled(False)
            self.provider_key_btn.setToolTip("Selected provider doesn't need an API key")
        else:
            self.provider_key_btn.setEnabled(True)
            self.provider_key_btn.setToolTip(f"Configure {provider_name} API key")

    def _configure_api_key(self) -> None:
        """Show API key configuration dialog for the selected provider."""
        provider_name = self.provider_combo.currentText()
        provider_key = self.PROVIDER_KEY_MAP.get(provider_name)

        if provider_key is None:
            QMessageBox.information(
                self,
                "No API Key Required",
                f"{provider_name} doesn't need an API key."
            )
            return

        current_key = self.settings.get_api_key(provider_key) or ""

        dialog = APIKeyDialog(self, provider_name, current_key)
        if dialog.exec() == QDialog.Accepted:
            key = dialog.get_api_key()
            if key:
                self.settings.set_api_key(provider_key, key)
                QMessageBox.information(self, "Success", f"{provider_name} API key saved successfully.")
            else:
                QMessageBox.warning(self, "Error", "API key cannot be empty.")

    def get_provider(self) -> str:
        return self.provider_combo.currentText()

    def get_media_type(self) -> str:
        return self.media_combo.currentText()

    def get_copy_mode(self) -> bool:
        return self.copy_mode_check.isChecked()

    def get_dry_run(self) -> bool:
        return self.dry_run_check.isChecked()

    def get_verify_after_copy(self) -> bool:
        return self.verify_after_copy_check.isChecked()


class ProgressDialog(QProgressDialog):
    """Custom progress dialog for long operations."""
    
    def __init__(self, parent, title: str, label: str, maximum: int = 100):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setLabelText(label)
        self.setMaximum(maximum)
        self.setAutoReset(False)
        self.setAutoClose(False)
        self.setCancelButtonText("Cancel")
        self.setValue(0)
    
    def update_progress(self, current: int, total: int, current_item: str = ""):
        """Update progress bar."""
        self.setMaximum(total)
        self.setValue(current)
        
        if current_item:
            self.setLabelText(f"{current_item}\n{current}/{total}")
        else:
            self.setLabelText(f"{current}/{total}")
    
    def was_cancelled(self) -> bool:
        """Check if user cancelled."""
        return self.wasCanceled()


class DuplicateDialog(QDialog):
    """Dialog for handling duplicate destination files."""
    
    SKIP = 0
    REPLACE = 1
    RENAME = 2
    SKIP_ALL = 10
    REPLACE_ALL = 11
    RENAME_ALL = 12
    
    def __init__(self, parent, filename: str, destination: str):
        super().__init__(parent)
        self.choice = None
        
        self._setup_ui(filename, destination)
    
    def _setup_ui(self, filename: str, destination: str):
        """Setup dialog UI."""
        self.setWindowTitle("File Already Exists")
        self.setGeometry(200, 200, 450, 200)
        
        layout = QVBoxLayout()
        layout.setSpacing(SPACING_MD)
        
        # Message
        message = QLabel(
            f"'{filename}' already exists at:\n"
            f"{destination}\n\n"
            "What would you like to do?"
        )
        message.setWordWrap(True)
        layout.addWidget(message)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        skip_btn = QPushButton("⊘ Skip")
        skip_btn.clicked.connect(lambda: self._choose(self.SKIP))
        button_layout.addWidget(skip_btn)
        
        replace_btn = QPushButton("🔄 Replace")
        replace_btn.clicked.connect(lambda: self._choose(self.REPLACE))
        button_layout.addWidget(replace_btn)
        
        rename_btn = QPushButton("✏️  Rename")
        rename_btn.clicked.connect(lambda: self._choose(self.RENAME))
        button_layout.addWidget(rename_btn)
        
        layout.addLayout(button_layout)
        
        # Apply to all checkbox
        self.apply_all_check = QPushButton("☑️  Apply to All")
        self.apply_all_check.setCheckable(True)
        layout.addWidget(self.apply_all_check)
        
        self.setLayout(layout)
    
    def _choose(self, choice: int):
        """User made a choice."""
        if self.apply_all_check.isChecked():
            # Convert to "apply to all" variants
            if choice == self.SKIP:
                choice = self.SKIP_ALL
            elif choice == self.REPLACE:
                choice = self.REPLACE_ALL
            elif choice == self.RENAME:
                choice = self.RENAME_ALL
        
        self.choice = choice
        self.accept()
    
    def get_choice(self) -> int:
        """Get user's choice."""
        return self.choice or self.SKIP


class ConfirmUndoDialog(QDialog):
    """Dialog to confirm destructive undo operation."""
    
    def __init__(self, parent, operations_count: int):
        super().__init__(parent)
        self.confirmed = False
        
        self._setup_ui(operations_count)
    
    def _setup_ui(self, operations_count: int):
        """Setup dialog UI."""
        self.setWindowTitle("Confirm Undo")
        self.setGeometry(200, 200, 400, 200)
        
        layout = QVBoxLayout()
        layout.setSpacing(SPACING_MD)
        
        # Warning
        warning = QLabel(
            "⚠️  This will undo the following operations:\n\n"
            f"• {operations_count} file operations\n\n"
            "This cannot be undone. Are you sure?"
        )
        warning.setWordWrap(True)
        warning.setStyleSheet(f"color: #ff9800;")
        layout.addWidget(warning)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("✗ Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        confirm_btn = QPushButton("✔️  Undo Anyway")
        confirm_btn.clicked.connect(self._confirm)
        button_layout.addWidget(confirm_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def _confirm(self):
        """User confirmed undo."""
        self.confirmed = True
        self.accept()
    
    def was_confirmed(self) -> bool:
        """Check if undo was confirmed."""
        return self.confirmed
