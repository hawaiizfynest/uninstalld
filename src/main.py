"""
Uninstall'd - Deep Program Removal Tool for Windows
"""

import sys
import os
import base64
import tempfile as _tempfile

# Try to import embedded icon data (co-located module)
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from icon_data import ICON_B64 as _ICON_B64
    _icon_tmp = _tempfile.NamedTemporaryFile(suffix=".ico", delete=False)
    _icon_tmp.write(base64.b64decode(_ICON_B64))
    _icon_tmp.close()
    _ICON_PATH = _icon_tmp.name
except Exception:
    _ICON_PATH = None

import winreg
import shutil
import threading
import tempfile
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem,
    QProgressBar, QFrame, QSplitter, QCheckBox, QMessageBox,
    QScrollArea, QGraphicsDropShadowEffect, QStatusBar, QTabWidget,
    QTextEdit, QGroupBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import (
    QColor, QFont, QPalette, QPixmap, QIcon, QPainter, QBrush,
    QLinearGradient, QFontDatabase, QPen
)


# ─── Theme ────────────────────────────────────────────────────────────────────
COLORS = {
    "bg":           "#0D0D0F",
    "surface":      "#141418",
    "surface2":     "#1C1C22",
    "border":       "#2A2A35",
    "accent":       "#FF3B5C",
    "accent2":      "#FF6B35",
    "success":      "#00E5A0",
    "warning":      "#FFB800",
    "text":         "#F0F0F5",
    "text_dim":     "#8888AA",
    "text_muted":   "#555566",
    "scan_reg":     "#A855F7",
    "scan_file":    "#3B82F6",
    "scan_temp":    "#F59E0B",
}

STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS['bg']};
}}
QWidget {{
    background-color: transparent;
    color: {COLORS['text']};
    font-family: 'Consolas', 'Courier New', monospace;
}}
QLabel {{
    color: {COLORS['text']};
}}
QLineEdit {{
    background-color: {COLORS['surface2']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 10px 14px;
    color: {COLORS['text']};
    font-size: 14px;
    font-family: 'Consolas', monospace;
}}
QLineEdit:focus {{
    border: 1px solid {COLORS['accent']};
}}
QPushButton {{
    background-color: {COLORS['surface2']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 10px 20px;
    color: {COLORS['text']};
    font-size: 13px;
    font-weight: bold;
}}
QPushButton:hover {{
    background-color: {COLORS['surface']};
    border-color: {COLORS['accent']};
    color: {COLORS['accent']};
}}
QPushButton:pressed {{
    background-color: {COLORS['accent']};
    color: white;
}}
QPushButton:disabled {{
    color: {COLORS['text_muted']};
    border-color: {COLORS['text_muted']};
}}
QPushButton#danger {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
    color: white;
}}
QPushButton#danger:hover {{
    background-color: #CC2040;
    border-color: #CC2040;
    color: white;
}}
QPushButton#scan {{
    background-color: {COLORS['accent']};
    border: none;
    color: white;
    font-size: 14px;
    letter-spacing: 1px;
    padding: 12px 32px;
}}
QPushButton#scan:hover {{
    background-color: #FF5570;
    color: white;
}}
QPushButton#scan:disabled {{
    background-color: {COLORS['surface2']};
    color: {COLORS['text_muted']};
}}
QTreeWidget {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    alternate-background-color: {COLORS['surface2']};
    color: {COLORS['text']};
    font-size: 12px;
    outline: none;
}}
QTreeWidget::item {{
    padding: 4px 8px;
    border-bottom: 1px solid {COLORS['bg']};
}}
QTreeWidget::item:selected {{
    background-color: {COLORS['surface2']};
    color: {COLORS['accent']};
}}
QTreeWidget::item:hover {{
    background-color: {COLORS['surface2']};
}}
QHeaderView::section {{
    background-color: {COLORS['surface2']};
    color: {COLORS['text_dim']};
    border: none;
    border-bottom: 1px solid {COLORS['border']};
    padding: 8px 12px;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}
QProgressBar {{
    background-color: {COLORS['surface2']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    height: 6px;
    text-align: center;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['accent']}, stop:1 {COLORS['accent2']});
    border-radius: 4px;
}}
QCheckBox {{
    color: {COLORS['text_dim']};
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1px solid {COLORS['border']};
    border-radius: 3px;
    background: {COLORS['surface2']};
}}
QCheckBox::indicator:checked {{
    background: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}
QScrollBar:vertical {{
    background: {COLORS['surface']};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {COLORS['border']};
    border-radius: 3px;
    min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{
    background: {COLORS['accent']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QTextEdit {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    color: {COLORS['text_dim']};
    font-size: 11px;
    font-family: 'Consolas', monospace;
    padding: 8px;
}}
QStatusBar {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_muted']};
    border-top: 1px solid {COLORS['border']};
    font-size: 11px;
}}
QSplitter::handle {{
    background-color: {COLORS['border']};
}}
"""


# ─── Scanner Thread ───────────────────────────────────────────────────────────
class ScanWorker(QThread):
    progress = pyqtSignal(int, str)
    found_registry = pyqtSignal(str, str, str)   # hive, key_path, value
    found_file = pyqtSignal(str, str)             # path, size
    found_temp = pyqtSignal(str, str)             # path, size
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    REGISTRY_HIVES = [
        (winreg.HKEY_LOCAL_MACHINE, "HKLM"),
        (winreg.HKEY_CURRENT_USER,  "HKCU"),
        (winreg.HKEY_USERS,         "HKU"),
        (winreg.HKEY_CLASSES_ROOT,  "HKCR"),
    ]

    UNINSTALL_PATHS = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
    ]

    APP_PATHS = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths",
    ]

    def __init__(self, query: str):
        super().__init__()
        self.query = query.lower().strip()
        self._cancel = False
        self.results = {
            "registry": [],
            "files": [],
            "temp": [],
        }

    def cancel(self):
        self._cancel = True

    def _fmt_size(self, path: str) -> str:
        try:
            p = Path(path)
            if p.is_file():
                size = p.stat().st_size
            elif p.is_dir():
                size = sum(f.stat().st_size for f in p.rglob('*') if f.is_file())
            else:
                return "?"
            if size < 1024:
                return f"{size} B"
            elif size < 1024**2:
                return f"{size/1024:.1f} KB"
            elif size < 1024**3:
                return f"{size/1024**2:.1f} MB"
            else:
                return f"{size/1024**3:.2f} GB"
        except Exception:
            return "?"

    def _matches(self, text: str) -> bool:
        return self.query in text.lower()

    def _scan_registry_key(self, hive, hive_name: str, subkey: str):
        """Recursively scan a registry key for matches."""
        try:
            key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ)
        except OSError:
            return

        try:
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    full_path = f"{subkey}\\{subkey_name}"
                    if self._matches(subkey_name):
                        self.found_registry.emit(hive_name, full_path, "Key")
                        self.results["registry"].append({
                            "hive": hive_name, "path": full_path, "value": "Key"
                        })
                    self._scan_registry_key(hive, hive_name, full_path)
                    i += 1
                except OSError:
                    break

            # Check values
            j = 0
            while True:
                try:
                    name, data, _ = winreg.EnumValue(key, j)
                    data_str = str(data) if data else ""
                    if self._matches(name) or self._matches(data_str):
                        display = f"{name} = {data_str[:80]}"
                        self.found_registry.emit(hive_name, subkey, display)
                        self.results["registry"].append({
                            "hive": hive_name, "path": subkey, "value": display
                        })
                    j += 1
                except OSError:
                    break
        finally:
            winreg.CloseKey(key)

    def _scan_uninstall_entries(self):
        """Check uninstall registry entries specifically."""
        for hive, hive_name in self.REGISTRY_HIVES:
            for upath in self.UNINSTALL_PATHS:
                try:
                    key = winreg.OpenKey(hive, upath, 0, winreg.KEY_READ)
                    i = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            try:
                                sub = winreg.OpenKey(key, subkey_name, 0, winreg.KEY_READ)
                                try:
                                    display_name, _ = winreg.QueryValueEx(sub, "DisplayName")
                                except Exception:
                                    display_name = subkey_name

                                if self._matches(display_name) or self._matches(subkey_name):
                                    full_path = f"{upath}\\{subkey_name}"
                                    self.found_registry.emit(
                                        hive_name, full_path,
                                        f"Uninstall Entry: {display_name}"
                                    )
                                    self.results["registry"].append({
                                        "hive": hive_name,
                                        "path": full_path,
                                        "value": f"Uninstall Entry: {display_name}"
                                    })

                                    # Also grab InstallLocation and UninstallString
                                    for val_name in ["InstallLocation", "UninstallString", "DisplayIcon"]:
                                        try:
                                            val, _ = winreg.QueryValueEx(sub, val_name)
                                            if val:
                                                self.found_registry.emit(
                                                    hive_name, full_path, f"{val_name}: {str(val)[:80]}"
                                                )
                                                self.results["registry"].append({
                                                    "hive": hive_name, "path": full_path,
                                                    "value": f"{val_name}: {str(val)[:80]}"
                                                })
                                                # If it's a file/folder, add to files
                                                clean_path = str(val).strip('"').split('"')[0]
                                                if val_name == "InstallLocation" and clean_path and Path(clean_path).exists():
                                                    size = self._fmt_size(clean_path)
                                                    self.found_file.emit(clean_path, size)
                                                    self.results["files"].append({
                                                        "path": clean_path, "size": size, "source": "InstallLocation"
                                                    })
                                        except Exception:
                                            pass
                                winreg.CloseKey(sub)
                            except Exception:
                                pass
                            i += 1
                        except OSError:
                            break
                    winreg.CloseKey(key)
                except OSError:
                    pass
                if self._cancel:
                    return

    def _scan_common_file_locations(self):
        """Search common install directories."""
        search_dirs = [
            os.environ.get("ProgramFiles", r"C:\Program Files"),
            os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
            os.environ.get("LOCALAPPDATA", ""),
            os.environ.get("APPDATA", ""),
            os.environ.get("ProgramData", r"C:\ProgramData"),
        ]
        for base in search_dirs:
            if not base or not Path(base).exists():
                continue
            try:
                for entry in Path(base).iterdir():
                    if self._cancel:
                        return
                    if self._matches(entry.name):
                        size = self._fmt_size(str(entry))
                        self.found_file.emit(str(entry), size)
                        self.results["files"].append({
                            "path": str(entry), "size": size, "source": "Program Files"
                        })
            except PermissionError:
                pass

    def _scan_temp(self):
        """Scan %TEMP% for anything matching the query."""
        temp_dir = os.environ.get("TEMP") or tempfile.gettempdir()
        if not temp_dir or not Path(temp_dir).exists():
            return
        try:
            for entry in Path(temp_dir).rglob("*"):
                if self._cancel:
                    return
                if self._matches(entry.name):
                    size = self._fmt_size(str(entry))
                    self.found_temp.emit(str(entry), size)
                    self.results["temp"].append({"path": str(entry), "size": size})
        except Exception:
            pass

    def run(self):
        try:
            self.progress.emit(5, "Scanning Uninstall registry entries...")
            self._scan_uninstall_entries()
            if self._cancel:
                return

            self.progress.emit(30, "Scanning HKLM registry...")
            self._scan_registry_key(
                winreg.HKEY_LOCAL_MACHINE, "HKLM",
                r"SOFTWARE\Microsoft\Windows\CurrentVersion"
            )
            if self._cancel:
                return

            self.progress.emit(50, "Scanning HKCU registry...")
            self._scan_registry_key(
                winreg.HKEY_CURRENT_USER, "HKCU",
                r"SOFTWARE"
            )
            if self._cancel:
                return

            self.progress.emit(65, "Scanning program file locations...")
            self._scan_common_file_locations()
            if self._cancel:
                return

            self.progress.emit(85, "Scanning %TEMP% folder...")
            self._scan_temp()
            if self._cancel:
                return

            self.progress.emit(100, "Scan complete.")
            self.finished.emit(self.results)

        except Exception as e:
            self.error.emit(str(e))


# ─── Delete Worker ────────────────────────────────────────────────────────────
class DeleteWorker(QThread):
    progress = pyqtSignal(int, str)
    item_done = pyqtSignal(str, bool, str)  # path, success, error_msg
    finished = pyqtSignal(int, int)         # success_count, fail_count

    def __init__(self, items):
        super().__init__()
        self.items = items  # list of dicts with 'type' ('file'/'registry') and 'data'

    def run(self):
        total = len(self.items)
        success = 0
        fail = 0
        for i, item in enumerate(self.items):
            pct = int((i / total) * 100)
            if item["type"] == "file":
                path = item["path"]
                self.progress.emit(pct, f"Deleting: {path}")
                try:
                    p = Path(path)
                    if p.is_dir():
                        shutil.rmtree(path, ignore_errors=False)
                    elif p.is_file():
                        p.unlink()
                    self.item_done.emit(path, True, "")
                    success += 1
                except Exception as e:
                    self.item_done.emit(path, False, str(e))
                    fail += 1
            elif item["type"] == "registry":
                hive_map = {
                    "HKLM": winreg.HKEY_LOCAL_MACHINE,
                    "HKCU": winreg.HKEY_CURRENT_USER,
                    "HKCR": winreg.HKEY_CLASSES_ROOT,
                    "HKU":  winreg.HKEY_USERS,
                }
                hive_name = item.get("hive", "HKLM")
                key_path = item.get("path", "")
                self.progress.emit(pct, f"Removing registry key: {hive_name}\\{key_path}")
                try:
                    hive = hive_map.get(hive_name, winreg.HKEY_LOCAL_MACHINE)
                    winreg.DeleteKey(hive, key_path)
                    self.item_done.emit(f"{hive_name}\\{key_path}", True, "")
                    success += 1
                except Exception as e:
                    self.item_done.emit(f"{hive_name}\\{key_path}", False, str(e))
                    fail += 1

        self.finished.emit(success, fail)


# ─── Main Window ──────────────────────────────────────────────────────────────
class UninstalldWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scan_worker = None
        self.delete_worker = None
        self.scan_results = {}
        self.setWindowTitle("Uninstall'd")
        self.setMinimumSize(1100, 720)
        self.resize(1200, 780)
        self.setStyleSheet(STYLESHEET)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        central.setStyleSheet(f"background-color: {COLORS['bg']};")
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        root.addWidget(self._build_header())

        # Search bar
        root.addWidget(self._build_search_bar())

        # Progress
        self.progress_frame = self._build_progress()
        self.progress_frame.setVisible(False)
        root.addWidget(self.progress_frame)

        # Results
        root.addWidget(self._build_results(), 1)

        # Action bar
        root.addWidget(self._build_action_bar())

        # Status bar
        self.status = QStatusBar()
        self.status.setFixedHeight(28)
        self.setStatusBar(self.status)
        self._set_status("Ready — enter a program name and click SCAN")

    def _build_header(self):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border-bottom: 1px solid {COLORS['border']};
            }}
        """)
        frame.setFixedHeight(72)
        h = QHBoxLayout(frame)
        h.setContentsMargins(28, 0, 28, 0)

        # Logo mark
        logo_label = QLabel("⌫")
        logo_label.setStyleSheet(f"""
            font-size: 28px;
            color: {COLORS['accent']};
            background: transparent;
            font-weight: bold;
        """)

        title = QLabel("UNINSTALL'D")
        title.setStyleSheet(f"""
            font-size: 22px;
            font-weight: bold;
            color: {COLORS['text']};
            letter-spacing: 4px;
            background: transparent;
        """)

        tagline = QLabel("Deep Program Removal for Windows")
        tagline.setStyleSheet(f"""
            font-size: 12px;
            color: {COLORS['text_muted']};
            letter-spacing: 1px;
            background: transparent;
        """)

        ver = QLabel("v1.0")
        ver.setStyleSheet(f"""
            font-size: 11px;
            color: {COLORS['text_muted']};
            background: transparent;
        """)
        ver.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        h.addWidget(logo_label)
        h.addSpacing(12)
        h.addWidget(title)
        h.addSpacing(16)

        vl = QVBoxLayout()
        vl.addStretch()
        vl.addWidget(tagline)
        vl.addStretch()
        h.addLayout(vl)
        h.addStretch()
        h.addWidget(ver)
        return frame

    def _build_search_bar(self):
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {COLORS['bg']}; border: none;")
        frame.setFixedHeight(70)
        h = QHBoxLayout(frame)
        h.setContentsMargins(28, 12, 28, 12)
        h.setSpacing(12)

        lbl = QLabel("PROGRAM NAME")
        lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; letter-spacing: 2px;")
        lbl.setFixedWidth(120)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("e.g.  Discord,  Spotify,  Adobe Photoshop...")
        self.search_input.returnPressed.connect(self._start_scan)

        self.scan_btn = QPushButton("▶  SCAN")
        self.scan_btn.setObjectName("scan")
        self.scan_btn.setFixedWidth(140)
        self.scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.scan_btn.clicked.connect(self._start_scan)

        self.cancel_btn = QPushButton("CANCEL")
        self.cancel_btn.setFixedWidth(100)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self._cancel_scan)

        h.addWidget(lbl)
        h.addWidget(self.search_input, 1)
        h.addWidget(self.scan_btn)
        h.addWidget(self.cancel_btn)
        return frame

    def _build_progress(self):
        frame = QFrame()
        frame.setStyleSheet(f"background: {COLORS['bg']}; border: none;")
        frame.setFixedHeight(44)
        h = QHBoxLayout(frame)
        h.setContentsMargins(28, 4, 28, 4)
        h.setSpacing(14)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setRange(0, 100)

        self.progress_label = QLabel("Scanning...")
        self.progress_label.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 12px;")
        self.progress_label.setFixedWidth(300)

        h.addWidget(self.progress_bar, 1)
        h.addWidget(self.progress_label)
        return frame

    def _build_results(self):
        frame = QFrame()
        frame.setStyleSheet(f"background: {COLORS['bg']}; border: none;")
        outer = QVBoxLayout(frame)
        outer.setContentsMargins(28, 8, 28, 8)
        outer.setSpacing(0)

        # Stats row
        stats_row = QHBoxLayout()
        self.stat_reg = self._stat_badge("Registry Keys", "0", COLORS['scan_reg'])
        self.stat_files = self._stat_badge("Files / Folders", "0", COLORS['scan_file'])
        self.stat_temp = self._stat_badge("Temp Files", "0", COLORS['scan_temp'])
        stats_row.addWidget(self.stat_reg[0])
        stats_row.addSpacing(12)
        stats_row.addWidget(self.stat_files[0])
        stats_row.addSpacing(12)
        stats_row.addWidget(self.stat_temp[0])
        stats_row.addStretch()
        outer.addLayout(stats_row)
        outer.addSpacing(12)

        # Splitter with two panes
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(1)

        # Left: registry + files tree
        left_panel = QWidget()
        left_panel.setStyleSheet("background: transparent;")
        lv = QVBoxLayout(left_panel)
        lv.setContentsMargins(0, 0, 6, 0)
        lv.setSpacing(8)

        reg_lbl = QLabel("◆  REGISTRY ENTRIES")
        reg_lbl.setStyleSheet(f"color: {COLORS['scan_reg']}; font-size: 11px; letter-spacing: 2px;")
        lv.addWidget(reg_lbl)

        self.reg_tree = QTreeWidget()
        self.reg_tree.setHeaderLabels(["Hive", "Key Path", "Value / Detail"])
        self.reg_tree.setColumnWidth(0, 60)
        self.reg_tree.setColumnWidth(1, 260)
        self.reg_tree.setAlternatingRowColors(True)
        self.reg_tree.setSelectionMode(QTreeWidget.SelectionMode.MultiSelection)
        lv.addWidget(self.reg_tree, 1)

        files_lbl = QLabel("◆  FILES & FOLDERS")
        files_lbl.setStyleSheet(f"color: {COLORS['scan_file']}; font-size: 11px; letter-spacing: 2px;")
        lv.addWidget(files_lbl)

        self.files_tree = QTreeWidget()
        self.files_tree.setHeaderLabels(["Path", "Size", "Source"])
        self.files_tree.setColumnWidth(0, 280)
        self.files_tree.setColumnWidth(1, 70)
        self.files_tree.setAlternatingRowColors(True)
        self.files_tree.setSelectionMode(QTreeWidget.SelectionMode.MultiSelection)
        lv.addWidget(self.files_tree, 1)

        # Right: temp + log
        right_panel = QWidget()
        right_panel.setStyleSheet("background: transparent;")
        rv = QVBoxLayout(right_panel)
        rv.setContentsMargins(6, 0, 0, 0)
        rv.setSpacing(8)

        temp_lbl = QLabel("◆  TEMP FILES")
        temp_lbl.setStyleSheet(f"color: {COLORS['scan_temp']}; font-size: 11px; letter-spacing: 2px;")
        rv.addWidget(temp_lbl)

        self.temp_tree = QTreeWidget()
        self.temp_tree.setHeaderLabels(["Path", "Size"])
        self.temp_tree.setColumnWidth(0, 300)
        self.temp_tree.setAlternatingRowColors(True)
        self.temp_tree.setSelectionMode(QTreeWidget.SelectionMode.MultiSelection)
        rv.addWidget(self.temp_tree, 1)

        log_lbl = QLabel("◆  SCAN LOG")
        log_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; letter-spacing: 2px;")
        rv.addWidget(log_lbl)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(160)
        rv.addWidget(self.log_text)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([620, 380])
        outer.addWidget(splitter, 1)
        return frame

    def _stat_badge(self, label: str, count: str, color: str):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
            }}
        """)
        frame.setFixedHeight(52)
        frame.setFixedWidth(180)
        h = QHBoxLayout(frame)
        h.setContentsMargins(14, 8, 14, 8)

        count_lbl = QLabel(count)
        count_lbl.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {color}; background: transparent;")
        h.addWidget(count_lbl)
        h.addSpacing(8)

        name_lbl = QLabel(label)
        name_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent;")
        h.addWidget(name_lbl)
        h.addStretch()

        return frame, count_lbl

    def _build_action_bar(self):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border-top: 1px solid {COLORS['border']};
            }}
        """)
        frame.setFixedHeight(64)
        h = QHBoxLayout(frame)
        h.setContentsMargins(28, 0, 28, 0)
        h.setSpacing(12)

        self.chk_reg = QCheckBox("Delete Registry Entries")
        self.chk_files = QCheckBox("Delete Files & Folders")
        self.chk_temp = QCheckBox("Delete Temp Files")
        for chk in [self.chk_reg, self.chk_files, self.chk_temp]:
            chk.setChecked(True)
            chk.setEnabled(False)

        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.setEnabled(False)
        self.select_all_btn.clicked.connect(self._select_all)

        self.delete_btn = QPushButton("🗑  DELETE SELECTED")
        self.delete_btn.setObjectName("danger")
        self.delete_btn.setFixedWidth(200)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.clicked.connect(self._confirm_delete)

        h.addWidget(self.chk_reg)
        h.addWidget(self.chk_files)
        h.addWidget(self.chk_temp)
        h.addStretch()
        h.addWidget(self.select_all_btn)
        h.addWidget(self.delete_btn)
        return frame

    # ─── Scan logic ───────────────────────────────────────────────────────────
    def _start_scan(self):
        query = self.search_input.text().strip()
        if not query:
            self._set_status("Please enter a program name first.")
            return

        self._clear_results()
        self.scan_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.delete_btn.setEnabled(False)
        self.select_all_btn.setEnabled(False)
        self.progress_frame.setVisible(True)
        self.progress_bar.setValue(0)

        self.scan_worker = ScanWorker(query)
        self.scan_worker.progress.connect(self._on_progress)
        self.scan_worker.found_registry.connect(self._on_registry)
        self.scan_worker.found_file.connect(self._on_file)
        self.scan_worker.found_temp.connect(self._on_temp)
        self.scan_worker.finished.connect(self._on_finished)
        self.scan_worker.error.connect(self._on_error)
        self.scan_worker.start()

    def _cancel_scan(self):
        if self.scan_worker:
            self.scan_worker.cancel()
        self._set_status("Scan cancelled.")
        self.scan_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)

    def _clear_results(self):
        self.reg_tree.clear()
        self.files_tree.clear()
        self.temp_tree.clear()
        self.log_text.clear()
        self.scan_results = {}
        self.stat_reg[1].setText("0")
        self.stat_files[1].setText("0")
        self.stat_temp[1].setText("0")

    def _on_progress(self, pct, msg):
        self.progress_bar.setValue(pct)
        self.progress_label.setText(msg)
        self._log(msg)

    def _on_registry(self, hive, path, value):
        item = QTreeWidgetItem([hive, path, value])
        item.setForeground(0, QColor(COLORS['scan_reg']))
        item.setCheckState(0, Qt.CheckState.Checked)
        self.reg_tree.addTopLevelItem(item)
        count = self.reg_tree.topLevelItemCount()
        self.stat_reg[1].setText(str(count))

    def _on_file(self, path, size):
        source = "Scan"
        item = QTreeWidgetItem([path, size, source])
        item.setForeground(0, QColor(COLORS['scan_file']))
        item.setCheckState(0, Qt.CheckState.Checked)
        self.files_tree.addTopLevelItem(item)
        count = self.files_tree.topLevelItemCount()
        self.stat_files[1].setText(str(count))

    def _on_temp(self, path, size):
        item = QTreeWidgetItem([path, size])
        item.setForeground(0, QColor(COLORS['scan_temp']))
        item.setCheckState(0, Qt.CheckState.Checked)
        self.temp_tree.addTopLevelItem(item)
        count = self.temp_tree.topLevelItemCount()
        self.stat_temp[1].setText(str(count))

    def _on_finished(self, results):
        self.scan_results = results
        self.progress_frame.setVisible(False)
        self.scan_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)

        total = (self.reg_tree.topLevelItemCount() +
                 self.files_tree.topLevelItemCount() +
                 self.temp_tree.topLevelItemCount())

        if total > 0:
            self.delete_btn.setEnabled(True)
            self.select_all_btn.setEnabled(True)
            for chk in [self.chk_reg, self.chk_files, self.chk_temp]:
                chk.setEnabled(True)
            self._set_status(
                f"Scan complete — found {self.reg_tree.topLevelItemCount()} registry entries, "
                f"{self.files_tree.topLevelItemCount()} files/folders, "
                f"{self.temp_tree.topLevelItemCount()} temp items."
            )
        else:
            self._set_status(f"No traces found for '{self.search_input.text()}'. Program may already be removed.")

        self._log(f"Scan finished. {total} items found total.")

    def _on_error(self, msg):
        self._log(f"ERROR: {msg}")
        self._set_status(f"Scan error: {msg}")
        self.scan_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_frame.setVisible(False)

    # ─── Delete logic ─────────────────────────────────────────────────────────
    def _select_all(self):
        for tree in [self.reg_tree, self.files_tree, self.temp_tree]:
            for i in range(tree.topLevelItemCount()):
                tree.topLevelItem(i).setCheckState(0, Qt.CheckState.Checked)

    def _gather_selected(self):
        items = []
        if self.chk_reg.isChecked():
            for i in range(self.reg_tree.topLevelItemCount()):
                it = self.reg_tree.topLevelItem(i)
                if it.checkState(0) == Qt.CheckState.Checked:
                    items.append({
                        "type": "registry",
                        "hive": it.text(0),
                        "path": it.text(1),
                    })
        if self.chk_files.isChecked():
            for i in range(self.files_tree.topLevelItemCount()):
                it = self.files_tree.topLevelItem(i)
                if it.checkState(0) == Qt.CheckState.Checked:
                    items.append({"type": "file", "path": it.text(0)})
        if self.chk_temp.isChecked():
            for i in range(self.temp_tree.topLevelItemCount()):
                it = self.temp_tree.topLevelItem(i)
                if it.checkState(0) == Qt.CheckState.Checked:
                    items.append({"type": "file", "path": it.text(0)})
        return items

    def _confirm_delete(self):
        items = self._gather_selected()
        if not items:
            self._set_status("No items selected for deletion.")
            return

        msg = QMessageBox(self)
        msg.setWindowTitle("Confirm Deletion")
        msg.setText(
            f"<b style='color:#FF3B5C;'>You are about to permanently delete {len(items)} items.</b><br><br>"
            "This action <b>cannot be undone</b>. Registry entries and files will be removed.<br><br>"
            "Are you sure you want to continue?"
        )
        msg.setStyleSheet(f"""
            QMessageBox {{ background-color: {COLORS['surface']}; color: {COLORS['text']}; }}
            QPushButton {{ min-width: 100px; }}
        """)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        )
        msg.setDefaultButton(QMessageBox.StandardButton.Cancel)
        if msg.exec() != QMessageBox.StandardButton.Yes:
            return

        self._start_delete(items)

    def _start_delete(self, items):
        self.delete_btn.setEnabled(False)
        self.scan_btn.setEnabled(False)
        self.progress_frame.setVisible(True)
        self.progress_bar.setValue(0)

        self.delete_worker = DeleteWorker(items)
        self.delete_worker.progress.connect(self._on_progress)
        self.delete_worker.item_done.connect(self._on_item_deleted)
        self.delete_worker.finished.connect(self._on_delete_finished)
        self.delete_worker.start()

    def _on_item_deleted(self, path, success, err):
        icon = "✓" if success else "✗"
        color = COLORS['success'] if success else COLORS['accent']
        self._log(f'<span style="color:{color}">{icon} {path}{" — " + err if err else ""}</span>')

    def _on_delete_finished(self, success, fail):
        self.progress_frame.setVisible(False)
        self.scan_btn.setEnabled(True)
        self._set_status(f"Deletion complete — {success} succeeded, {fail} failed.")
        self._log(f"Done. {success} removed, {fail} failed.")
        self._clear_results()

    # ─── Helpers ──────────────────────────────────────────────────────────────
    def _set_status(self, msg: str):
        self.status.showMessage(f"  {msg}")

    def _log(self, msg: str):
        self.log_text.append(msg)


# ─── Entry Point ──────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Uninstall'd")
    app.setApplicationVersion("1.0")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(COLORS['bg']))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(COLORS['text']))
    app.setPalette(palette)

    # Set application icon from embedded data
    if _ICON_PATH and os.path.exists(_ICON_PATH):
        app_icon = QIcon(_ICON_PATH)
        app.setWindowIcon(app_icon)

    win = UninstalldWindow()
    if _ICON_PATH and os.path.exists(_ICON_PATH):
        win.setWindowIcon(QIcon(_ICON_PATH))
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
