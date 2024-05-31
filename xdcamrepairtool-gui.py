import sys
import os
import glob
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QProgressBar, QTextEdit, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal

def repair_video_file(reference_file, corrupted_file, output_dir, file_type):
    if file_type == 'MTS':
        return repair_mts_file(reference_file, corrupted_file, output_dir)
    elif file_type == 'MXF':
        return repair_mxf_file(reference_file, corrupted_file, output_dir)
    else:
        raise ValueError("Unsupported file type.")

def repair_mts_file(reference_file, corrupted_file, output_dir):
    with open(reference_file, 'rb') as ref:
        reference_data = ref.read(768)

    with open(corrupted_file, 'rb') as corr:
        corrupted_data = corr.read()

    repaired_data = reference_data + corrupted_data[768:]

    filename = os.path.splitext(os.path.basename(corrupted_file))[0]  # Get base filename without extension
    os.makedirs(output_dir, exist_ok=True)

    # Remove any additional extensions from the filename
    filename = os.path.splitext(filename)[0]

    repaired_file_path = os.path.join(output_dir, filename + '.MTS')
    with open(repaired_file_path, 'wb') as repaired_file:
        repaired_file.write(repaired_data)

    return repaired_file_path

def repair_mxf_file(reference_file, corrupted_file, output_dir):
    with open(reference_file, 'rb') as ref:
        reference_data = ref.read(524308)

    with open(corrupted_file, 'rb') as corr:
        corrupted_data = corr.read()

    repaired_data = reference_data + corrupted_data[524308:]

    filename = os.path.splitext(os.path.basename(corrupted_file))[0]  # Get base filename without extension
    os.makedirs(output_dir, exist_ok=True)

    # Remove any additional extensions from the filename
    filename = os.path.splitext(filename)[0]

    repaired_file_path = os.path.join(output_dir, filename + '.MXF')
    with open(repaired_file_path, 'wb') as repaired_file:
        repaired_file.write(repaired_data)

    return repaired_file_path

class VideoRepairWorker(QThread):
    progress_updated = pyqtSignal(int)
    log_updated = pyqtSignal(str)
    repair_finished = pyqtSignal(str)

    def __init__(self, reference_file, corrupted_files, output_dir, file_type):
        super().__init__()
        self.reference_file = reference_file
        self.corrupted_files = corrupted_files
        self.output_dir = output_dir
        self.file_type = file_type

    def run(self):
        os.makedirs(self.output_dir, exist_ok=True)  # Create the "Repaired" folder if it doesn't exist
        total_files = len(self.corrupted_files)
        for i, file in enumerate(self.corrupted_files):
            self.progress_updated.emit((i + 1) * 100 / total_files)
            file_name = os.path.basename(file)
            self.log_updated.emit(f"Processing {file_name}...")
            try:
                repaired_file_path = repair_video_file(self.reference_file, file, self.output_dir, self.file_type)
                self.log_updated.emit(f"{file_name} repaired. Saved to: {repaired_file_path}")
            except Exception as e:
                self.log_updated.emit(f"Error repairing {file_name}: {str(e)}")
        self.progress_updated.emit(100)
        self.repair_finished.emit("All files repaired.")

class VideoRepairApp(QWidget):
    log_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Repair Tool")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.file_type_label = QLabel("Select File Type:")
        self.file_type_edit = QLineEdit()
        self.file_type_edit.setReadOnly(True)

        self.file_type_browse_button = QPushButton("Browse", self)
        self.file_type_browse_button.setObjectName("browseButton")
        self.file_type_browse_button.clicked.connect(self.browse_file_type)

        self.reference_label = QLabel("Reference File:")
        self.reference_path_edit = QLineEdit()
        self.reference_browse_button = QPushButton("Browse", self)
        self.reference_browse_button.setObjectName("browseButton")
        self.reference_browse_button.clicked.connect(self.browse_reference_file)

        self.corrupted_label = QLabel("Corrupted Folder:")
        self.corrupted_path_edit = QLineEdit()
        self.corrupted_browse_button = QPushButton("Browse", self)
        self.corrupted_browse_button.setObjectName("browseButton")
        self.corrupted_browse_button.clicked.connect(self.browse_corrupted_folder)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        self.repair_button = QPushButton("Repair", self)
        self.repair_button.setObjectName("blueButton")
        self.repair_button.clicked.connect(self.repair_all_files)

        layout.addWidget(self.file_type_label)
        layout.addWidget(self.file_type_edit)
        layout.addWidget(self.file_type_browse_button)
        layout.addWidget(self.reference_label)
        layout.addWidget(self.reference_path_edit)
        layout.addWidget(self.reference_browse_button)
        layout.addWidget(self.corrupted_label)
        layout.addWidget(self.corrupted_path_edit)
        layout.addWidget(self.corrupted_browse_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.log_box)
        layout.addWidget(self.repair_button)

        self.setLayout(layout)

        self.setStyleSheet("""
        #browseButton, #blueButton {
            background-color: #3498db;
            border: none;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 4px;
        }
        #browseButton:hover, #blueButton:hover {
            background-color: #2980b9;
        }
        """)

        self.log_updated.connect(self.update_log)

    def browse_file_type(self):
        file_type, _ = QFileDialog.getOpenFileName(self, "Select File Type (MTS or MXF)", "", "MTS Files (*.MTS);;MXF Files (*.MXF)")
        if file_type:
            self.file_type_edit.setText(file_type.split('.')[-1].upper())

    def browse_reference_file(self):
        reference_file, _ = QFileDialog.getOpenFileName(self, "Select Reference File", "", "All Files (*.*)")
        if reference_file:
            self.reference_path_edit.setText(reference_file)

    def browse_corrupted_folder(self):
        corrupted_folder = QFileDialog.getExistingDirectory(self, "Select Corrupted Folder")
        if corrupted_folder:
            self.corrupted_path_edit.setText(corrupted_folder)

    def repair_all_files(self):
        reference_file_path = self.reference_path_edit.text()
        corrupted_folder_path = self.corrupted_path_edit.text()
        file_type = self.file_type_edit.text().upper()

        if not os.path.exists(reference_file_path):
            self.show_message("Error", "Reference file does not exist.")
            return
        if not os.path.exists(corrupted_folder_path):
            self.show_message("Error", "Corrupted folder does not exist.")
            return
        if file_type not in ['MTS', 'MXF']:
            self.show_message("Error", "Invalid file type. Must be MTS or MXF.")
            return

        encrypted_files = glob.glob(os.path.join(corrupted_folder_path, f'*.{file_type}.*'))
        output_dir = os.path.join(os.path.dirname(corrupted_folder_path), 'Repaired')

        self.worker = VideoRepairWorker(reference_file_path, encrypted_files, output_dir, file_type)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.log_updated.connect(self.update_log)
        self.worker.repair_finished.connect(self.repair_finished)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(int(value))

    def update_log(self, message):
        self.log_box.append(message)

    def repair_finished(self, message):
        self.show_message("Success", message)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def closeEvent(self, event):
        if hasattr(self, 'worker') and self.worker.isRunning():
            event.ignore()
            self.show_message("Error", "Cannot close the application while repair process is running.")
        else:
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoRepairApp()
    window.show()
    sys.exit(app.exec())
