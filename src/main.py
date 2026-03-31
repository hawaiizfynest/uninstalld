"""
Uninstall'd v1.1 - Deep Program Removal Tool for Windows
"""

import sys, os, base64, datetime, re, subprocess, shutil, tempfile, winreg, string
import tempfile as _tempfile
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem,
    QProgressBar, QFrame, QSplitter, QCheckBox, QMessageBox,
    QStatusBar, QTextEdit, QDialog, QComboBox, QFileDialog,
    QListWidget, QListWidgetItem, QGroupBox,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QPalette, QIcon

try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from icon_data import ICON_B64 as _ICON_B64
    _icon_tmp = _tempfile.NamedTemporaryFile(suffix=".ico", delete=False)
    _icon_tmp.write(base64.b64decode(_ICON_B64))
    _icon_tmp.close()
    _ICON_PATH = _icon_tmp.name
except Exception:
    _ICON_PATH = None

COLORS = {
    "bg": "#0D0D0F", "surface": "#141418", "surface2": "#1C1C22",
    "border": "#2A2A35", "accent": "#FF3B5C", "accent2": "#FF6B35",
    "success": "#00E5A0", "warning": "#FFB800", "move": "#3B82F6",
    "text": "#F0F0F5", "text_dim": "#8888AA", "text_muted": "#555566",
    "scan_reg": "#A855F7", "scan_file": "#3B82F6", "scan_temp": "#F59E0B",
}

SS = f"""
QMainWindow {{ background-color: {COLORS["bg"]}; }}
QWidget {{ background-color: transparent; color: {COLORS["text"]}; font-family: Consolas, Courier New, monospace; }}
QLabel {{ color: {COLORS["text"]}; }}
QLineEdit {{ background-color: {COLORS["surface2"]}; border: 1px solid {COLORS["border"]}; border-radius: 6px; padding: 10px 14px; color: {COLORS["text"]}; font-size: 14px; }}
QLineEdit:focus {{ border: 1px solid {COLORS["accent"]}; }}
QComboBox {{ background-color: {COLORS["surface2"]}; border: 1px solid {COLORS["border"]}; border-radius: 6px; padding: 8px 12px; color: {COLORS["text"]}; font-size: 13px; }}
QComboBox::drop-down {{ border: none; width: 24px; }}
QComboBox QAbstractItemView {{ background-color: {COLORS["surface2"]}; color: {COLORS["text"]}; border: 1px solid {COLORS["border"]}; selection-background-color: {COLORS["accent"]}; }}
QPushButton {{ background-color: {COLORS["surface2"]}; border: 1px solid {COLORS["border"]}; border-radius: 6px; padding: 10px 20px; color: {COLORS["text"]}; font-size: 13px; font-weight: bold; }}
QPushButton:hover {{ background-color: {COLORS["surface"]}; border-color: {COLORS["accent"]}; color: {COLORS["accent"]}; }}
QPushButton:pressed {{ background-color: {COLORS["accent"]}; color: white; }}
QPushButton:disabled {{ color: {COLORS["text_muted"]}; border-color: {COLORS["text_muted"]}; }}
QPushButton#danger {{ background-color: {COLORS["accent"]}; border-color: {COLORS["accent"]}; color: white; }}
QPushButton#danger:hover {{ background-color: #CC2040; border-color: #CC2040; }}
QPushButton#scan {{ background-color: {COLORS["accent"]}; border: none; color: white; font-size: 14px; letter-spacing: 1px; padding: 12px 32px; }}
QPushButton#scan:hover {{ background-color: #FF5570; }}
QPushButton#scan:disabled {{ background-color: {COLORS["surface2"]}; color: {COLORS["text_muted"]}; }}
QPushButton#move {{ background-color: {COLORS["move"]}; border-color: {COLORS["move"]}; color: white; }}
QPushButton#move:hover {{ background-color: #2563EB; }}
QPushButton#restore {{ background-color: {COLORS["warning"]}; border-color: {COLORS["warning"]}; color: #0D0D0F; }}
QPushButton#restore:hover {{ background-color: #D97706; }}
QTreeWidget {{ background-color: {COLORS["surface"]}; border: 1px solid {COLORS["border"]}; border-radius: 8px; alternate-background-color: {COLORS["surface2"]}; color: {COLORS["text"]}; font-size: 12px; outline: none; }}
QTreeWidget::item {{ padding: 4px 8px; border-bottom: 1px solid {COLORS["bg"]}; }}
QTreeWidget::item:selected {{ background-color: {COLORS["surface2"]}; color: {COLORS["accent"]}; }}
QTreeWidget::item:hover {{ background-color: {COLORS["surface2"]}; }}
QListWidget {{ background-color: {COLORS["surface"]}; border: 1px solid {COLORS["border"]}; border-radius: 6px; color: {COLORS["text"]}; font-size: 12px; outline: none; }}
QListWidget::item {{ padding: 6px 10px; border-bottom: 1px solid {COLORS["bg"]}; }}
QListWidget::item:selected {{ background-color: {COLORS["surface2"]}; color: {COLORS["warning"]}; }}
QHeaderView::section {{ background-color: {COLORS["surface2"]}; color: {COLORS["text_dim"]}; border: none; border-bottom: 1px solid {COLORS["border"]}; padding: 8px 12px; font-size: 11px; letter-spacing: 1px; }}
QProgressBar {{ background-color: {COLORS["surface2"]}; border: 1px solid {COLORS["border"]}; border-radius: 4px; height: 6px; }}
QProgressBar::chunk {{ background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 {COLORS["accent"]}, stop:1 {COLORS["accent2"]}); border-radius: 4px; }}
QCheckBox {{ color: {COLORS["text_dim"]}; spacing: 8px; }}
QCheckBox::indicator {{ width: 16px; height: 16px; border: 1px solid {COLORS["border"]}; border-radius: 3px; background: {COLORS["surface2"]}; }}
QCheckBox::indicator:checked {{ background: {COLORS["accent"]}; border-color: {COLORS["accent"]}; }}
QScrollBar:vertical {{ background: {COLORS["surface"]}; width: 6px; border-radius: 3px; }}
QScrollBar::handle:vertical {{ background: {COLORS["border"]}; border-radius: 3px; min-height: 20px; }}
QScrollBar::handle:vertical:hover {{ background: {COLORS["accent"]}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QTextEdit {{ background-color: {COLORS["surface"]}; border: 1px solid {COLORS["border"]}; border-radius: 6px; color: {COLORS["text_dim"]}; font-size: 11px; padding: 8px; }}
QStatusBar {{ background-color: {COLORS["surface"]}; color: {COLORS["text_muted"]}; border-top: 1px solid {COLORS["border"]}; font-size: 11px; }}
QSplitter::handle {{ background-color: {COLORS["border"]}; }}
QDialog {{ background-color: {COLORS["surface"]}; }}
QGroupBox {{ border: 1px solid {COLORS["border"]}; border-radius: 6px; margin-top: 12px; color: {COLORS["text_dim"]}; font-size: 11px; letter-spacing: 1px; }}
QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 6px; }}
"""

# ── Registry backup helpers ───────────────────────────────────────────────────
BACKUP_DIR = Path(os.environ.get("APPDATA", "")) / "Uninstalld" / "backups"

def ensure_backup_dir():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def backup_registry(program_name: str) -> Path:
    ensure_backup_dir()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in program_name)
    bp = BACKUP_DIR / f"backup_{safe}_{ts}.reg"
    bp2 = BACKUP_DIR / f"backup_{safe}_{ts}.hkcu.reg"
    with tempfile.NamedTemporaryFile(suffix=".reg", delete=False) as t1, \
         tempfile.NamedTemporaryFile(suffix=".reg", delete=False) as t2:
        t1n, t2n = t1.name, t2.name
    try:
        subprocess.run(["reg", "export",
            r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion", t1n, "/y"],
            check=True, capture_output=True)
        subprocess.run(["reg", "export", r"HKCU\SOFTWARE", t2n, "/y"],
            check=True, capture_output=True)
        shutil.copy(t1n, str(bp))
        shutil.copy(t2n, str(bp2))
    finally:
        for f in [t1n, t2n]:
            try: os.unlink(f)
            except: pass
    return bp

def restore_registry(reg_path: Path):
    subprocess.run(["reg", "import", str(reg_path)], check=True, capture_output=True)
    companion = reg_path.with_suffix(".hkcu.reg")
    if companion.exists():
        subprocess.run(["reg", "import", str(companion)], check=True, capture_output=True)

def list_backups():
    ensure_backup_dir()
    return sorted(
        [p for p in BACKUP_DIR.glob("backup_*.reg") if not p.name.endswith(".hkcu.reg")],
        key=lambda p: p.stat().st_mtime, reverse=True)


# ── Backup Prompt Dialog ──────────────────────────────────────────────────────
class BackupPromptDialog(QDialog):
    def __init__(self, parent, action_desc):
        super().__init__(parent)
        self.choice = "cancel"
        self.setWindowTitle("Registry Backup")
        self.setModal(True)
        self.setMinimumWidth(540)
        self.setStyleSheet(f"QDialog {{ background-color: {COLORS['surface']}; }}")
        v = QVBoxLayout(self)
        v.setContentsMargins(28, 24, 28, 20)
        v.setSpacing(14)

        row = QHBoxLayout()
        ico = QLabel("🛡")
        ico.setStyleSheet("font-size: 32px;")
        ttl = QLabel("Back up the Registry?")
        ttl.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {COLORS['text']};")
        row.addWidget(ico); row.addSpacing(10); row.addWidget(ttl); row.addStretch()
        v.addLayout(row)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {COLORS['border']};"); v.addWidget(sep)

        desc = QLabel(
            f"You are about to <b>{action_desc}</b>.<br><br>"
            "A backup lets you restore the registry to its current state if anything goes wrong.<br><br>"
            f"<span style='color:{COLORS['text_muted']};'>Backups are saved to:<br>"
            f"<code>{BACKUP_DIR}</code></span>")
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 13px; line-height: 1.5;")
        v.addWidget(desc)
        v.addSpacing(6)

        btn_row = QHBoxLayout(); btn_row.setSpacing(10)

        b_btn = QPushButton("🛡  Backup and Continue")
        b_btn.setStyleSheet(f"""QPushButton {{
            background-color: {COLORS['success']}; color: #0D0D0F;
            border: none; border-radius: 6px; padding: 12px 20px;
            font-size: 13px; font-weight: bold;
        }} QPushButton:hover {{ background-color: #00C98A; }}""")
        b_btn.clicked.connect(lambda: self._choose("backup"))

        s_btn = QPushButton("⚠  Continue Without Backup")
        s_btn.setStyleSheet(f"""QPushButton {{
            background-color: {COLORS['warning']}; color: #0D0D0F;
            border: none; border-radius: 6px; padding: 12px 20px;
            font-size: 13px; font-weight: bold;
        }} QPushButton:hover {{ background-color: #D97706; }}""")
        s_btn.clicked.connect(lambda: self._choose("skip"))

        c_btn = QPushButton("Cancel"); c_btn.clicked.connect(self.reject)

        btn_row.addWidget(b_btn); btn_row.addWidget(s_btn)
        btn_row.addStretch(); btn_row.addWidget(c_btn)
        v.addLayout(btn_row)

    def _choose(self, choice):
        self.choice = choice; self.accept()


# ── Restore Dialog ────────────────────────────────────────────────────────────
class RestoreDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Restore Registry Backup")
        self.setModal(True); self.setMinimumSize(640, 420)
        self.setStyleSheet(f"QDialog {{ background-color: {COLORS['surface']}; }}")
        v = QVBoxLayout(self)
        v.setContentsMargins(24, 20, 24, 20); v.setSpacing(12)

        ttl = QLabel("🔄  Restore Registry Backup")
        ttl.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLORS['text']};")
        v.addWidget(ttl)

        info = QLabel("Select a backup to restore. The registry file will be re-imported via reg.exe. Restart your PC after restoring.")
        info.setWordWrap(True)
        info.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 12px;")
        v.addWidget(info)

        self.lw = QListWidget()
        backups = list_backups()
        if backups:
            for bp in backups:
                ts = datetime.datetime.fromtimestamp(bp.stat().st_mtime).strftime("%Y-%m-%d  %H:%M:%S")
                sz = bp.stat().st_size // 1024
                item = QListWidgetItem(f"{bp.stem}    [{ts}]    {sz} KB")
                item.setData(Qt.ItemDataRole.UserRole, str(bp))
                self.lw.addItem(item)
            self.lw.setCurrentRow(0)
        else:
            ni = QListWidgetItem("No backups found.")
            ni.setFlags(Qt.ItemFlag.NoItemFlags); self.lw.addItem(ni)
        v.addWidget(self.lw, 1)

        browse_row = QHBoxLayout()
        self.browse_edit = QLineEdit()
        self.browse_edit.setPlaceholderText("Or browse for a .reg file manually...")
        bb = QPushButton("Browse..."); bb.setFixedWidth(100); bb.clicked.connect(self._browse)
        browse_row.addWidget(self.browse_edit, 1); browse_row.addWidget(bb)
        v.addLayout(browse_row)

        btn_row = QHBoxLayout()
        rb = QPushButton("🔄  Restore Selected"); rb.setObjectName("restore")
        rb.clicked.connect(self._do_restore)
        cb = QPushButton("Cancel"); cb.clicked.connect(self.reject)
        btn_row.addWidget(rb); btn_row.addStretch(); btn_row.addWidget(cb)
        v.addLayout(btn_row)

    def _browse(self):
        p, _ = QFileDialog.getOpenFileName(self, "Select Backup", str(BACKUP_DIR), "Registry Files (*.reg)")
        if p: self.browse_edit.setText(p)

    def _do_restore(self):
        manual = self.browse_edit.text().strip()
        if manual and Path(manual).exists():
            reg_path = Path(manual)
        else:
            item = self.lw.currentItem()
            if not item or not item.data(Qt.ItemDataRole.UserRole):
                QMessageBox.warning(self, "No Selection", "Please select a backup to restore.")
                return
            reg_path = Path(item.data(Qt.ItemDataRole.UserRole))

        c = QMessageBox(self)
        c.setWindowTitle("Confirm Restore")
        c.setText(f"<b>Restore this backup?</b><br><br><code>{reg_path.name}</code><br><br>You should restart your PC afterwards.")
        c.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        c.setDefaultButton(QMessageBox.StandardButton.Cancel)
        if c.exec() != QMessageBox.StandardButton.Yes: return

        try:
            restore_registry(reg_path)
            QMessageBox.information(self, "Restore Complete",
                "Registry backup restored.\n\nPlease restart your PC for full effect.")
            self.accept()
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Restore Failed",
                f"reg.exe error:\n{e.stderr.decode(errors='replace') if e.stderr else str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Restore Failed", str(e))


# ── Move Worker ───────────────────────────────────────────────────────────────
class MoveWorker(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)

    def __init__(self, src, dst, reg_entries):
        super().__init__()
        self.src = Path(src); self.dst = Path(dst)
        self.reg_entries = reg_entries

    def run(self):
        try:
            if not self.src.exists():
                self.finished.emit(False, f"Source not found: {self.src}"); return

            self.progress.emit(5, f"Copying {self.src} → {self.dst} ...")
            self.dst.parent.mkdir(parents=True, exist_ok=True)

            all_files = [f for f in self.src.rglob("*") if f.is_file()]
            total = len(all_files) or 1
            for i, item in enumerate(self.src.rglob("*")):
                rel = item.relative_to(self.src)
                dest = self.dst / rel
                if item.is_dir():
                    dest.mkdir(parents=True, exist_ok=True)
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(item), str(dest))
                pct = 5 + int((i / total) * 60)
                self.progress.emit(pct, f"Copying: {rel}")

            self.progress.emit(68, "Updating registry path entries...")
            hive_map = {
                "HKLM": winreg.HKEY_LOCAL_MACHINE,
                "HKCU": winreg.HKEY_CURRENT_USER,
                "HKCR": winreg.HKEY_CLASSES_ROOT,
                "HKU":  winreg.HKEY_USERS,
            }
            src_s = str(self.src); dst_s = str(self.dst)
            for i, e in enumerate(self.reg_entries):
                self.progress.emit(68 + int(i / max(len(self.reg_entries), 1) * 20),
                    f"Updating: {e.get('path','')}")
                try:
                    hive = hive_map.get(e["hive"], winreg.HKEY_LOCAL_MACHINE)
                    key = winreg.OpenKey(hive, e["path"], 0,
                                        winreg.KEY_READ | winreg.KEY_SET_VALUE)
                    try:
                        val, vtype = winreg.QueryValueEx(key, e["value_name"])
                        if isinstance(val, str) and src_s.lower() in val.lower():
                            new_val = re.sub(re.escape(src_s), dst_s, val, flags=re.IGNORECASE)
                            winreg.SetValueEx(key, e["value_name"], 0, vtype, new_val)
                    finally:
                        winreg.CloseKey(key)
                except Exception:
                    pass

            self.progress.emit(90, "Removing original folder...")
            shutil.rmtree(str(self.src), ignore_errors=True)
            self.progress.emit(100, "Move complete.")
            self.finished.emit(True, f"Moved to {self.dst}")
        except Exception as ex:
            self.finished.emit(False, str(ex))


# ── Move Dialog ───────────────────────────────────────────────────────────────
class MoveDialog(QDialog):
    def __init__(self, parent, install_path, reg_entries, program_name):
        super().__init__(parent)
        self.install_path = install_path
        self.reg_entries = reg_entries
        self.program_name = program_name
        self.move_worker = None
        self.setWindowTitle("Move Installation")
        self.setModal(True); self.setMinimumSize(700, 500)
        self.setStyleSheet(f"QDialog {{ background-color: {COLORS['surface']}; }}")
        self._build()

    def _build(self):
        v = QVBoxLayout(self)
        v.setContentsMargins(24, 20, 24, 20); v.setSpacing(14)

        ttl = QLabel(f"📦  Move  '{self.program_name}'  to Another Drive")
        ttl.setStyleSheet(f"font-size: 15px; font-weight: bold; color: {COLORS['text']};")
        v.addWidget(ttl)

        # Source group
        sg = QGroupBox("CURRENT INSTALLATION"); slv = QVBoxLayout(sg)
        self.src_edit = QLineEdit(self.install_path or "")
        self.src_edit.setPlaceholderText("e.g.  C:\\Program Files\\Discord")
        src_b = QPushButton("Browse..."); src_b.setFixedWidth(90)
        src_b.clicked.connect(self._browse_src)
        sr = QHBoxLayout(); sr.addWidget(self.src_edit, 1); sr.addWidget(src_b)
        slv.addLayout(sr); v.addWidget(sg)

        # Destination group
        dg = QGroupBox("DESTINATION"); dlv = QVBoxLayout(dg)
        dr = QHBoxLayout()
        dl = QLabel("Target Drive:"); dl.setStyleSheet(f"color:{COLORS['text_dim']};")
        self.drive_combo = QComboBox(); self._populate_drives()
        dr.addWidget(dl); dr.addWidget(self.drive_combo, 1); dlv.addLayout(dr)
        self.dst_edit = QLineEdit()
        self.dst_edit.setPlaceholderText("Full destination path, e.g.  D:\\Program Files\\Discord")
        dst_b = QPushButton("Browse..."); dst_b.setFixedWidth(90)
        dst_b.clicked.connect(self._browse_dst)
        dsr = QHBoxLayout(); dsr.addWidget(self.dst_edit, 1); dsr.addWidget(dst_b)
        dlv.addLayout(dsr)
        self.drive_combo.currentTextChanged.connect(self._auto_dst)
        v.addWidget(dg)

        # Space check label
        self.space_lbl = QLabel("")
        self.space_lbl.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 11px;")
        v.addWidget(self.space_lbl)
        self.drive_combo.currentTextChanged.connect(self._update_space)
        self._update_space()

        # Registry entries preview
        rg = QGroupBox(f"REGISTRY PATH ENTRIES TO UPDATE  ({len(self.reg_entries)} found)")
        rlv = QVBoxLayout(rg)
        self.reg_lw = QListWidget(); self.reg_lw.setMaximumHeight(90)
        if self.reg_entries:
            for e in self.reg_entries:
                self.reg_lw.addItem(f"{e['hive']}\\{e['path']}  →  {e['value_name']}")
        else:
            self.reg_lw.addItem("No registry path entries detected — paths may need manual update.")
        rlv.addWidget(self.reg_lw); v.addWidget(rg)

        # Progress
        self.pb = QProgressBar(); self.pb.setVisible(False)
        self.pl = QLabel(""); self.pl.setVisible(False)
        self.pl.setStyleSheet(f"color:{COLORS['text_dim']}; font-size:11px;")
        v.addWidget(self.pb); v.addWidget(self.pl)

        br = QHBoxLayout()
        self.mv_btn = QPushButton("📦  Move Installation"); self.mv_btn.setObjectName("move")
        self.mv_btn.clicked.connect(self._start_move)
        cb = QPushButton("Cancel"); cb.clicked.connect(self.reject)
        br.addWidget(self.mv_btn); br.addStretch(); br.addWidget(cb)
        v.addLayout(br)

    def _populate_drives(self):
        self.drive_combo.clear()
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if Path(drive).exists():
                try:
                    u = shutil.disk_usage(drive)
                    self.drive_combo.addItem(
                        f"{letter}:  ({u.free//1024**3} GB free / {u.total//1024**3} GB total)", letter)
                except Exception:
                    self.drive_combo.addItem(f"{letter}:", letter)

    def _auto_dst(self, text):
        if not text: return
        dl = text.split(":")[0].strip()
        src = self.src_edit.text().strip()
        if src and len(src) >= 3:
            self.dst_edit.setText(f"{dl}:{src[2:]}")

    def _update_space(self, *_):
        src = self.src_edit.text().strip()
        dl = self.drive_combo.currentText().split(":")[0].strip() if self.drive_combo.currentText() else ""
        if not dl: return
        try:
            src_sz = sum(f.stat().st_size for f in Path(src).rglob("*") if f.is_file()) if src and Path(src).exists() else 0
            free = shutil.disk_usage(f"{dl}:\\").free
            src_mb = src_sz // 1024 // 1024
            free_mb = free // 1024 // 1024
            color = COLORS["success"] if free > src_sz * 1.1 else COLORS["accent"]
            self.space_lbl.setText(f"Installation size: {src_mb} MB   |   Free on {dl}:\\: {free_mb} MB")
            self.space_lbl.setStyleSheet(f"color: {color}; font-size: 11px;")
        except Exception:
            pass

    def _browse_src(self):
        p = QFileDialog.getExistingDirectory(self, "Select Current Install Folder", self.src_edit.text())
        if p: self.src_edit.setText(p); self._update_space()

    def _browse_dst(self):
        p = QFileDialog.getExistingDirectory(self, "Select Destination Folder", self.dst_edit.text())
        if p: self.dst_edit.setText(p)

    def _start_move(self):
        src = self.src_edit.text().strip(); dst = self.dst_edit.text().strip()
        if not src or not dst:
            QMessageBox.warning(self, "Missing Paths", "Please set both source and destination paths."); return
        if not Path(src).exists():
            QMessageBox.warning(self, "Not Found", f"Source not found:\n{src}"); return
        if Path(src).resolve() == Path(dst).resolve():
            QMessageBox.warning(self, "Same Path", "Source and destination are the same."); return
        try:
            src_sz = sum(f.stat().st_size for f in Path(src).rglob("*") if f.is_file())
            free = shutil.disk_usage(Path(dst).anchor).free
            if src_sz > free:
                QMessageBox.critical(self, "Not Enough Space",
                    f"Need {src_sz//1024//1024} MB but only {free//1024//1024} MB free."); return
        except Exception: pass

        self.mv_btn.setEnabled(False)
        self.pb.setVisible(True); self.pl.setVisible(True)
        self.move_worker = MoveWorker(src, dst, self.reg_entries)
        self.move_worker.progress.connect(lambda p, m: (self.pb.setValue(p), self.pl.setText(m)))
        self.move_worker.finished.connect(self._on_done)
        self.move_worker.start()

    def _on_done(self, ok, msg):
        self.pb.setValue(100); self.pl.setText(msg); self.mv_btn.setEnabled(True)
        if ok:
            QMessageBox.information(self, "Move Complete",
                f"{msg}\n\nRegistry path entries updated.\nYou may need to restart the program or your PC.")
            self.accept()
        else:
            QMessageBox.critical(self, "Move Failed", msg)


# ── Scan Worker ───────────────────────────────────────────────────────────────
class ScanWorker(QThread):
    progress = pyqtSignal(int, str)
    found_registry = pyqtSignal(str, str, str)
    found_file = pyqtSignal(str, str)
    found_temp = pyqtSignal(str, str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    UNINSTALL_PATHS = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
    ]

    def __init__(self, query):
        super().__init__()
        self.query = query.lower().strip(); self._cancel = False
        self.results = {"registry": [], "files": [], "temp": [], "install_path": "", "reg_path_entries": []}

    def cancel(self): self._cancel = True

    def _fmt(self, path):
        try:
            p = Path(path)
            sz = p.stat().st_size if p.is_file() else sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
            for u in ["B","KB","MB","GB"]:
                if sz < 1024: return f"{sz:.1f} {u}"
                sz /= 1024
            return f"{sz:.2f} TB"
        except: return "?"

    def _m(self, t): return self.query in str(t).lower()

    def _scan_uninstall(self):
        for hive, hn in [(winreg.HKEY_LOCAL_MACHINE,"HKLM"),(winreg.HKEY_CURRENT_USER,"HKCU")]:
            for up in self.UNINSTALL_PATHS:
                try:
                    key = winreg.OpenKey(hive, up, 0, winreg.KEY_READ)
                    i = 0
                    while True:
                        try:
                            sk = winreg.EnumKey(key, i)
                            try:
                                sub = winreg.OpenKey(key, sk, 0, winreg.KEY_READ)
                                try: dn, _ = winreg.QueryValueEx(sub, "DisplayName")
                                except: dn = sk
                                if self._m(dn) or self._m(sk):
                                    fp = f"{up}\\{sk}"
                                    self.found_registry.emit(hn, fp, f"Uninstall Entry: {dn}")
                                    self.results["registry"].append({"hive":hn,"path":fp,"value":f"Uninstall Entry: {dn}"})
                                    for vn in ["InstallLocation","UninstallString","DisplayIcon","InstallSource"]:
                                        try:
                                            v, _ = winreg.QueryValueEx(sub, vn)
                                            vs = str(v)
                                            if vs:
                                                self.found_registry.emit(hn, fp, f"{vn}: {vs[:80]}")
                                                self.results["registry"].append({"hive":hn,"path":fp,"value":f"{vn}: {vs[:80]}"})
                                                self.results["reg_path_entries"].append({"hive":hn,"path":fp,"value_name":vn,"old_value":vs})
                                                if vn == "InstallLocation":
                                                    cl = vs.strip().strip('"')
                                                    if cl and Path(cl).exists():
                                                        if not self.results["install_path"]:
                                                            self.results["install_path"] = cl
                                                        sz = self._fmt(cl)
                                                        self.found_file.emit(cl, sz)
                                                        self.results["files"].append({"path":cl,"size":sz,"source":"InstallLocation"})
                                        except: pass
                                winreg.CloseKey(sub)
                            except: pass
                            i += 1
                        except OSError: break
                    winreg.CloseKey(key)
                except OSError: pass
            if self._cancel: return

    def _scan_software_keys(self):
        for hive, hn, base in [(winreg.HKEY_LOCAL_MACHINE,"HKLM",r"SOFTWARE"),
                                (winreg.HKEY_CURRENT_USER,"HKCU",r"SOFTWARE")]:
            try:
                key = winreg.OpenKey(hive, base, 0, winreg.KEY_READ)
                i = 0
                while True:
                    if self._cancel: return
                    try:
                        sk = winreg.EnumKey(key, i)
                        if self._m(sk):
                            fp = f"{base}\\{sk}"
                            self.found_registry.emit(hn, fp, "Software Key")
                            self.results["registry"].append({"hive":hn,"path":fp,"value":"Software Key"})
                            try:
                                sub = winreg.OpenKey(hive, fp, 0, winreg.KEY_READ)
                                j = 0
                                while True:
                                    try:
                                        name, data, _ = winreg.EnumValue(sub, j)
                                        ds = str(data)
                                        if any(kw in ds.lower() for kw in [":\\","program files","appdata"]):
                                            self.results["reg_path_entries"].append(
                                                {"hive":hn,"path":fp,"value_name":name,"old_value":ds})
                                        j += 1
                                    except OSError: break
                                winreg.CloseKey(sub)
                            except: pass
                        i += 1
                    except OSError: break
                winreg.CloseKey(key)
            except OSError: pass

    def _scan_files(self):
        dirs = [
            os.environ.get("ProgramFiles", r"C:\Program Files"),
            os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
            os.environ.get("LOCALAPPDATA",""),
            os.environ.get("APPDATA",""),
            os.environ.get("ProgramData", r"C:\ProgramData"),
        ]
        for base in dirs:
            if not base or not Path(base).exists(): continue
            try:
                for e in Path(base).iterdir():
                    if self._cancel: return
                    if self._m(e.name):
                        sz = self._fmt(str(e))
                        self.found_file.emit(str(e), sz)
                        self.results["files"].append({"path":str(e),"size":sz,"source":"Program Files"})
                        if not self.results["install_path"] and e.is_dir():
                            self.results["install_path"] = str(e)
            except PermissionError: pass

    def _scan_temp(self):
        td = os.environ.get("TEMP") or tempfile.gettempdir()
        if not td or not Path(td).exists(): return
        try:
            for e in Path(td).rglob("*"):
                if self._cancel: return
                if self._m(e.name):
                    sz = self._fmt(str(e))
                    self.found_temp.emit(str(e), sz)
                    self.results["temp"].append({"path":str(e),"size":sz})
        except: pass

    def run(self):
        try:
            self.progress.emit(5, "Scanning Uninstall registry entries...")
            self._scan_uninstall()
            if self._cancel: return
            self.progress.emit(35, "Scanning SOFTWARE registry keys...")
            self._scan_software_keys()
            if self._cancel: return
            self.progress.emit(60, "Scanning program file locations...")
            self._scan_files()
            if self._cancel: return
            self.progress.emit(82, "Scanning %TEMP% folder...")
            self._scan_temp()
            if self._cancel: return
            self.progress.emit(100, "Scan complete.")
            self.finished.emit(self.results)
        except Exception as ex:
            self.error.emit(str(ex))


# ── Delete Worker ─────────────────────────────────────────────────────────────
class DeleteWorker(QThread):
    progress = pyqtSignal(int, str)
    item_done = pyqtSignal(str, bool, str)
    finished = pyqtSignal(int, int)

    def __init__(self, items):
        super().__init__(); self.items = items

    def run(self):
        total = len(self.items); success = fail = 0
        hm = {"HKLM":winreg.HKEY_LOCAL_MACHINE,"HKCU":winreg.HKEY_CURRENT_USER,
              "HKCR":winreg.HKEY_CLASSES_ROOT,"HKU":winreg.HKEY_USERS}
        for i, item in enumerate(self.items):
            pct = int(i / max(total,1) * 100)
            if item["type"] == "file":
                p = item["path"]
                self.progress.emit(pct, f"Deleting: {p}")
                try:
                    pp = Path(p)
                    if pp.is_dir(): shutil.rmtree(p)
                    elif pp.is_file(): pp.unlink()
                    self.item_done.emit(p, True, ""); success += 1
                except Exception as ex:
                    self.item_done.emit(p, False, str(ex)); fail += 1
            elif item["type"] == "registry":
                hn = item.get("hive","HKLM"); kp = item.get("path","")
                self.progress.emit(pct, f"Removing: {hn}\\{kp}")
                try:
                    winreg.DeleteKey(hm.get(hn, winreg.HKEY_LOCAL_MACHINE), kp)
                    self.item_done.emit(f"{hn}\\{kp}", True, ""); success += 1
                except Exception as ex:
                    self.item_done.emit(f"{hn}\\{kp}", False, str(ex)); fail += 1
        self.finished.emit(success, fail)


# ── Main Window ───────────────────────────────────────────────────────────────
class UninstalldWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scan_worker = self.delete_worker = None
        self.scan_results = {}
        self.setWindowTitle("Uninstall'd")
        self.setMinimumSize(1100, 740); self.resize(1260, 820)
        self.setStyleSheet(SS); self._build_ui()

    def _build_ui(self):
        c = QWidget(); c.setStyleSheet(f"background-color: {COLORS['bg']};")
        self.setCentralWidget(c)
        root = QVBoxLayout(c); root.setContentsMargins(0,0,0,0); root.setSpacing(0)
        root.addWidget(self._build_header())
        root.addWidget(self._build_search())
        self.prog_frame = self._build_progress()
        self.prog_frame.setVisible(False)
        root.addWidget(self.prog_frame)
        root.addWidget(self._build_results(), 1)
        root.addWidget(self._build_action_bar())
        self.status = QStatusBar(); self.status.setFixedHeight(28)
        self.setStatusBar(self.status)
        self._set_status("Ready — enter a program name and click SCAN")

    def _build_header(self):
        f = QFrame()
        f.setStyleSheet(f"QFrame{{background:{COLORS['surface']};border-bottom:1px solid {COLORS['border']};}}")
        f.setFixedHeight(72); h = QHBoxLayout(f); h.setContentsMargins(28,0,28,0)
        logo = QLabel("⌫"); logo.setStyleSheet(f"font-size:28px;color:{COLORS['accent']};background:transparent;font-weight:bold;")
        title = QLabel("UNINSTALL'D"); title.setStyleSheet(f"font-size:22px;font-weight:bold;color:{COLORS['text']};letter-spacing:4px;background:transparent;")
        tag = QLabel("Deep Program Removal for Windows"); tag.setStyleSheet(f"font-size:12px;color:{COLORS['text_muted']};letter-spacing:1px;background:transparent;")
        self.restore_btn = QPushButton("🔄  Restore Registry"); self.restore_btn.setObjectName("restore")
        self.restore_btn.setFixedWidth(190); self.restore_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.restore_btn.clicked.connect(self._open_restore)
        ver = QLabel("v1.1"); ver.setStyleSheet(f"font-size:11px;color:{COLORS['text_muted']};background:transparent;")
        ver.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
        h.addWidget(logo); h.addSpacing(12); h.addWidget(title); h.addSpacing(16)
        vl = QVBoxLayout(); vl.addStretch(); vl.addWidget(tag); vl.addStretch()
        h.addLayout(vl); h.addStretch()
        h.addWidget(self.restore_btn); h.addSpacing(16); h.addWidget(ver)
        return f

    def _build_search(self):
        f = QFrame(); f.setStyleSheet(f"background:{COLORS['bg']};border:none;"); f.setFixedHeight(70)
        h = QHBoxLayout(f); h.setContentsMargins(28,12,28,12); h.setSpacing(12)
        lbl = QLabel("PROGRAM NAME"); lbl.setStyleSheet(f"color:{COLORS['text_muted']};font-size:11px;letter-spacing:2px;"); lbl.setFixedWidth(120)
        self.search_input = QLineEdit(); self.search_input.setPlaceholderText("e.g.  Discord,  Spotify,  Adobe Photoshop...")
        self.search_input.returnPressed.connect(self._start_scan)
        self.scan_btn = QPushButton("▶  SCAN"); self.scan_btn.setObjectName("scan"); self.scan_btn.setFixedWidth(140)
        self.scan_btn.setCursor(Qt.CursorShape.PointingHandCursor); self.scan_btn.clicked.connect(self._start_scan)
        self.cancel_btn = QPushButton("CANCEL"); self.cancel_btn.setFixedWidth(100); self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self._cancel_scan)
        h.addWidget(lbl); h.addWidget(self.search_input, 1); h.addWidget(self.scan_btn); h.addWidget(self.cancel_btn)
        return f

    def _build_progress(self):
        f = QFrame(); f.setStyleSheet(f"background:{COLORS['bg']};border:none;"); f.setFixedHeight(44)
        h = QHBoxLayout(f); h.setContentsMargins(28,4,28,4); h.setSpacing(14)
        self.prog_bar = QProgressBar(); self.prog_bar.setFixedHeight(6); self.prog_bar.setRange(0,100)
        self.prog_lbl = QLabel("Scanning..."); self.prog_lbl.setStyleSheet(f"color:{COLORS['text_dim']};font-size:12px;"); self.prog_lbl.setFixedWidth(360)
        h.addWidget(self.prog_bar, 1); h.addWidget(self.prog_lbl)
        return f

    def _badge(self, label, count, color):
        f = QFrame(); f.setStyleSheet(f"QFrame{{background:{COLORS['surface']};border:1px solid {COLORS['border']};border-radius:6px;}}"); f.setFixedHeight(52); f.setFixedWidth(185)
        h = QHBoxLayout(f); h.setContentsMargins(14,8,14,8)
        cl = QLabel(count); cl.setStyleSheet(f"font-size:22px;font-weight:bold;color:{color};background:transparent;")
        nl = QLabel(label); nl.setStyleSheet(f"font-size:11px;color:{COLORS['text_muted']};background:transparent;")
        h.addWidget(cl); h.addSpacing(8); h.addWidget(nl); h.addStretch()
        return f, cl

    def _build_results(self):
        f = QFrame(); f.setStyleSheet(f"background:{COLORS['bg']};border:none;")
        outer = QVBoxLayout(f); outer.setContentsMargins(28,8,28,8); outer.setSpacing(0)

        sr = QHBoxLayout()
        self.stat_reg = self._badge("Registry Keys","0",COLORS["scan_reg"])
        self.stat_files = self._badge("Files / Folders","0",COLORS["scan_file"])
        self.stat_temp = self._badge("Temp Files","0",COLORS["scan_temp"])
        self.install_lbl = QLabel("No install path detected")
        self.install_lbl.setStyleSheet(f"color:{COLORS['text_muted']};font-size:11px;background:{COLORS['surface']};border:1px solid {COLORS['border']};border-radius:6px;padding:6px 14px;")
        self.move_btn = QPushButton("📦  Move to Drive..."); self.move_btn.setObjectName("move")
        self.move_btn.setEnabled(False); self.move_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.move_btn.clicked.connect(self._open_move)
        sr.addWidget(self.stat_reg[0]); sr.addSpacing(10)
        sr.addWidget(self.stat_files[0]); sr.addSpacing(10)
        sr.addWidget(self.stat_temp[0]); sr.addSpacing(16)
        sr.addWidget(self.install_lbl); sr.addSpacing(8)
        sr.addWidget(self.move_btn); sr.addStretch()
        outer.addLayout(sr); outer.addSpacing(12)

        sp = QSplitter(Qt.Orientation.Horizontal); sp.setHandleWidth(1)

        lp = QWidget(); lp.setStyleSheet("background:transparent;"); lv = QVBoxLayout(lp); lv.setContentsMargins(0,0,6,0); lv.setSpacing(8)
        rl = QLabel("◆  REGISTRY ENTRIES"); rl.setStyleSheet(f"color:{COLORS['scan_reg']};font-size:11px;letter-spacing:2px;"); lv.addWidget(rl)
        self.reg_tree = QTreeWidget(); self.reg_tree.setHeaderLabels(["Hive","Key Path","Value / Detail"])
        self.reg_tree.setColumnWidth(0,60); self.reg_tree.setColumnWidth(1,260)
        self.reg_tree.setAlternatingRowColors(True); self.reg_tree.setSelectionMode(QTreeWidget.SelectionMode.MultiSelection)
        lv.addWidget(self.reg_tree, 1)
        fl = QLabel("◆  FILES & FOLDERS"); fl.setStyleSheet(f"color:{COLORS['scan_file']};font-size:11px;letter-spacing:2px;"); lv.addWidget(fl)
        self.files_tree = QTreeWidget(); self.files_tree.setHeaderLabels(["Path","Size","Source"])
        self.files_tree.setColumnWidth(0,280); self.files_tree.setColumnWidth(1,70)
        self.files_tree.setAlternatingRowColors(True); self.files_tree.setSelectionMode(QTreeWidget.SelectionMode.MultiSelection)
        lv.addWidget(self.files_tree, 1)

        rp = QWidget(); rp.setStyleSheet("background:transparent;"); rv = QVBoxLayout(rp); rv.setContentsMargins(6,0,0,0); rv.setSpacing(8)
        tl = QLabel("◆  TEMP FILES"); tl.setStyleSheet(f"color:{COLORS['scan_temp']};font-size:11px;letter-spacing:2px;"); rv.addWidget(tl)
        self.temp_tree = QTreeWidget(); self.temp_tree.setHeaderLabels(["Path","Size"])
        self.temp_tree.setColumnWidth(0,300); self.temp_tree.setAlternatingRowColors(True)
        self.temp_tree.setSelectionMode(QTreeWidget.SelectionMode.MultiSelection)
        rv.addWidget(self.temp_tree, 1)
        ll = QLabel("◆  OPERATION LOG"); ll.setStyleSheet(f"color:{COLORS['text_muted']};font-size:11px;letter-spacing:2px;"); rv.addWidget(ll)
        self.log = QTextEdit(); self.log.setReadOnly(True); self.log.setMaximumHeight(170); rv.addWidget(self.log)

        sp.addWidget(lp); sp.addWidget(rp); sp.setSizes([650,390])
        outer.addWidget(sp, 1); return f

    def _build_action_bar(self):
        f = QFrame(); f.setStyleSheet(f"QFrame{{background:{COLORS['surface']};border-top:1px solid {COLORS['border']};}}")
        f.setFixedHeight(64); h = QHBoxLayout(f); h.setContentsMargins(28,0,28,0); h.setSpacing(12)
        self.chk_reg = QCheckBox("Delete Registry Entries")
        self.chk_files = QCheckBox("Delete Files & Folders")
        self.chk_temp = QCheckBox("Delete Temp Files")
        for chk in [self.chk_reg, self.chk_files, self.chk_temp]:
            chk.setChecked(True); chk.setEnabled(False)
        self.sel_all_btn = QPushButton("Select All"); self.sel_all_btn.setEnabled(False)
        self.sel_all_btn.clicked.connect(self._select_all)
        self.del_btn = QPushButton("🗑  DELETE SELECTED"); self.del_btn.setObjectName("danger")
        self.del_btn.setFixedWidth(210); self.del_btn.setEnabled(False)
        self.del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.del_btn.clicked.connect(self._confirm_delete)
        h.addWidget(self.chk_reg); h.addWidget(self.chk_files); h.addWidget(self.chk_temp)
        h.addStretch(); h.addWidget(self.sel_all_btn); h.addWidget(self.del_btn)
        return f

    # ── Backup gate ────────────────────────────────────────────────────────────
    def _require_backup_consent(self, action_desc, program_name=""):
        dlg = BackupPromptDialog(self, action_desc)
        if _ICON_PATH: dlg.setWindowIcon(QIcon(_ICON_PATH))
        dlg.exec()
        if dlg.choice == "cancel":
            self._set_status("Action cancelled."); return False
        if dlg.choice == "backup":
            self._set_status("Creating registry backup...")
            try:
                bp = backup_registry(program_name or self.search_input.text().strip() or "unknown")
                self._log(f'<span style="color:{COLORS["success"]}">✓ Backup saved: {bp}</span>')
                self._set_status(f"Backup saved — {bp.name}")
            except Exception as ex:
                self._log(f'<span style="color:{COLORS["accent"]}">✗ Backup failed: {ex}</span>')
                r = QMessageBox.question(self, "Backup Failed", f"Backup failed:\n{ex}\n\nContinue anyway?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
                if r != QMessageBox.StandardButton.Yes: return False
        return True

    def _open_restore(self):
        dlg = RestoreDialog(self)
        if _ICON_PATH: dlg.setWindowIcon(QIcon(_ICON_PATH))
        dlg.exec()

    def _open_move(self):
        prog = self.search_input.text().strip()
        if not self._require_backup_consent(f"move '{prog}' to another drive", prog): return
        dlg = MoveDialog(self, self.scan_results.get("install_path",""), self.scan_results.get("reg_path_entries",[]), prog)
        if _ICON_PATH: dlg.setWindowIcon(QIcon(_ICON_PATH))
        dlg.exec()

    # ── Scan ───────────────────────────────────────────────────────────────────
    def _start_scan(self):
        q = self.search_input.text().strip()
        if not q: self._set_status("Please enter a program name first."); return
        self._clear()
        self.scan_btn.setEnabled(False); self.cancel_btn.setEnabled(True)
        self.del_btn.setEnabled(False); self.sel_all_btn.setEnabled(False)
        self.move_btn.setEnabled(False)
        self.prog_frame.setVisible(True); self.prog_bar.setValue(0)
        self.scan_worker = ScanWorker(q)
        self.scan_worker.progress.connect(self._on_prog)
        self.scan_worker.found_registry.connect(self._on_reg)
        self.scan_worker.found_file.connect(self._on_file)
        self.scan_worker.found_temp.connect(self._on_temp)
        self.scan_worker.finished.connect(self._on_scan_done)
        self.scan_worker.error.connect(self._on_err)
        self.scan_worker.start()

    def _cancel_scan(self):
        if self.scan_worker: self.scan_worker.cancel()
        self._set_status("Scan cancelled."); self.scan_btn.setEnabled(True); self.cancel_btn.setEnabled(False)

    def _clear(self):
        self.reg_tree.clear(); self.files_tree.clear(); self.temp_tree.clear(); self.log.clear()
        self.scan_results = {}
        self.stat_reg[1].setText("0"); self.stat_files[1].setText("0"); self.stat_temp[1].setText("0")
        self.install_lbl.setText("No install path detected")

    def _on_prog(self, p, m):
        self.prog_bar.setValue(p); self.prog_lbl.setText(m); self._log(m)

    def _on_reg(self, hive, path, value):
        it = QTreeWidgetItem([hive, path, value])
        it.setForeground(0, QColor(COLORS["scan_reg"])); it.setCheckState(0, Qt.CheckState.Checked)
        self.reg_tree.addTopLevelItem(it); self.stat_reg[1].setText(str(self.reg_tree.topLevelItemCount()))

    def _on_file(self, path, size):
        it = QTreeWidgetItem([path, size, "Scan"])
        it.setForeground(0, QColor(COLORS["scan_file"])); it.setCheckState(0, Qt.CheckState.Checked)
        self.files_tree.addTopLevelItem(it); self.stat_files[1].setText(str(self.files_tree.topLevelItemCount()))

    def _on_temp(self, path, size):
        it = QTreeWidgetItem([path, size])
        it.setForeground(0, QColor(COLORS["scan_temp"])); it.setCheckState(0, Qt.CheckState.Checked)
        self.temp_tree.addTopLevelItem(it); self.stat_temp[1].setText(str(self.temp_tree.topLevelItemCount()))

    def _on_scan_done(self, results):
        self.scan_results = results
        self.prog_frame.setVisible(False); self.scan_btn.setEnabled(True); self.cancel_btn.setEnabled(False)
        ip = results.get("install_path","")
        if ip:
            short = ip if len(ip)<50 else "..."+ip[-46:]
            self.install_lbl.setText(f"📁  {short}"); self.move_btn.setEnabled(True)
        total = self.reg_tree.topLevelItemCount()+self.files_tree.topLevelItemCount()+self.temp_tree.topLevelItemCount()
        if total > 0:
            self.del_btn.setEnabled(True); self.sel_all_btn.setEnabled(True)
            for chk in [self.chk_reg,self.chk_files,self.chk_temp]: chk.setEnabled(True)
            self._set_status(f"Scan complete — {self.reg_tree.topLevelItemCount()} registry, {self.files_tree.topLevelItemCount()} files, {self.temp_tree.topLevelItemCount()} temp.")
        else:
            self._set_status(f"No traces found for '{self.search_input.text()}'.")
        self._log(f"Scan finished. {total} items found.")

    def _on_err(self, msg):
        self._log(f'<span style="color:{COLORS["accent"]}">ERROR: {msg}</span>')
        self._set_status(f"Error: {msg}"); self.scan_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False); self.prog_frame.setVisible(False)

    # ── Delete ──────────────────────────────────────────────────────────────────
    def _select_all(self):
        for tree in [self.reg_tree, self.files_tree, self.temp_tree]:
            for i in range(tree.topLevelItemCount()):
                tree.topLevelItem(i).setCheckState(0, Qt.CheckState.Checked)

    def _gather(self):
        items = []
        if self.chk_reg.isChecked():
            for i in range(self.reg_tree.topLevelItemCount()):
                it = self.reg_tree.topLevelItem(i)
                if it.checkState(0)==Qt.CheckState.Checked:
                    items.append({"type":"registry","hive":it.text(0),"path":it.text(1)})
        if self.chk_files.isChecked():
            for i in range(self.files_tree.topLevelItemCount()):
                it = self.files_tree.topLevelItem(i)
                if it.checkState(0)==Qt.CheckState.Checked:
                    items.append({"type":"file","path":it.text(0)})
        if self.chk_temp.isChecked():
            for i in range(self.temp_tree.topLevelItemCount()):
                it = self.temp_tree.topLevelItem(i)
                if it.checkState(0)==Qt.CheckState.Checked:
                    items.append({"type":"file","path":it.text(0)})
        return items

    def _confirm_delete(self):
        items = self._gather()
        if not items: self._set_status("No items selected."); return
        prog = self.search_input.text().strip()
        if not self._require_backup_consent(f"permanently delete {len(items)} items related to '{prog}'", prog): return
        m = QMessageBox(self); m.setWindowTitle("Confirm Deletion")
        m.setText(f"<b style='color:{COLORS['accent']};'>Permanently delete {len(items)} items?</b><br><br>"
                  "This cannot be undone (unless you backed up above).")
        m.setStyleSheet(f"QMessageBox{{background:{COLORS['surface']};color:{COLORS['text']};}}")
        m.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.Cancel)
        m.setDefaultButton(QMessageBox.StandardButton.Cancel)
        if m.exec()!=QMessageBox.StandardButton.Yes: return
        self.del_btn.setEnabled(False); self.scan_btn.setEnabled(False)
        self.prog_frame.setVisible(True); self.prog_bar.setValue(0)
        self.delete_worker = DeleteWorker(items)
        self.delete_worker.progress.connect(self._on_prog)
        self.delete_worker.item_done.connect(self._on_item_done)
        self.delete_worker.finished.connect(self._on_del_done)
        self.delete_worker.start()

    def _on_item_done(self, path, ok, err):
        c = COLORS["success"] if ok else COLORS["accent"]
        i = "✓" if ok else "✗"
        self._log(f'<span style="color:{c}">{i} {path}{" — "+err if err else ""}</span>')

    def _on_del_done(self, s, f):
        self.prog_frame.setVisible(False); self.scan_btn.setEnabled(True)
        self._set_status(f"Deletion complete — {s} succeeded, {f} failed.")
        self._log(f"Done. {s} removed, {f} failed."); self._clear()

    def _set_status(self, m): self.status.showMessage(f"  {m}")
    def _log(self, m): self.log.append(m)


# ── Entry Point ───────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Uninstall'd"); app.setApplicationVersion("1.1")
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window, QColor(COLORS["bg"]))
    pal.setColor(QPalette.ColorRole.WindowText, QColor(COLORS["text"]))
    app.setPalette(pal)
    if _ICON_PATH and os.path.exists(_ICON_PATH):
        app.setWindowIcon(QIcon(_ICON_PATH))
    win = UninstalldWindow()
    if _ICON_PATH and os.path.exists(_ICON_PATH):
        win.setWindowIcon(QIcon(_ICON_PATH))
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
