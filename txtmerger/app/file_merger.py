import os
from typing import Optional, Callable


class FileMerger:
    """Handles the core logic of merging text files."""

    def merge_files(
            self,
            source_dir: str,
            output_file: str,
            progress_callback: Optional[Callable[[str, int, int], None]] = None
    ) -> int:
        """
        Merge all .txt files from source_dir into output_file.

        Args:
            source_dir: Directory containing .txt files
            output_file: Output file path
            progress_callback: Function with signature (filename, current, total)
        """
        if not os.path.isdir(source_dir):
            raise FileNotFoundError(f"Directory not found: {source_dir}")

        txt_files = [f for f in os.listdir(source_dir) if f.endswith(".txt")]
        total_files = len(txt_files)

        if total_files == 0:
            return 0

        try:
            with open(output_file, "w", encoding="utf-8") as out_file:
                for i, filename in enumerate(txt_files, 1):
                    filepath = os.path.join(source_dir, filename)
                    try:
                        with open(filepath, "r", encoding="utf-8") as in_file:
                            out_file.write(in_file.read())

                        if progress_callback:
                            progress_callback(filename, i, total_files)

                    except UnicodeDecodeError:
                        continue

            return total_files

        except PermissionError as e:
            raise PermissionError(f"Cannot write to {output_file}") from e
