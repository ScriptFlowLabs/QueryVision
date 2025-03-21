import sys

from PyQt5.QtCore import Qt, QRegularExpression
from PyQt5.QtGui import QFont, QKeySequence, QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QTextEdit, QAction, QFrame,
    QDialog, QLabel, QLineEdit, QFormLayout, QPushButton, QWidget, QStyle,
    QTableWidget, QFileDialog, QHBoxLayout, QShortcut, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QTableWidgetItem, QVBoxLayout
)

import webbrowser
import mysql.connector as sql

main_window_style_sheet = '''
/* General Window Styles */
QMainWindow {
    background-color: #0f0f1f;
    border: none;
}

QDialog {
    background-color: #0f0f1f;
    border: 2px solid #58a6ff;
}

/* Label Styles */
QLabel {
    color: #00ffcc;
    font-family: "Consolas", monospace;
    font-size: 14px;
}

/* Line Edit Styles */
QLineEdit {
    background-color: #161b22;
    border-top-left-radius:12px;
    border-top-right-radius:0px;
    border-bottom-right-radius:0px;
    color: #c9d1d9;
    padding: 5px;
    font-family: "Consolas", monospace;
    font-size: 14px;
}

/* Button Styles */
QPushButton {
    background-color: #00ccff;
    color: #000000;
    border: 2px solid #0033ff;
    padding: 10px;
    font-size: 14px;
    font-family: 'Orbitron', Arial, sans-serif;
    font-weight: bold;
    border-radius: 8px;
    height: 35px;
}
QPushButton:hover {
    background-color: #00ffcc;
    border: 1px solid white;
}
QPushButton:pressed {
    background-color: #00aaff;
    border: 1px solid white;
}

/* Form Layout Styles */
QFormLayout {
    background-color: transparent;
    margin: 10px;
    padding: 10px;
}

/* Text Edit Styles */
QTextEdit {
    background-color: #1f1f3f;
    color: #00ffcc;
    border: 2px solid #00c8ff;
    border-radius: 12px;
    padding: 10px;
    font-family: "Consolas", monospace;
    font-size: 14px;
}

/* Tab Widget Styles */
QTabWidget::pane {
    background-color: #0f0f1f;
    border-radius: 8px;
}
QTabBar::tab {
    background-color: #161b22;
    color: #00ffcc;
    border: 2px solid #00c8ff;
    border-radius: 4px;
    padding-left: 5px;
    padding-right: 5px;
    min-height: 25px;
    margin:4px;
}
QTabBar::tab:selected {
    background-color: #00c8ff;
    color: #0f0f1f;
}
QTabBar::tab:hover {
    background-color: #00ffcc;
    color: #0f0f1f;
}

/* Dock Widget Styles */
QDockWidget {
    background-color: #1a1a2e;
    color: white;
    border: 2px solid #00c8ff;
    border-radius: 15px;
    padding: 5px;
}
QDockWidget::title {
    background-color: #101028;
    color: #00ffcc;
    padding: 10px;
    font-size: 10px;
    border-radius: 3px;
    border: 1px solid #00ccff;
}

/* Menu Bar Styles */
QMenuBar {
    background-color: #101028;
    color: #00ffcc;
    border: none;
    padding: 5px;
    font-family: "Consolas", monospace;
    font-size: 14px;
}
QMenuBar::item {
    background-color: #101028;
    color: #00ffcc;
    padding: 5px;
    border-radius: 3px;
}
QMenuBar::item:selected {
    background-color: #00ffcc;
    color: #000000;
}
QMenuBar::item:hover {
    background-color: #0066ff;
    color: #ffffff;
}
QMenu {
    background-color: #0f0f1f;
    border: 2px solid #00ffcc;
    padding: 5px;
    border-radius: 5px;
}
QMenu::item {
    color: #ffffff;
    padding: 8px;
    font-size: 14px;
    border-radius: 3px;
}
QMenu::item:selected {
    background-color: #00ffcc;
    color: #000000;
}
QMenu::item:hover {
    background-color: #0066ff;
    color: #ffffff;
}

/* Tree Widget Styles */
QTreeWidget {
    background-color: #1f1f3f;
    alternate-background-color: #101028;
    color: #00ffcc;
    border: 2px solid #00c8ff;
    border-radius: 12px;
    font-family: "Consolas", monospace;
    font-size: 14px;
    outline: 0;
}

QTreeWidget::item {
    padding: 6px;
    margin: 2px;
    border-radius: 8px;
}
QTreeWidget::item:selected {
    background-color: #00ccff;
    color: #000000;
    border: 1px solid #00ffcc;
}
QTreeWidget::item:hover {
    background-color: #0066ff;
    color: #ffffff;
}

/* Table Widget Styles */
QTableWidget {
    background-color: #1f1f3f;
    border: 2px solid #00c8ff;
    border-radius: 12px;
    color: #00ffcc;
    font-family: "Consolas", monospace;
    font-size: 14px;
    alternate-background-color: #101028;
}
QTableWidget::item {
    border: 1px solid #00ccff;
}
QTableWidget::item:alternate {
    background-color: #000;
}
QTableWidget::item:selected {
    background-color: #00ccff;
    color: #000;
}
QTableWidget::item:hover {
    background-color: #0066ff;
    color: #ffffff;
}
QTableWidget::horizontalHeader {
    background-color: #1f1f3f;
}

/* Header View Styles */
QHeaderView {
    background-color: #101028;
    color: #00ffcc;
}
QHeaderView::section {
    background-color: #101028;
    color: #00ffcc;
    font: bold 14px "Consolas";
    border: 1px solid #00c8ff;
    padding: 5px;
    margin: 2px;
}
QHeaderView::section:horizontal {
    background-color: #101028;
}
QHeaderView::section:vertical {
    background-color: #101028;
    color: #00ffcc;
    border-right: 0px solid #00c8ff;
}
QTableCornerButton::section {
    background-color: #101028;
}
'''

dialogue_window_style_sheet = style="""
QDialog {
    background-color: #0f0f1f;
    border: 2px solid #58a6ff;
}
QLabel {
    color: #00ffcc;
    font-family: "Consolas", monospace;
    font-size: 14px;
}
QLineEdit {
    background-color: #161b22;  
    border: 1px solid #00c8ff;  
    color: #c9d1d9; 
    padding: 5px;
    font-family: "Consolas", monospace;
    font-size: 14px;
    border-radius: 5px;
}
QPushButton {
    background-color: #58a6ff;
    color: #0d1117;
    border: 1px solid white;
    border-radius: 5px;
    font-size: 14px;
    font-family: 'Orbitron', Arial, sans-serif;
    height: 35px;
}
QPushButton:hover {
    background-color: #00ffcc;
    border: 1px solid white; 
}
QPushButton:pressed {
    background-color: #00aaff;  
    border: 1px solid white;
}
QFormLayout {
    background-color: transparent;
    margin: 10px;
    padding: 10px;
}
"""

title_bar_style_sheet = '''
QWidget {
    background-color: #101028;
    border: 1px solid #00ccff;
    border-radius: 3px;
}
QLabel {
    border: none;
    color: #00ffcc;
    font-size: 14px;
    padding: 5px;
}
QPushButton {
    background-color: transparent;
    color: #00ffcc;
    font-size: 16px;
    border: none;
    padding: 2px;
}
QPushButton:hover {
    color: #ffffff;
}
'''

info = """\
Author: V & M Team
Studio: Script Flow
Version: 1.0.0 (Unstable)
Description: SQL IDLE
(Integrated Development Learning Environment)\
"""

tips = """\
#This Software Uses semicolon to split queries.
#Comments might not work as expected when it contains a semicolon.
#Relauch the application if some error is recurring\
"""

keywords = [
"CREATE", "ALTER", "DROP", "RENAME", "TRUNCATE", "COMMENT",
"SELECT", "INSERT", "UPDATE", "DELETE", "MERGE", "CALL",
"WHERE", "FROM", "JOIN", "ON", "USING", "IN", "AND", "OR", "NOT", "LIKE",
"BETWEEN", "GROUP BY", "ORDER BY", "HAVING", "LIMIT", "DISTINCT",
"VALUES", "SET", "INTO", "AS", "WITH", "PARTITION BY", "WINDOW",
"FETCH", "OFFSET", "USE", "ASC", "DESC",
"EXISTS", "IS", "NULL", "TRUE", "FALSE", "ANY", "ALL", "SOME",
"COUNT", "SUM", "AVG", "MIN", "MAX",
"LOWER", "UPPER", "SUBSTRING", "POSITION", "TRIM", "CONCAT",
"COALESCE", "NULLIF", "CAST", "CONVERT",
"CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP", "EXTRACT",
"DATE_ADD", "DATE_SUB", "DATEDIFF", "NOW", "SYSDATE",
"CHAR", "VARCHAR", "TEXT", "BLOB", "INT", "INTEGER", "BIGINT",
"SMALLINT", "DECIMAL", "NUMERIC", "FLOAT", "DOUBLE", "DATE",
"TIME", "DATETIME", "TIMESTAMP", "BOOLEAN",
"INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN",
"CROSS JOIN", "NATURAL JOIN",
"UNION", "UNION ALL", "INTERSECT", "EXCEPT", "CASE", "WHEN",
"THEN", "ELSE", "END", "DEFAULT", "PRIMARY KEY", "FOREIGN KEY",
"REFERENCES", "CHECK", "CONSTRAINT", "INDEX", "AUTO_INCREMENT",
"SEQUENCE", "ANALYZE", "CLUSTER", "VACUUM", "OPTIMIZE"
]

class SQLSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Keyword format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FF5733"))  # Orange
        keyword_format.setFontWeight(QFont.Bold)

        for keyword in keywords:
            pattern = f"\\b{keyword}\\b"
            self.highlighting_rules.append((pattern, keyword_format))

        # String format
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#2ECC71"))  # Green
        self.highlighting_rules.append((r'".*?"', string_format))
        self.highlighting_rules.append((r"'.*?'", string_format))

        # Comment format
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#AAAAAA"))  # Gray
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((r"--[^\n]*", comment_format))

        block_comment_format = QTextCharFormat()
        block_comment_format.setForeground(QColor("#AAAAAA"))  # Gray
        block_comment_format.setFontItalic(True)
        self.highlighting_rules.append((r"/\*[^*]*\*+(?:[^/*][^*]*\*+)*/", block_comment_format))

        # Number format
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#3498DB"))  # Blue
        self.highlighting_rules.append((r"\b\d+\b", number_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            expression.setPatternOptions(QRegularExpression.CaseInsensitiveOption)
            match = expression.globalMatch(text)
            while match.hasNext():
                current_match = match.next()
                start = current_match.capturedStart()
                length = current_match.capturedLength()
                self.setFormat(start, length, fmt)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Query Vision")
        self.resize(1000, 700)

        self.setStyleSheet(main_window_style_sheet)

        self.create_menubar()
        #self.create_statusbar()

        self.left_dock_widgets = []
        self.right_dock_widgets = []
        self.LIW= [] # left_inner_widgets
        self.RIW = [] #right_inner_widgets
        self.create_dock_widgets()
        self.create_help()

        self.LIW[0].header().setHidden(True)
       
        self.tabcount = 1

        self.RIW[0].addTab(QTextEdit(), f'File {self.tabcount}')
        self.RIW[0].tabBar().setFont(QFont("Consolas", 12))
        self.RIW[0].currentChanged.connect(self.switch_highlighting)

        self.sql_editor = self.RIW[0].currentWidget()
        self.syntax_highlighter = SQLSyntaxHighlighter(self.sql_editor.document())

        shortcut = QShortcut(QKeySequence("F11"), self)
        shortcut.activated.connect(self.toggle_fullscreen)

        self.conn = None
        self.cursor = None

        self.show()
        
    def create_help(self):
        self.LIW[1].setStyleSheet('''QFrame{
                                        border:2px solid #00c8ff;
                                        border-radius:12px;}
                                  
                                  QTextEdit{
                                        border-left:0px;
                                        border-right:0px;
                                        border-bottom:0px;
                                        border-top:2px solid #00c8ff;
                                        border-top-left-radius:0px;
                                        border-top-right-radius:0px;}
                                  
                                  QPushButton{
                                        border:0px;
                                        height:10px;
                                        border-bottom-left-radius:0px;
                                        border-top-left-radius:0px;
                                        border-bottom-right-radius:0px;
                                  }
                                  ''')

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        self.LIW[1].setLayout(main_layout)

        inner_layout = QHBoxLayout()
        search_edit =  QLineEdit()

        self.search_text = QTextEdit()
        self.search_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.search_text.setReadOnly(True)

        search_button = QPushButton('search')
        search_button.clicked.connect(lambda: self.search(search_edit.text()))

        main_layout.addLayout(inner_layout)

        inner_layout.addWidget(search_edit)
        inner_layout.addWidget(search_button)
        main_layout.addWidget(self.search_text)

        main_layout.setStretch(1,10)

    def on_connect(self, host, user, password, db_name=None, win=None):
        if self.conn:

            self.cursor.close()
            self.conn.close()
            self.conn = None
            self.cursor = None
            self.LIW[0].clear()
            print("Previous connection closed.")

        try:
            self.conn = sql.connect(
                host=host,
                user=user,
                passwd=password,
                db=db_name,
                use_pure=True
            )
            
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                if win: win.close()
                self.connection_status_label.setStyleSheet("QLabel {color: #00ffcc;font-size: 18px;}")
                self.update_database_tree()
            else:
                self.show_error_message("Connection unsuccessful. Please check your credentials.")
                self.connection_status_label.setStyleSheet("QLabel {color: #ff0000;font-size: 18px;}")

        except sql.Error as e:
            self.show_error_message(f"Error: {e}")
            self.connection_status_label.setStyleSheet("QLabel {color: #ff0000;font-size: 18px;}")

    def db_action(self, dbname, win, action):
        if self.conn and dbname:
            try:
                self.cursor.execute(f'{action} database {dbname}')
                self.update_database_tree()
            except sql.Error as e:
                self.show_error_message(str(e))
            win.close()
        
        elif not self.conn:
            self.open_con_win(title='Connect to Sql First!')
        
        else: 
            self.show_error_message("Enter a valid name")
    
    def switch_highlighting(self, index):
        if index != -1:
            current_widget = self.RIW[0].widget(index)  
            self.syntax_highlighter = SQLSyntaxHighlighter(current_widget.document())

    def search(self, content):
        if self.conn:
            self.cursor.execute('use mysql')
            self.cursor.execute(f'select description from help_topic where name like "{content}%"')
            data = self.cursor.fetchall()
            self.search_text.setText(data[0][0])

    def save_file(self):
        save_location = QFileDialog.getSaveFileName(self, 'Save File', '', 'MV Query Files (*.mv)')[0]
        if save_location:
            with open(save_location, mode = 'w') as file:
                tab_index = self.RIW[0].currentIndex()
                query = self.RIW[0].widget(tab_index)
                file.write(query.toPlainText())
                
            # to update file name
            full_file_name = save_location.split('/')[-1]
            only_file_name = full_file_name.split('.')[0]
            self.RIW[0].setTabText(tab_index, only_file_name)

    def open_file(self):
        open_location = QFileDialog.getOpenFileName(None, 'Open File', '', 'MV Query Files (*.mv)')[0]
        textbox = QTextEdit()
        if open_location:
            with open(open_location, mode = 'r') as file:
                query = file.read()
                textbox.setText(query)
            
            full_file_name = open_location.split('/')[-1]
            only_file_name = full_file_name.split('.')[0]
            self.RIW[0].addTab(textbox, only_file_name)
            tab_index = self.RIW[0].indexOf(textbox)
            self.RIW[0].setCurrentIndex(tab_index)

    def new_file(self):
        self.tabcount += 1
        textbox = QTextEdit()
        self.RIW[0].addTab(textbox, f'File {self.tabcount}')
        tab_index = self.RIW[0].indexOf(textbox)
        self.RIW[0].setCurrentIndex(tab_index)

    def close_file(self):
        current_index = self.RIW[0].currentIndex()
        self.RIW[0].removeTab(current_index)
        if not self.RIW[0].count():
            self.tabcount = 0
    
    def execute_query(self):
        if not self.cursor:
            self.open_con_win(title='Connect to Sql before executing')
            return
        rows = self.RIW[0].currentWidget().toPlainText().split(';')
        rows.pop() # remove the last empty string
        print(rows)
        for row in rows:
    
            try:
                self.cursor.execute(row)
                # updates currently open table
                db_nav_selected_item = self.LIW[0].currentItem()
                if db_nav_selected_item and db_nav_selected_item.parent():
                    self.update_tableview(db_nav_selected_item)

                if any(word in row for word in ['show', 'select', 'desc']):
                    table = self.cursor.fetchall()
                    headers = [description[0] for description in self.cursor.description]
                    self.populate_tableview(headers, table)

                # updates database tree
                if any(word in row for word in ['drop', 'create']): 
                    self.update_database_tree() 
                    self.populate_tableview((), ()) # clear result table

            except Exception as e:
                self.show_error_message(str(e))
                break # break out of the loop if any error occurs
            else:
                self.conn.commit()

    def open_con_win(self, title=''):
        self.connect_window = ConnectWindow(title)

    def open_db_win(self, action):
        self.db_windows = DbWindow(action)

    def open_window(self, title, text):
        self.about_window = Window(title=title, text=text)

    def open_sql_documentation(self):
        url = "https://www.sql.org/"  # Official SQL documentation website
        webbrowser.open(url)

    def show_error_message(self, message):
        self.error_window = ErrorWindow(message)

    def update_database_tree(self):
        self.LIW[0].clear()
        if not self.conn:
            return

        self.LIW[0].setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.cursor.execute('show databases')
        for databases in self.cursor.fetchall():
            parent_db = QTreeWidgetItem(self.LIW[0], [databases[0].title()])
            self.cursor.execute(f'use {databases[0]}')
            self.cursor.execute('show tables')

            for tables in self.cursor.fetchall():
                QTreeWidgetItem(parent_db, [tables[0].title()])

        self.LIW[0].itemClicked.connect(self.update_tableview)

    def populate_tableview(self, headers, table):
        self.RIW[1].setRowCount(len(table))
        self.RIW[1].setColumnCount(len(headers))
        self.RIW[1].setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.RIW[1].setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(len(table)):
            row = table[i]
            self.RIW[1].insertRow(i)
            for j in range(len(row)):
                self.RIW[1].setItem(i, j, QTableWidgetItem(str(row[j])))

        for _ in range(len(table)): # Fixes empty rows
            self.RIW[1].removeRow(len(table))

        self.RIW[1].setHorizontalHeaderLabels(headers)

    def update_tableview(self, item, col=0):
        if not item.parent():
            self.cursor.execute(f'use {item.text(col)}')
            return
        
        self.cursor.execute(f'use {item.parent().text(col)}')
        self.cursor.execute(f'desc {item.text(col)}')
        headers = [i[0] for i in self.cursor.fetchall()]

        self.cursor.execute(f'select * from {item.text(col)}')
        table = self.cursor.fetchall()
        self.populate_tableview(headers, table)

    def create_menubar(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu('File')
        new_action = QAction('New File', self)
        open_action = QAction('Open', self)
        save_action = QAction('Save', self)
        exit_action = QAction('Exit', self)

        new_action.triggered.connect(self.new_file)
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        exit_action.triggered.connect(self.close)

        QShortcut(QKeySequence('Ctrl+N'), self).activated.connect(self.new_file)
        QShortcut(QKeySequence('Ctrl+O'), self).activated.connect(self.open_file)
        QShortcut(QKeySequence('Ctrl+S'), self).activated.connect(self.save_file)
        QShortcut(QKeySequence('Ctrl+Q'), self).activated.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        # Query Menu
        query_menu = menubar.addMenu('Query')

        execute_action = QAction('Execute Query (F5)', self)
        execute_action.triggered.connect(self.execute_query)
        close_action = QAction('Close Tab (Ctrl + W)', self)
        close_action.triggered.connect(self.close_file)

        shortcut = QShortcut(QKeySequence('F5'), self)
        shortcut.activated.connect(self.execute_query)
        shortcut_close_tab = QShortcut(QKeySequence('Ctrl+W'), self)
        shortcut_close_tab.activated.connect(self.close_file)

        query_menu.addAction(execute_action)
        query_menu.addAction(close_action)

        # Pane Menu
        pane_menu = menubar.addMenu('Panes')

        DB_Naviagtor = QAction('Navigator', self)
        Messages = QAction('Messages', self)
        Query_edit = QAction('Editor', self)
        Result = QAction('Result', self)
        sql_query = QAction('Query', self)

        DB_Naviagtor.triggered.connect(lambda: self.pane_logic('left', 0))
        sql_query.triggered.connect(lambda: self.pane_logic('left', 1))
        Messages.triggered.connect(lambda: self.pane_logic('left', 2))
        Query_edit.triggered.connect(lambda: self.pane_logic('right', 0))
        Result.triggered.connect(lambda: self.pane_logic('right', 1))

        pane_menu.addAction(DB_Naviagtor)
        pane_menu.addAction(Messages)
        pane_menu.addAction(Query_edit)
        pane_menu.addAction(Result)
        pane_menu.addAction(sql_query)

        # Database Menu
        db_menu = menubar.addMenu('Database')

        con_db = QAction('Connect', self)
        create_db = QAction('Create', self)
        drop_db = QAction('Drop', self)
        refresh_db= QAction('Refresh', self)

        con_db.triggered.connect(self.open_con_win)
        create_db.triggered.connect(lambda: self.open_db_win('Create'))
        drop_db.triggered.connect(lambda: self.open_db_win('Drop'))
        refresh_db.triggered.connect(self.update_database_tree)

        db_menu.addAction(con_db)
        db_menu.addAction(create_db)
        db_menu.addAction(drop_db)
        db_menu.addAction(refresh_db)

        # Help Menu
        help_menu = menubar.addMenu('Help')

        about_action = QAction('About', self)
        about_action.triggered.connect(lambda:self.open_window('About QueryVision', info))

        tips_action = QAction('Tips', self)
        tips_action.triggered.connect(lambda:self.open_window('Tips', tips))

        sql_doc_action = QAction('Open (SQL.org)', self)
        sql_doc_action.triggered.connect(self.open_sql_documentation)

        help_menu.addAction(about_action)
        help_menu.addAction(tips_action)
        help_menu.addAction(sql_doc_action)

        # Status Indicator
        self.connection_status_label = QLabel("●")
        self.connection_status_label.setAlignment(Qt.AlignCenter)
        self.connection_status_label.setStyleSheet("color: #ff0000; font-size: 18px;")

        status_widget = QWidget()
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.addWidget(self.connection_status_label, alignment=Qt.AlignCenter)
        status_widget.setLayout(status_layout)

        menubar.setCornerWidget(status_widget)
    
    def create_statusbar(self):
        statusbar = self.statusBar()

    def pane_logic(self, area, index):
        if area == 'left':
            self.left_dock_widgets[index].setVisible(not self.left_dock_widgets[index].isVisible())
        elif area == 'right':
            self.right_dock_widgets[index].setVisible(not self.right_dock_widgets[index].isVisible())

    def create_dock_widgets(self):
        dock_data = [
            ("Database Navigator", Qt.LeftDockWidgetArea, QTreeWidget),
            ("Help", Qt.LeftDockWidgetArea, QFrame),
            ("Messages", Qt.LeftDockWidgetArea, QTextEdit),
            ("Query Editor", Qt.RightDockWidgetArea, QTabWidget),
            ("Results", Qt.RightDockWidgetArea, QTableWidget),
        ]

        self.inner_widgets = []

        for name, area, widget_class in dock_data:
            dock_widget, inner_widget = self.create_dock(name, area, widget_class)

            if area == Qt.LeftDockWidgetArea:
                self.left_dock_widgets.append(dock_widget)
                self.LIW.append(inner_widget)
            else:
                self.right_dock_widgets.append(dock_widget)
                self.RIW.append(inner_widget)


    def create_dock(self, title, position, widget):
        dock_widget = QDockWidget(self)
        dock_widget.setWindowTitle(title)

        # Title bar setup
        title_bar = QWidget()
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(5, 5, 5, 5)

        title_bar.setStyleSheet(title_bar_style_sheet)

        title_label = QLabel(title)
        
        # Close button 
        close_button = QPushButton("x")
        close_button.setFixedSize(20, 20)   
        close_button.clicked.connect(dock_widget.close)

        # Title bar layout
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        # title_layout.addWidget(refresh_button)
        title_layout.addWidget(close_button)
        title_bar.setLayout(title_layout)

        dock_widget.setTitleBarWidget(title_bar)

        # Inner widget setup
        inner_widget = widget()
        dock_widget.setWidget(inner_widget)
        dock_widget.setFeatures(
            QDockWidget.DockWidgetMovable | 
            QDockWidget.DockWidgetFloatable | 
            QDockWidget.DockWidgetClosable
        )
        self.addDockWidget(position, dock_widget)

        return dock_widget, inner_widget
    
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        width = self.width()
        a = width // 4

        self.resizeDocks(self.left_dock_widgets, [a, a, a], Qt.Horizontal)
        self.resizeDocks(self.right_dock_widgets, [a*3, a*3], Qt.Horizontal)

class ConnectWindow(QDialog):
    def __init__(self, title):
        super().__init__()
        self.setFixedSize(300,180)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Connection' if not title else title)

        self.setStyleSheet(dialogue_window_style_sheet)
        
        font = QFont('Arial', 12)
        
        layout = QFormLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(10,10,10,10)
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(10)
        
        self.host = QLineEdit('localhost')
        self.host.setPlaceholderText('Enter Host Name')
        
        self.user = QLineEdit('root')
        self.user.setPlaceholderText('Enter User Name')
        
        self.password = QLineEdit('root')
        self.password.setPlaceholderText('Enter Password')
        self.password.setEchoMode(QLineEdit.Password)
        
        self.db_name = QLineEdit('')
        self.db_name.setPlaceholderText('Enter Database')
        
        host_lab = QLabel('Host Name:')
        host_lab.setFont(font)
        
        user_lab = QLabel('User Name:')
        user_lab.setFont(font)
        
        pass_lab = QLabel('Password:')
        pass_lab.setFont(font)
        
        db_lab = QLabel('Database:')
        db_lab.setFont(font)
        
        con_button = QPushButton('Connect')
        con_button.clicked.connect(lambda: main_window.on_connect(self.host.text(), self.user.text(), self.password.text(), self.db_name.text(), self))
        
        layout.addRow(host_lab, self.host)
        layout.addRow(user_lab, self.user)
        layout.addRow(pass_lab, self.password)
        layout.addRow(db_lab, self.db_name)
        layout.addRow(con_button)
        
        self.setLayout(layout)
        self.setModal(True)
        self.show()

class DbWindow(QDialog):
    def __init__(self, action):
        super().__init__()
        self.setFixedSize(250,90)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(f'{action} Database')
        self.setStyleSheet(style)
        
        layout = QFormLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(10,10,10,10)
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(10)
        
        self.db_name = QLineEdit()
        self.db_name.setPlaceholderText('Enter Name')

        con_button = QPushButton(action)
        con_button.clicked.connect(lambda: main_window.db_action(self.db_name.text(), self, action))

        layout.addRow('Database', self.db_name)
        layout.addRow(con_button)
        
        self.setLayout(layout)

        self.setModal(True)

        self.show()

class ErrorWindow(QDialog):
    def __init__(self, message, title="Error", parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(title)
        self.setFixedSize(350, 200)
        
        layout = QVBoxLayout()
        
        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)
        
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Understood")
        self.ok_button.setFixedSize(120, 40)
        self.ok_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        self.setStyleSheet(dialogue_window_style_sheet)
        self.setModal(True)
        self.show()

class Window(QDialog):
    def __init__(self, title, text, parent=None):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setStyleSheet(dialogue_window_style_sheet)
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()
        info_label = QLabel(text)
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(info_label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)
        self.setModal(True)
        self.show()

app = QApplication(sys.argv)

main_window = MainWindow()
# main_window.on_connect('localhost', 'root', 'root')

sys.exit(app.exec_())