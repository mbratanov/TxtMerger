from PySide6.QtCore import QSettings


class AppSettings:
    """Handles persistent application settings."""

    def __init__(self):
        self._settings = QSettings("Possible", "TxtMerger")

    @property
    def source_dir(self) -> str:
        return self._settings.value("source_dir", "")

    @source_dir.setter
    def source_dir(self, value: str):
        self._settings.setValue("source_dir", value)

    @property
    def output_dir(self) -> str:
        return self._settings.value("output_dir", "")

    @output_dir.setter
    def output_dir(self, value: str):
        self._settings.setValue("output_dir", value)
