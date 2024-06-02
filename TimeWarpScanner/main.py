import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, \
    QWidget, QLineEdit
from scanner.left_to_right_scanner import LeftToRightScanner
from scanner.right_to_left_scanner import RightToLeftScanner
from scanner.top_to_bottom_scanner import TopToBottomScanner
from scanner.bottom_to_top_scanner import BottomToTopScanner


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Loader and Saver")

        main_layout = QVBoxLayout()

        path_layout = QHBoxLayout()

        self.path_edit = QLineEdit()
        path_layout.addWidget(self.path_edit)

        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_file)
        path_layout.addWidget(browse_button)

        main_layout.addLayout(path_layout)

        button_layout = QHBoxLayout()

        convert_button = QPushButton("Convert File")
        convert_button.clicked.connect(self.convert_file)
        button_layout.addWidget(convert_button)

        save_file_button = QPushButton("Save File")
        save_file_button.clicked.connect(self.save_file)
        button_layout.addWidget(save_file_button)

        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.selected_file_path = None
        self.converted_data = None

    def browse_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if file_path:
            self.path_edit.setText(file_path)
            self.selected_file_path = file_path

    def convert_file(self):
        if self.selected_file_path:
            self.path_edit.setText("Converting file...")
            output_path = self.selected_file_path.replace('.mp4', '_converted.avi')

            direction = 'left'  # 예시로 방향을 지정, 실제로는 UI에서 받아야 함
            line_speed = 1  # 예시로 속도를 지정, 실제로는 UI에서 받아야 함

            if direction == 'left':
                scanner = LeftToRightScanner(self.selected_file_path, line_speed)
            elif direction == 'right':
                scanner = RightToLeftScanner(self.selected_file_path, line_speed)
            elif direction == 'top':
                scanner = TopToBottomScanner(self.selected_file_path, line_speed)
            elif direction == 'bottom':
                scanner = BottomToTopScanner(self.selected_file_path, line_speed)

            scanner.convert(output_path)
            self.converted_data = output_path
            self.path_edit.setText("File converted. Ready to save.")
        else:
            self.path_edit.setText("No file selected for conversion.")

    def save_file(self):
        if self.converted_data:
            options = QFileDialog.Options()
            save_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)", options=options)
            if save_path:
                with open(save_path, 'wb') as file:
                    with open(self.converted_data, 'rb') as converted_file:
                        file.write(converted_file.read())
                self.path_edit.setText(f"File saved to: {save_path}")
        else:
            self.path_edit.setText("No converted data to save.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(500, 100)
    window.show()
    sys.exit(app.exec_())
