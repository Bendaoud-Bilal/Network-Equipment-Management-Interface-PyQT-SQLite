import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import *
from PyQt5.QtCore import QDateTime
import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDate, QTime, QDateTime




ICON_PATH = "icon/"  # Update if your icon path is different


class AddWilayaDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Add New Wilaya")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Wilaya Code")
        layout.addWidget(self.code_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Wilaya Name")
        layout.addWidget(self.name_input)

        self.submit_btn = QPushButton("Add Wilaya")
        self.submit_btn.clicked.connect(self.add_wilaya)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def add_wilaya(self):
        code = self.code_input.text()
        name = self.name_input.text()
        if not code or not name:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        try:
            conn = sqlite3.connect("database.db")
            conn.execute("INSERT INTO wilaya VALUES (?, ?)", (code, name))
            conn.commit()
            QMessageBox.information(self, "Success", "Wilaya added successfully!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")


class AddEquipmentTypeDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Add New Equipment Type")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Type Code")
        layout.addWidget(self.code_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Type Name")
        layout.addWidget(self.name_input)

        self.submit_btn = QPushButton("Add Type")
        self.submit_btn.clicked.connect(self.add_type)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def add_type(self):
        code = self.code_input.text()
        name = self.name_input.text()
        if not code or not name:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        try:
            conn = sqlite3.connect("database.db")
            conn.execute("INSERT INTO equipment_type VALUES (?, ?)", (code, name))
            conn.commit()
            QMessageBox.information(
                self, "Success", "Equipment type added successfully!"
            )
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")




class EquipmentDialog(QDialog):
    def __init__(self, equipment_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.equipment_id = equipment_id
        self.setWindowTitle("Add Equipment" if not equipment_id else "Update Equipment")
        self.setFixedSize(400, 500)

        layout = QFormLayout()

        # Existing fields
        self.description = QLineEdit()
        self.ipv4_decimal = QLineEdit()
        self.ipv4_binary = QLineEdit()
        self.ipv6_decimal = QLineEdit()
        self.ipv6_binary = QLineEdit()

        # Date/Time inputs as separate fields in the form layout
        self.day_input = QLineEdit()
        self.day_input.setPlaceholderText("Day (1-31)")
        layout.addRow("Day:", self.day_input)
        
        self.month_input = QLineEdit()
        self.month_input.setPlaceholderText("Month (1-12)")
        layout.addRow("Month:", self.month_input)
        
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Year (YYYY)")
        layout.addRow("Year:", self.year_input)
        
        self.hour_input = QLineEdit()
        self.hour_input.setPlaceholderText("Hour (0-23)")
        layout.addRow("Hour:", self.hour_input)

        # Add all other widgets to layout
        layout.addRow("Description:", self.description)
        layout.addRow("IPv4 Decimal:", self.ipv4_decimal)
        layout.addRow("IPv4 Binary:", self.ipv4_binary)
        layout.addRow("IPv6 Decimal:", self.ipv6_decimal)
        layout.addRow("IPv6 Binary:", self.ipv6_binary)

        # Comboboxes
        self.wilaya_combo = QComboBox()
        self.load_wilayas()
        layout.addRow("Wilaya:", self.wilaya_combo)

        self.type_combo = QComboBox()
        self.load_types()
        layout.addRow("Type:", self.type_combo)

        # Submit Button
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.save_equipment)
        layout.addRow(self.submit_btn)

        self.setLayout(layout)

        if equipment_id:
            self.load_equipment_data()
        else:
            self.set_current_datetime()

    # The rest of the methods remain unchanged
    def set_current_datetime(self):
        """Set default values to current date/time"""
        now = QDateTime.currentDateTime()
        self.day_input.setText(str(now.date().day()))
        self.month_input.setText(str(now.date().month()))
        self.year_input.setText(str(now.date().year()))
        self.hour_input.setText(str(now.time().hour()))

    def validate_datetime(self):
        """Validate date/time inputs and return QDateTime if valid"""
        try:
            day = int(self.day_input.text())
            month = int(self.month_input.text())
            year = int(self.year_input.text())
            hour = int(self.hour_input.text())

            if not (1 <= day <= 31):
                raise ValueError("Day must be between 1-31")
            if not (1 <= month <= 12):
                raise ValueError("Month must be between 1-12")
            if not (0 <= hour <= 23):
                raise ValueError("Hour must be between 0-23")

            date = QDate(year, month, day)
            if not date.isValid():
                raise ValueError("Invalid date combination")

            time = QTime(hour, 0)  # Minutes set to 0
            if not time.isValid():
                raise ValueError("Invalid time")

            return QDateTime(date, time)

        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))
            return None

    def load_wilayas(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.execute("SELECT code_wilaya, wilaya_name FROM wilaya")
        for code, name in cursor:
            self.wilaya_combo.addItem(f"{code} - {name}", code)
        conn.close()

    def load_types(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.execute("SELECT code_type, type_name FROM equipment_type")
        for code, name in cursor:
            self.type_combo.addItem(f"{code} - {name}", code)
        conn.close()

    def load_equipment_data(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.execute(
            "SELECT * FROM equipment WHERE id_equipment=?", (self.equipment_id,)
        )
        equipment = cursor.fetchone()
        conn.close()

        if equipment:
            # Load basic fields
            self.description.setText(equipment[1])
            self.ipv4_decimal.setText(equipment[2])
            self.ipv4_binary.setText(equipment[3])
            self.ipv6_decimal.setText(equipment[4])
            self.ipv6_binary.setText(equipment[5])

            # Parse and load date/time
            dt = QDateTime.fromString(equipment[6], "yyyy-MM-dd hh:mm:ss")
            if dt.isValid():
                self.day_input.setText(str(dt.date().day()))
                self.month_input.setText(str(dt.date().month()))
                self.year_input.setText(str(dt.date().year()))
                self.hour_input.setText(str(dt.time().hour()))

            # Load comboboxes
            self.wilaya_combo.setCurrentIndex(
                self.wilaya_combo.findData(equipment[7])
            )
            self.type_combo.setCurrentIndex(
                self.type_combo.findData(equipment[8])
            )

    def save_equipment(self):
        # Validate all fields
        required_fields = [
            self.description.text().strip(),
            self.ipv4_decimal.text().strip(),
            self.ipv4_binary.text().strip(),
            self.ipv6_decimal.text().strip(),
            self.ipv6_binary.text().strip()
        ]

        if any(not field for field in required_fields):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        # Validate date/time
        datetime = self.validate_datetime()
        if not datetime:
            return

        # Prepare data
        data = (
            *required_fields,
            datetime.toString("yyyy-MM-dd hh:mm:ss"),
            self.wilaya_combo.currentData(),
            self.type_combo.currentData()
        )

        # Database operations
        try:
            conn = sqlite3.connect("database.db")
            if self.equipment_id:
                conn.execute(
                    """UPDATE equipment SET
                    description=?, address_IPV4_decimal=?, address_IPV4_binary=?,
                    address_IPV6_decimal=?, address_IPV6_binary=?, start_serving_date=?,
                    code_wil=?, code_t=? WHERE id_equipment=?""",
                    data + (self.equipment_id,)
                )
            else:
                conn.execute(
                    """INSERT INTO equipment
                    (description, address_IPV4_decimal, address_IPV4_binary,
                    address_IPV6_decimal, address_IPV6_binary, start_serving_date,
                    code_wil, code_t)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    data
                )
            conn.commit()
            QMessageBox.information(self, "Success", "Equipment saved successfully!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")
        finally:
            conn.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Equipment Management")
        self.setMinimumSize(800, 600)

        # Initialize database
        self.init_db()

        # Create UI
        self.table = QTableWidget()
        self.setCentralWidget(self.table)
        self.setup_table()
        self.create_menu()
        self.create_toolbar()

        self.load_data()

    def init_db(self):
        conn = sqlite3.connect("database.db")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS wilaya (
            code_wilaya INTEGER PRIMARY KEY,
            wilaya_name VARCHAR(100) NOT NULL)"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS equipment_type (
            code_type INTEGER PRIMARY KEY,
            type_name VARCHAR(150) NOT NULL)"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS equipment (
            id_equipment INTEGER PRIMARY KEY,
            description VARCHAR(1000),
            address_IPV4_decimal VARCHAR(20),
            address_IPV4_binary VARCHAR(40),
            address_IPV6_decimal VARCHAR(40),
            address_IPV6_binary VARCHAR(140),
            start_serving_date TIMESTAMP,
            code_wil INTEGER,
            code_t INTEGER,
            FOREIGN KEY (code_wil) REFERENCES wilaya (code_wilaya),
            FOREIGN KEY (code_t) REFERENCES equipment_type (code_type))"""
        )
        conn.close()

    def setup_table(self):
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Description",
                "IPv4 Decimal",
                "IPv4 Binary",
                "IPv6 Decimal",
                "IPv6 Binary",
                "Start Date",
                "Wilaya",
                "Type",
                "Actions",
            ]
        )
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def create_menu(self):
        menu = self.menuBar()

        # Equipment menu
        equipment_menu = menu.addMenu("&Equipment")
        equipment_menu.addAction("Add New", self.add_equipment)

        # Configuration menu
        config_menu = menu.addMenu("&Configuration")
        config_menu.addAction("Add Wilaya", lambda: AddWilayaDialog().exec_())
        config_menu.addAction(
            "Add Equipment Type", lambda: AddEquipmentTypeDialog().exec_()
        )

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Add buttons to the toolbar
        toolbar.addAction("Add Equipment", self.add_equipment)
        toolbar.addAction("Refresh", self.load_data)

        # Add new buttons for showing wilayas and equipment types
        toolbar.addAction("Show Wilayas", self.show_wilayas)
        toolbar.addAction("Show Equipment Types", self.show_equipment_types)

        # Search input field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by description, wilaya, or type")
        self.search_input.textChanged.connect(self.search_equipment)
        toolbar.addWidget(self.search_input)

    def add_equipment(self):
        dialog = EquipmentDialog()
        dialog.exec_()
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        conn = sqlite3.connect("database.db")
        query = """SELECT e.*, w.wilaya_name, t.type_name 
                FROM equipment e
                LEFT JOIN wilaya w ON e.code_wil = w.code_wilaya
                LEFT JOIN equipment_type t ON e.code_t = t.code_type"""
        cursor = conn.execute(query)

        for row_idx, row in enumerate(cursor):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row[:9]):  # Exclude FK codes
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            # Add action buttons
            btn_edit = QPushButton("Edit")
            btn_edit.clicked.connect(lambda _, id=row[0]: self.edit_equipment(id))

            btn_delete = QPushButton("Delete")
            btn_delete.clicked.connect(lambda _, id=row[0]: self.delete_equipment(id))

            cell_widget = QWidget()
            layout = QHBoxLayout(cell_widget)
            layout.addWidget(btn_edit)
            layout.addWidget(btn_delete)
            self.table.setCellWidget(row_idx, 9, cell_widget)

        conn.close()

    def edit_equipment(self, equipment_id):
        dialog = EquipmentDialog(equipment_id)
        dialog.exec_()
        self.load_data()

    def delete_equipment(self, equipment_id):
        confirm = QMessageBox.question(
            self, "Confirm Delete", "Are you sure you want to delete this equipment?"
        )
        if confirm == QMessageBox.Yes:
            conn = sqlite3.connect("database.db")
            conn.execute("DELETE FROM equipment WHERE id_equipment=?", (equipment_id,))
            conn.commit()
            conn.close()
            self.load_data()

    def search_equipment(self):
        query = f"%{self.search_input.text()}%"
        self.table.setRowCount(0)
        conn = sqlite3.connect("database.db")
        cursor = conn.execute(
            """SELECT e.*, w.wilaya_name, t.type_name 
                              FROM equipment e
                              LEFT JOIN wilaya w ON e.code_wil = w.code_wilaya
                              LEFT JOIN equipment_type t ON e.code_t = t.code_type
                              WHERE e.description LIKE ? 
                              OR w.wilaya_name LIKE ? 
                              OR t.type_name LIKE ?""",
            (query, query, query),
        )

        for row_idx, row in enumerate(cursor):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row[:9]):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            # Action buttons (same as in load_data)
            btn_edit = QPushButton("Edit")
            btn_edit.clicked.connect(lambda _, id=row[0]: self.edit_equipment(id))

            btn_delete = QPushButton("Delete")
            btn_delete.clicked.connect(lambda _, id=row[0]: self.delete_equipment(id))

            cell_widget = QWidget()
            layout = QHBoxLayout(cell_widget)
            layout.addWidget(btn_edit)
            layout.addWidget(btn_delete)
            self.table.setCellWidget(row_idx, 9, cell_widget)

        conn.close()

    def show_wilayas(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.execute("SELECT code_wilaya, wilaya_name FROM wilaya ORDER BY code_wilaya")
        wilayas = cursor.fetchall()
        conn.close()

        page_size = 20
        total_pages = (len(wilayas) + page_size - 1) // page_size
        current_page = 0

        def update_display():
            start = current_page * page_size
            end = start + page_size
            page_wilayas = wilayas[start:end]
            text = "\n".join(f"{code} - {name}" for code, name in page_wilayas)
            text_display.setPlainText(text)
            page_label.setText(f"Page {current_page + 1} of {total_pages}")
            prev_button.setEnabled(current_page > 0)
            next_button.setEnabled(current_page < total_pages - 1)

        dialog = QDialog(self)
        dialog.setWindowTitle("Wilayas Database")
        dialog.setMinimumSize(400, 500)

        layout = QVBoxLayout()
        text_display = QTextEdit()
        text_display.setReadOnly(True)

        nav_layout = QHBoxLayout()
        page_label = QLabel()
        prev_button = QPushButton("Previous")
        next_button = QPushButton("Next")

        def prev_page():
            nonlocal current_page
            current_page -= 1
            update_display()

        def next_page():
            nonlocal current_page
            current_page += 1
            update_display()

        prev_button.clicked.connect(prev_page)
        next_button.clicked.connect(next_page)

        nav_layout.addWidget(prev_button)
        nav_layout.addWidget(page_label)
        nav_layout.addWidget(next_button)

        layout.addWidget(text_display)
        layout.addLayout(nav_layout)
        dialog.setLayout(layout)

        update_display()
        dialog.exec_()


    def show_equipment_types(self):  # Moved inside MainWindow class
        conn = sqlite3.connect("database.db")
        cursor = conn.execute("SELECT code_type, type_name FROM equipment_type ORDER BY code_type")
        types = cursor.fetchall()
        conn.close()

        page_size = 20
        total_pages = (len(types) + page_size - 1) // page_size
        current_page = 0

        def update_display():
            start = current_page * page_size
            end = start + page_size
            page_types = types[start:end]
            text = "\n".join(f"Code: {code}, Type: {name}" for code, name in page_types)
            text_display.setPlainText(text)
            page_label.setText(f"Page {current_page + 1} of {total_pages}")
            prev_button.setEnabled(current_page > 0)
            next_button.setEnabled(current_page < total_pages - 1)

        dialog = QDialog(self)
        dialog.setWindowTitle("Equipment Types")
        dialog.setMinimumSize(400, 500)

        layout = QVBoxLayout()
        text_display = QTextEdit()
        text_display.setReadOnly(True)

        nav_layout = QHBoxLayout()
        page_label = QLabel()
        prev_button = QPushButton("Previous")
        next_button = QPushButton("Next")

        def prev_page():
            nonlocal current_page
            current_page -= 1
            update_display()

        def next_page():
            nonlocal current_page
            current_page += 1
            update_display()

        prev_button.clicked.connect(prev_page)
        next_button.clicked.connect(next_page)

        nav_layout.addWidget(prev_button)
        nav_layout.addWidget(page_label)
        nav_layout.addWidget(next_button)

        layout.addWidget(text_display)
        layout.addLayout(nav_layout)
        dialog.setLayout(layout)

        update_display()
        dialog.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
