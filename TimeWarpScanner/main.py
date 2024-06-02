import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, \
    QWidget, QLineEdit, QRadioButton, QButtonGroup, QSlider, QFormLayout
from PyQt5.QtCore import Qt
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

        # 방향 선택 라디오 버튼 그룹
        direction_layout = QFormLayout()
        self.button_group = QButtonGroup(self)

        self.radio_left = QRadioButton("Left to Right")
        self.radio_right = QRadioButton("Right to Left")
        self.radio_top = QRadioButton("Top to Bottom")
        self.radio_bottom = QRadioButton("Bottom to Top")

        self.button_group.addButton(self.radio_left)
        self.button_group.addButton(self.radio_right)
        self.button_group.addButton(self.radio_top)
        self.button_group.addButton(self.radio_bottom)

        direction_layout.addRow("Direction:", self.radio_left)
        direction_layout.addRow("", self.radio_right)
        direction_layout.addRow("", self.radio_top)
        direction_layout.addRow("", self.radio_bottom)

        main_layout.addLayout(direction_layout)

        # 라인 스피드 슬라이더
        speed_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.setValue(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)

        speed_layout.addWidget(QLabel("Line Speed:"))
        speed_layout.addWidget(self.slider)

        main_layout.addLayout(speed_layout)

        # 변환 버튼
        convert_button = QPushButton("Convert File")
        convert_button.clicked.connect(self.convert_file)
        main_layout.addWidget(convert_button)

        # 파일 이름 입력 및 경로 선택 레이아웃
        save_layout = QFormLayout()
        self.save_name_edit = QLineEdit()
        self.save_path_edit = QLineEdit()

        save_browse_button = QPushButton("Browse...")
        save_browse_button.clicked.connect(self.browse_save_path)

        save_path_layout = QHBoxLayout()
        save_path_layout.addWidget(self.save_path_edit)
        save_path_layout.addWidget(save_browse_button)

        save_layout.addRow("File Name:", self.save_name_edit)
        save_layout.addRow("Save Path:", save_path_layout)

        main_layout.addLayout(save_layout)

        # 확장자 선택 라디오 버튼 그룹
        extension_layout = QHBoxLayout()
        self.extension_group = QButtonGroup(self)

        self.radio_mp4 = QRadioButton("mp4")
        self.radio_avi = QRadioButton("avi")
        self.radio_custom = QRadioButton("Custom")

        self.extension_group.addButton(self.radio_mp4)
        self.extension_group.addButton(self.radio_avi)
        self.extension_group.addButton(self.radio_custom)

        self.radio_mp4.setChecked(True)  # 기본값으로 mp4 선택

        self.custom_extension_edit = QLineEdit()
        self.custom_extension_edit.setEnabled(False)

        def toggle_custom_extension():
            self.custom_extension_edit.setEnabled(self.radio_custom.isChecked())

        self.radio_custom.toggled.connect(toggle_custom_extension)

        extension_layout.addWidget(QLabel("Extension:"))
        extension_layout.addWidget(self.radio_mp4)
        extension_layout.addWidget(self.radio_avi)
        extension_layout.addWidget(self.radio_custom)
        extension_layout.addWidget(self.custom_extension_edit)

        main_layout.addLayout(extension_layout)

        # 저장 버튼
        save_file_button = QPushButton("Save File")
        save_file_button.clicked.connect(self.save_file)
        main_layout.addWidget(save_file_button)

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

    def browse_save_path(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)
        if directory:
            self.save_path_edit.setText(directory)

    def convert_file(self):
        if self.selected_file_path:
            self.path_edit.setText("Converting file...")
            output_path = self.selected_file_path.replace('.mp4', '_converted.avi')

            direction = self.get_selected_direction()
            line_speed = self.slider.value()

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

    def get_selected_direction(self):
        if self.radio_left.isChecked():
            return 'left'
        elif self.radio_right.isChecked():
            return 'right'
        elif self.radio_top.isChecked():
            return 'top'
        elif self.radio_bottom.isChecked():
            return 'bottom'
        else:
            return None

    def get_selected_extension(self):
        if self.radio_mp4.isChecked():
            return "mp4"
        elif self.radio_avi.isChecked():
            return "avi"
        elif self.radio_custom.isChecked():
            return self.custom_extension_edit.text()
        else:
            return None

    def save_file(self):
        if self.converted_data:
            save_path = self.save_path_edit.text()
            file_name = self.save_name_edit.text()
            extension = self.get_selected_extension()
            if save_path and file_name and extension:
                full_save_path = f"{save_path}/{file_name}.{extension}"
                with open(full_save_path, 'wb') as file:
                    with open(self.converted_data, 'rb') as converted_file:
                        file.write(converted_file.read())
                self.path_edit.setText(f"File saved to: {full_save_path}")
            else:
                self.path_edit.setText("Save path, file name, or extension is missing.")
        else:
            self.path_edit.setText("No converted data to save.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(500, 400)
    window.show()
    sys.exit(app.exec_())
