import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QLabel,
                               QPushButton, QFileDialog, QProgressBar,
                               QMessageBox)
import qtawesome as qta

from txtmerger.app.file_merger import FileMerger
from txtmerger.app.settings import AppSettings
from txtmerger.utils.styles import APP_STYLESHEET


class MainWindow(QWidget):
    """Main application window for TxtMerger."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TxtMerger")
        self.setFixedWidth(400)

        self.settings = AppSettings()
        self.file_merger = FileMerger()
        self.output_file_path = ""

        self._init_ui()
        self._setup_connections()

    def _init_ui(self):
        """Initialize all UI components."""
        self.setStyleSheet(APP_STYLESHEET)

        layout = QVBoxLayout()

        # Source Directory Group
        self.source_dir_group = QGroupBox("Source Dir")
        self.source_dir_label = QLabel(self.settings.source_dir or "Not selected")
        self.source_dir_label.setWordWrap(True)
        self.btn_source_dir = QPushButton(qta.icon("fa6.folder-open"), " Select source directory")
        self.btn_source_dir.setFixedHeight(50)

        source_dir_layout = QVBoxLayout()
        source_dir_layout.addWidget(self.source_dir_label)
        source_dir_layout.addWidget(self.btn_source_dir)
        self.source_dir_group.setLayout(source_dir_layout)

        # Output File Group
        self.output_file_group = QGroupBox("Output File")
        self.output_file_label = QLabel("Not selected")
        self.output_file_label.setWordWrap(True)
        self.btn_output_file = QPushButton(qta.icon("fa6.file"), " Select output file")
        self.btn_output_file.setFixedHeight(50)

        output_file_layout = QVBoxLayout()
        output_file_layout.addWidget(self.output_file_label)
        output_file_layout.addWidget(self.btn_output_file)
        self.output_file_group.setLayout(output_file_layout)

        # Progress Group
        self.progress_group = QGroupBox("Progress")
        self.progress_bar = QProgressBar()
        self.status_label = QLabel("Idle")

        progress_layout = QVBoxLayout()
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.status_label)
        self.progress_group.setLayout(progress_layout)

        # Merge Button
        self.btn_merge = QPushButton(qta.icon("fa6s.gears"), " Merge .txt files")
        self.btn_merge.setFixedHeight(50)

        # Assemble main layout
        layout.addWidget(self.source_dir_group)
        layout.addWidget(self.output_file_group)
        layout.addWidget(self.progress_group)
        layout.addWidget(self.btn_merge)

        self.setLayout(layout)

    def _setup_connections(self):
        """Connect signals to slots."""
        self.btn_source_dir.clicked.connect(self._select_source_dir)
        self.btn_output_file.clicked.connect(self._select_output_file)
        self.btn_merge.clicked.connect(self._merge_files)

    def _select_source_dir(self):
        """Handle source directory selection."""
        selected_dir = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            self.settings.source_dir or ""
        )
        if selected_dir:
            self.settings.source_dir = selected_dir
            self.source_dir_label.setText(selected_dir)

    def _select_output_file(self):
        """Handle output file selection."""
        output_file, _ = QFileDialog.getSaveFileName(
            self,
            "Save File As",
            self.settings.source_dir or "",
            "Text Files (*.txt)"
        )
        if output_file:
            if not output_file.endswith(".txt"):
                output_file += ".txt"
            self.output_file_path = output_file
            self.settings.output_dir = os.path.dirname(output_file)
            self.output_file_label.setText(f"Output File: {os.path.basename(output_file)}")

    def _merge_files(self):
        """Handle the merge operation."""
        if not self.settings.source_dir:
            QMessageBox.warning(self, "Error", "Please select a source directory")
            return

        if not self.output_file_path:
            QMessageBox.warning(self, "Error", "Please select an output file")
            return

        self.progress_bar.setValue(0)
        self.status_label.setText("Starting merge...")

        try:
            def progress_callback(filename, current, total):
                self.progress_bar.setMaximum(total)
                self.progress_bar.setValue(current)
                self.status_label.setText(f"Merging: {filename} ({current}/{total})")
                QApplication.processEvents()

            total_merged = self.file_merger.merge_files(
                self.settings.source_dir,
                self.output_file_path,
                progress_callback
            )

            self.status_label.setText(f"Merge complete! {total_merged} files merged.")
            QMessageBox.information(
                self,
                "Success",
                f"Successfully merged {total_merged} files into '{os.path.basename(self.output_file_path)}'"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.status_label.setText("Merge failed")
