"""Design constants and theming for MediaForge Organizer."""

# ============================================================================
# Colors
# ============================================================================

# Text Colors
PRIMARY_TEXT = "#F3F4F6"
SECONDARY_TEXT = "#C7CBD3"
MUTED_TEXT = "#9AA3AF"

# Background Colors
BG_DARK = "#1F2937"
BG_DARKER = "#111827"
BG_SURFACE = "#374151"

# Accent Colors
ACCENT_PRIMARY = "#3B82F6"      # Blue
ACCENT_PRIMARY_HOVER = "#2563EB"
ACCENT_PRIMARY_PRESSED = "#1D4ED8"
ACCENT_SUCCESS = "#10B981"       # Green
ACCENT_WARNING = "#F59E0B"       # Amber
ACCENT_ERROR = "#EF4444"         # Red

# Border Colors
BORDER_COLOR = "#4B5563"
BORDER_COLOR_LIGHT = "#6B7280"

# ============================================================================
# Typography
# ============================================================================

# Font Family
FONT_FAMILY = "Segoe UI"

# Font Sizes
HEADER_FONT = 22
TITLE_FONT = 18
SUBTITLE_FONT = 16
BODY_FONT = 14
LIST_ITEM_FONT = 16
LIST_PATH_FONT = 12
SMALL_FONT = 12
TINY_FONT = 10
STATUS_FONT = 11

# Font Weights
FONT_BOLD = 700
FONT_SEMIBOLD = 600
FONT_NORMAL = 400

# ============================================================================
# Spacing
# ============================================================================

# Padding and Margins (in pixels)
SPACING_XS = 4
SPACING_SM = 8
SPACING_MD = 12
SPACING_LG = 16
SPACING_XL = 20
SPACING_2XL = 24
SPACING_3XL = 32

# Common Padding for Components
CARD_PADDING = 20
BUTTON_PADDING = 10
DIALOG_PADDING = 24
INPUT_PADDING = 8

# ============================================================================
# Borders & Radius
# ============================================================================

# Border Radius
CARD_RADIUS = 14
BUTTON_RADIUS = 8
INPUT_RADIUS = 6
SMALL_RADIUS = 4

# Border Width
BORDER_WIDTH = 1
BORDER_WIDTH_THICK = 2

# ============================================================================
# Dimensions
# ============================================================================

# Component Heights
BUTTON_HEIGHT = 40
INPUT_HEIGHT = 36
DIALOG_MIN_WIDTH = 500
DIALOG_MIN_HEIGHT = 300

# Table/List
TABLE_ROW_HEIGHT = 48
TABLE_HEADER_HEIGHT = 40
STATUS_BAR_HEIGHT = 32

# ============================================================================
# Effects
# ============================================================================

# Opacity
OPACITY_DISABLED = 0.5
OPACITY_HOVER = 0.8
OPACITY_ACTIVE = 1.0

# Shadows (for QSS)
SHADOW_SMALL = "0px 1px 2px rgba(0, 0, 0, 0.1)"
SHADOW_MEDIUM = "0px 4px 6px rgba(0, 0, 0, 0.1)"
SHADOW_LARGE = "0px 10px 15px rgba(0, 0, 0, 0.1)"


# ============================================================================
# Theme Generator
# ============================================================================

def get_stylesheet() -> str:
    """Generate QSS stylesheet from design constants."""
    return f"""
    * {{
        background-color: {BG_DARKER};
        color: {PRIMARY_TEXT};
        font-family: '{FONT_FAMILY}';
        font-size: {BODY_FONT}pt;
    }}

    QMainWindow {{
        background-color: {BG_DARKER};
    }}

    QWidget {{
        background-color: {BG_DARKER};
        color: {PRIMARY_TEXT};
    }}

    QLabel {{
        color: {PRIMARY_TEXT};
        background-color: transparent;
    }}

    QLabel#header {{
        color: {PRIMARY_TEXT};
        font-size: {SUBTITLE_FONT}pt;
        font-weight: bold;
    }}

    QLabel#secondary {{
        color: {SECONDARY_TEXT};
    }}

    QLabel#muted {{
        color: {MUTED_TEXT};
    }}

    QLabel#status {{
        color: {PRIMARY_TEXT};
        font-size: {STATUS_FONT}pt;
    }}

    /* Card-style container used for the 3 main columns (input/controls/output) */
    QFrame#panel {{
        background-color: {BG_SURFACE};
        border: {BORDER_WIDTH}px solid {BORDER_COLOR};
        border-radius: {CARD_RADIUS}px;
    }}

    QFrame#titleBar {{
        background-color: {BG_SURFACE};
        border: {BORDER_WIDTH}px solid {BORDER_COLOR};
        border-radius: {CARD_RADIUS}px;
    }}

    QPushButton {{
        background-color: {ACCENT_PRIMARY};
        color: {PRIMARY_TEXT};
        border: none;
        border-radius: {BUTTON_RADIUS}px;
        padding: {BUTTON_PADDING}px {BUTTON_PADDING + 4}px;
        font-weight: bold;
        min-height: {BUTTON_HEIGHT}px;
        min-width: 100px;
    }}

    QPushButton:hover {{
        background-color: {ACCENT_PRIMARY_HOVER};
    }}

    QPushButton:pressed {{
        background-color: {ACCENT_PRIMARY_PRESSED};
    }}

    QPushButton:disabled {{
        background-color: {BG_DARK};
        color: {MUTED_TEXT};
        opacity: {OPACITY_DISABLED};
    }}

    /* Circular icon button used for the Settings gear */
    QToolButton#gearButton {{
        background-color: {ACCENT_PRIMARY};
        color: {PRIMARY_TEXT};
        border: none;
        border-radius: 22px;
        min-width: 44px;
        max-width: 44px;
        min-height: 44px;
        max-height: 44px;
        font-size: 18pt;
        padding: 0px;
    }}

    QToolButton#gearButton:hover {{
        background-color: {ACCENT_PRIMARY_HOVER};
    }}

    QToolButton#gearButton:pressed {{
        background-color: {ACCENT_PRIMARY_PRESSED};
    }}

    QLineEdit {{
        background-color: {BG_DARK};
        color: {PRIMARY_TEXT};
        border: {BORDER_WIDTH}px solid {BORDER_COLOR};
        border-radius: {INPUT_RADIUS}px;
        padding: {INPUT_PADDING}px;
        min-height: {INPUT_HEIGHT}px;
    }}

    QLineEdit:focus {{
        border: {BORDER_WIDTH_THICK}px solid {ACCENT_PRIMARY};
    }}

    QComboBox {{
        background-color: {BG_DARK};
        color: {PRIMARY_TEXT};
        border: {BORDER_WIDTH}px solid {BORDER_COLOR};
        border-radius: {INPUT_RADIUS}px;
        padding: {INPUT_PADDING}px;
        min-height: {INPUT_HEIGHT}px;
    }}

    QComboBox:hover {{
        border: {BORDER_WIDTH}px solid {BORDER_COLOR_LIGHT};
    }}

    QComboBox:focus {{
        border: {BORDER_WIDTH_THICK}px solid {ACCENT_PRIMARY};
    }}

    QComboBox QAbstractItemView {{
        background-color: {BG_DARK};
        color: {PRIMARY_TEXT};
        border: {BORDER_WIDTH}px solid {BORDER_COLOR};
        selection-background-color: {ACCENT_PRIMARY};
    }}

    QCheckBox {{
        color: {PRIMARY_TEXT};
        background-color: transparent;
        spacing: {SPACING_MD}px;
    }}

    QCheckBox::indicator {{
        width: {BUTTON_HEIGHT - 10}px;
        height: {BUTTON_HEIGHT - 10}px;
        border: {BORDER_WIDTH}px solid {BORDER_COLOR};
        border-radius: {SMALL_RADIUS}px;
        background-color: {BG_DARK};
    }}

    QCheckBox::indicator:hover {{
        border: {BORDER_WIDTH}px solid {ACCENT_PRIMARY};
    }}

    QCheckBox::indicator:checked {{
        background-color: {ACCENT_PRIMARY};
        border: {BORDER_WIDTH}px solid {ACCENT_PRIMARY};
    }}

    /* Input file list (left panel) */
    QListWidget {{
        background-color: {BG_DARK};
        color: {PRIMARY_TEXT};
        border: {BORDER_WIDTH}px solid {BORDER_COLOR};
        border-radius: {INPUT_RADIUS}px;
        padding: {SPACING_SM}px;
    }}

    QListWidget::item {{
        padding: {SPACING_SM}px;
        border-radius: {SMALL_RADIUS}px;
        margin: 1px 0px;
    }}

    QListWidget::item:selected {{
        background-color: {ACCENT_PRIMARY};
        color: {PRIMARY_TEXT};
    }}

    QListWidget::item:hover {{
        background-color: {BG_SURFACE};
    }}

    QTableWidget {{
        background-color: {BG_DARK};
        color: {PRIMARY_TEXT};
        gridline-color: {BORDER_COLOR};
        border: {BORDER_WIDTH}px solid {BORDER_COLOR};
        border-radius: {CARD_RADIUS}px;
        alternate-background-color: {BG_SURFACE};
    }}

    QTableWidget::item {{
        padding: {SPACING_MD}px {SPACING_SM}px;
        border: none;
    }}

    QTableWidget::item:selected {{
        background-color: {ACCENT_PRIMARY};
        color: {PRIMARY_TEXT};
    }}

    QTableWidget::item:hover {{
        background-color: {BG_SURFACE};
    }}

    QHeaderView::section {{
        background-color: {BG_DARKER};
        color: {PRIMARY_TEXT};
        padding: {SPACING_MD}px;
        border: none;
        border-right: {BORDER_WIDTH}px solid {BORDER_COLOR};
        font-weight: bold;
        font-size: {SMALL_FONT}pt;
    }}

    QProgressBar {{
        background-color: {BG_DARK};
        border: {BORDER_WIDTH}px solid {BORDER_COLOR};
        border-radius: {SMALL_RADIUS}px;
        text-align: center;
        color: {PRIMARY_TEXT};
        font-size: {SMALL_FONT}pt;
    }}

    QProgressBar::chunk {{
        background-color: {ACCENT_SUCCESS};
        border-radius: {SMALL_RADIUS}px;
    }}

    QDialog {{
        background-color: {BG_DARKER};
        border-radius: {CARD_RADIUS}px;
    }}

    QMessageBox {{
        background-color: {BG_DARKER};
    }}

    QMessageBox QLabel {{
        color: {PRIMARY_TEXT};
    }}
    """


def get_color(color_name: str) -> str:
    """Get color by semantic name."""
    colors = {
        "primary_text": PRIMARY_TEXT,
        "secondary_text": SECONDARY_TEXT,
        "muted_text": MUTED_TEXT,
        "bg_dark": BG_DARK,
        "bg_darker": BG_DARKER,
        "bg_surface": BG_SURFACE,
        "accent_primary": ACCENT_PRIMARY,
        "accent_success": ACCENT_SUCCESS,
        "accent_warning": ACCENT_WARNING,
        "accent_error": ACCENT_ERROR,
        "border": BORDER_COLOR,
    }
    return colors.get(color_name.lower(), PRIMARY_TEXT)
