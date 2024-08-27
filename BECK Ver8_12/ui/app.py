import datetime
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate, QSettings, QTime, Qt, QByteArray, QDateTime
from PyQt6.QtGui import QCloseEvent

import tracker_config as tkc
# ////////////////////////////////////////////////////////////////////////////////////////
# UI
# ////////////////////////////////////////////////////////////////////////////////////////
from ui.main_ui.gui import Ui_MainWindow

# ////////////////////////////////////////////////////////////////////////////////////////
# LOGGER
# ////////////////////////////////////////////////////////////////////////////////////////
from logger_setup import logger

# ////////////////////////////////////////////////////////////////////////////////////////
# NAVIGATION
# ////////////////////////////////////////////////////////////////////////////////////////
from navigation.master_navigation import change_main_stack, change_beck_stack

# Window geometry and frame
from utility.app_operations.frameless_window import (
    FramelessWindow)
from utility.app_operations.window_controls import (
    WindowController)
from utility.app_operations.show_hide import toggle_views
from utility.widgets_set_widgets.slider_spinbox_connections import (
    connect_slider_spinbox)

# Database connections
from database.database_manager import (
    DataManager)

# Delete Records
from database.database_utility.delete_records import (
    delete_selected_rows)

# setup Models
from database.database_utility.model_setup import (
    create_and_set_model)
# ////////////////////////////////////////////////////////////////////////////////////////
# ADD DATA MODULES
# ////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////
# ADD DATA MODULES
# ////////////////////////////////////////////////////////////////////////////////////////
from database.add_data.beck import add_beck_data


class MainWindow(FramelessWindow, QtWidgets.QMainWindow, Ui_MainWindow):
    """
    The main window of the application.

    This class represents the main window of the application. It inherits from `FramelessWindow`,
    `QtWidgets.QMainWindow`, and `Ui_MainWindow`. It provides methods for handling various actions
    and events related to the main window.

    Attributes:
        becks_model (QAbstractTableModel): The model for the mental mental table.
        ui (Ui_MainWindow): The user interface object for the main window.

    """
    
    def __init__(self,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.becks_model = None
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        # Database init
        self.db_manager = DataManager()
        self.setup_models()
        # QSettings settings_manager setup
        self.settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)
        self.window_controller = WindowController()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.restore_state()
        self.app_operations()
        # self.slider_set_spinbox()
        self.stack_navigation()
        self.delete_group()
        self.update_beck_summary()
        self.auto_date_time()
        self.setup_switch_page()
        self.forward_backward_btn_set()
        self.slider_set_spinbox()
        self.hidemeframe.setVisible(False)
        self.stackedWidget.setCurrentWidget(self.pageOne)
        
        # Assume you have a list of QTableView widgets
        table_views = [self.beck_table]
        
        # Column index for the date column
        date_column_index = 1  # Adjust this to the correct column index for your date column
        for table_view in table_views:
            table_view.setSortingEnabled(True)
            table_view.sortByColumn(date_column_index, Qt.SortOrder.DescendingOrder)
            
        #########################################################################
        # beck summer of summation
        #########################################################################
        self.beck_summary.setEnabled(False)
        for slider in [
                self.b_slider,
                self.b_slider_2,
                self.b_slider_3,
                self.b_slider_4,
                self.b_slider_5,
                self.b_slider_6,
                self.b_slider_7,
                self.b_slider_8,
                self.b_slider_9,
                self.b_slider_10,
                self.b_slider_11,
                self.b_slider_12,
                self.b_slider_13,
                self.b_slider_14,
                self.b_slider_15,
                self.b_slider_16,
                self.b_slider_17,
                self.b_slider_18,
                self.b_slider_19,
                self.b_slider_20,
                self.b_slider_21,
        ]:
            slider.setRange(0, 3)
        
        self.b_slider.valueChanged.connect(self.update_beck_summary)
        self.b_slider_2.valueChanged.connect(self.update_beck_summary)
        self.b_slider_3.valueChanged.connect(self.update_beck_summary)
        self.b_slider_4.valueChanged.connect(self.update_beck_summary)
        self.b_slider_5.valueChanged.connect(self.update_beck_summary)
        self.b_slider_6.valueChanged.connect(self.update_beck_summary)
        self.b_slider_7.valueChanged.connect(self.update_beck_summary)
        self.b_slider_8.valueChanged.connect(self.update_beck_summary)
        self.b_slider_9.valueChanged.connect(self.update_beck_summary)
        self.b_slider_10.valueChanged.connect(self.update_beck_summary)
        self.b_slider_11.valueChanged.connect(self.update_beck_summary)
        self.b_slider_12.valueChanged.connect(self.update_beck_summary)
        self.b_slider_13.valueChanged.connect(self.update_beck_summary)
        self.b_slider_14.valueChanged.connect(self.update_beck_summary)
        self.b_slider_15.valueChanged.connect(self.update_beck_summary)
        self.b_slider_16.valueChanged.connect(self.update_beck_summary)
        self.b_slider_17.valueChanged.connect(self.update_beck_summary)
        self.b_slider_18.valueChanged.connect(self.update_beck_summary)
        self.b_slider_19.valueChanged.connect(self.update_beck_summary)
        self.b_slider_20.valueChanged.connect(self.update_beck_summary)
        self.b_slider_21.valueChanged.connect(self.update_beck_summary)
    
    def update_beck_summary(self):
        """
        Updates the averages of the sliders in the wellbeing and pain module such that
        the overall is the average of the whole.

        :return: None
        """
        try:
            values = [slider.value() for slider in
                      [
                          self.b_slider, self.b_slider_2, self.b_slider_3, self.b_slider_4,
                          self.b_slider_5, self.b_slider_6, self.b_slider_7, self.b_slider_8,
                          self.b_slider_9, self.b_slider_10, self.b_slider_11, self.b_slider_12,
                          self.b_slider_13, self.b_slider_14, self.b_slider_15, self.b_slider_16,
                          self.b_slider_17, self.b_slider_18, self.b_slider_19, self.b_slider_20,
                          self.b_slider_21
                      ] if
                      slider.value() > 0]

            sumabitch = sum(values)

            self.beck_summary.setValue(int(sumabitch))

        except Exception as e:
            logger.error(f"{e}", exc_info=True)
    
    def forward_backward_btn_set(self):
        self.actionNext.triggered.connect(self.next_page)
        self.actionPrev.triggered.connect(self.prev_page)
        
        # action forward/backward
        # self.actionPrevious.triggered.connect(self.prev_page)
        # self.actionNext.triggered.connect(self.next_page)
        self.actionHome.triggered.connect(self.go_home)
    
    def next_page(self):
        current_index = self.stackedWidget.currentIndex()
        next_index = (current_index + 1) % self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(next_index)
    
    def prev_page(self):
        current_index = self.stackedWidget.currentIndex()
        prev_index = (current_index - 1) % self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(prev_index)
    
    def go_home(self):
        self.stackedWidget.setCurrentIndex(0)
        
    def switch_to_page0(self):
        """
        Switches the current widget to the 'beckPage' and adjusts the window size.

        This method sets the current widget of the mainStack to the 'beckPage' widget,
        and adjusts the size of the window to a fixed size of 445x170 pixels.

        Parameters:
        None

        Returns:
        None
        """
        self.stackedWidget.setCurrentWidget(self.pageOne)
        self.setFixedSize(500, 135)
        
    def switch_to_page1(self):
        """
        Switches the current widget to the altmanPage and adjusts the window size.

        This method sets the current widget of the mainStack to the altmanPage,
        and adjusts the window size to a fixed size of 445x170 pixels.

        Parameters:
        None

        Returns:
        None
        """
        self.mainStack.setCurrentWidget(self.pageTwo)
        self.setFixedSize(940, 680)
    
    # ////////////////////////////////////////////////////////////////////////////////////////
    # APP-OPERATIONS setup
    # ////////////////////////////////////////////////////////////////////////////////////////
    def app_operations(self):
        """
        Performs the necessary operations for setting up the application.

        This method connects signals and slots, sets the initial state of the UI elements,
        and handles various actions triggered by the user.

        Raises:
            Exception: If an error occurs while setting up the app_operations.

        """
        try:
            self.beck_table_commit()
            self.mainStack.currentChanged.connect(self.on_page_changed)
            last_index = self.settings.value("lastPageIndex", 0, type=int)
            self.mainStack.setCurrentIndex(last_index)
        except Exception as e:
            logger.error(f"Error occurred while setting up app_operations : {e}", exc_info=True)
    
    def auto_date_time(self):
        self.beck_time.setTime(QTime.currentTime())
        self.beck_date.setDate(QDate.currentDate())
    
    def setup_switch_page(self):
        self.actionShowBeckExam.triggered.connect(self.switch_to_page0)
        self.actionShowBeckTable.triggered.connect(self.switch_to_page1)
    
    def on_page_changed(self, index):
        """
        Callback method triggered when the page is changed in the UI.

        Args:
            index (int): The index of the new page.

        Raises:
            Exception: If an error occurs while setting the last page index.

        """
        try:
            self.settings.setValue("lastPageIndex", index)
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
    
    # ////////////////////////////////////////////////////////////////////////////////////////
    # Minder Navigation
    # ////////////////////////////////////////////////////////////////////////////////////////
    def stack_navigation(self):
        """
        Connects the triggered signals of certain actions to change the stack pages.

        The method creates a dictionary `change_stack_pages` that maps actions to their corresponding page index.
        It then iterates over the dictionary and connects the `triggered` signal of each action to a lambda function
        that calls the `change_stack_page` method with the corresponding page index.

        Raises:
            Exception: If an error occurs during the connection of signals.

        """
        try:
            change_stack_pages = {
                self.actionShowBeckExam: 0,
                self.actionShowBeckTable: 1,
            }
            
            for action, page in change_stack_pages.items():
                action.triggered.connect(lambda _, p=page: change_main_stack(self.mainStack, p))
        
        except Exception as e:
            logger.error(f"An error has occurred: {e}", exc_info=True)
    
    # ////////////////////////////////////////////////////////////////////////////////////////
    # SLIDER UPDATES SPINBOX/VICE VERSA SETUP
    # ////////////////////////////////////////////////////////////////////////////////////////
    def slider_set_spinbox(self):
        """
        Connects sliders to their corresponding spinboxes.

        This method establishes a connection between sliders and spinboxes
        by mapping each slider to its corresponding spinbox. It then calls
        the `connect_slider_spinbox` function to establish the connection.

        Returns:
            None
        """
        connect_slider_to_spinbox = {
            self.b_slider: self.b_box,
            self.b_slider_2: self.b_box_2,
            self.b_slider_3: self.b_box_3,
            self.b_slider_4: self.b_box_4,
            self.b_slider_5: self.b_box_5,
            self.b_slider_6: self.b_box_6,
            self.b_slider_7: self.b_box_7,
            self.b_slider_8: self.b_box_8,
            self.b_slider_9: self.b_box_9,
            self.b_slider_10: self.b_box_10,
            self.b_slider_11: self.b_box_11,
            self.b_slider_12: self.b_box_12,
            self.b_slider_13: self.b_box_13,
            self.b_slider_14: self.b_box_14,
            self.b_slider_15: self.b_box_15,
            self.b_slider_16: self.b_box_16,
            self.b_slider_17: self.b_box_17,
            self.b_slider_18: self.b_box_18,
            self.b_slider_19: self.b_box_19,
            self.b_slider_20: self.b_box_20,
            self.b_slider_21: self.b_box_21,
            self.beck_summary: self.sum_box,
        }
        
        for slider, spinbox in connect_slider_to_spinbox.items():
            connect_slider_spinbox(slider, spinbox)
    
    def beck_table_commit(self) -> None:
        """
        Connects the 'commit' action to the 'add_mentalsolo_data' function and inserts data into the altman_table.

        This method connects the 'commit' action to the 'add_beck_data' function, which inserts data into the beck_table.
        The data to be inserted is retrieved from various UI elements in the main window.

        Raises:
            Exception: If an error occurs during the process.
        """
        try:
            self.actionCommit.triggered.connect(
                lambda: add_beck_data(
                    self, {
                        "beck_date": "beck_date",
                        "beck_time": "beck_time",
                        "b_slider": "b_slider",
                        "b_slider_2": "b_slider_2",
                        "b_slider_3": "b_slider_3",
                        "b_slider_4": "b_slider_4",
                        "b_slider_5": "b_slider_5",
                        "b_slider_6": "b_slider_6",
                        "b_slider_7": "b_slider_7",
                        "b_slider_8": "b_slider_8",
                        "b_slider_9": "b_slider_9",
                        "b_slider_10": "b_slider_10",
                        "b_slider_11": "b_slider_11",
                        "b_slider_12": "b_slider_12",
                        "b_slider_13": "b_slider_13",
                        "b_slider_14": "b_slider_14",
                        "b_slider_15": "b_slider_15",
                        "b_slider_16": "b_slider_16",
                        "b_slider_17": "b_slider_17",
                        "b_slider_18": "b_slider_18",
                        "b_slider_19": "b_slider_19",
                        "b_slider_20": "b_slider_20",
                        "b_slider_21": "b_slider_21",
                        "beck_summary": "beck_summary",
                        "model": "becks_model"
                    },
                    self.db_manager.insert_into_beck_table_aug_8, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
            
    def delete_group(self):
        """
        Connects the delete action to the delete_selected_rows function.

        This method connects the delete action to the delete_selected_rows function,
        passing the necessary arguments to delete the selected rows in the altman_table.

        Args:
            self: The instance of the main window.

        Returns:
            None
        """
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'beck_table',
                'becks_model'
            )
        )
        
    def setup_models(self) -> None:
        """
        Set up the models for the main window.

        This method creates and sets the becks_model using the altman_table.

        Returns:
            None
        """
        self.becks_model = create_and_set_model(
            "beck_table_aug_8",
            self.beck_table
        )
        
    def save_state(self):
            """
            Saves the window geometry state and window state.

            This method saves the current geometry and state of the window
            using the QSettings object. It saves the window geometry state
            and the window state separately.

            Raises:
                Exception: If there is an error saving the window geometry state
                           or the window state.

            """
            try:
                self.settings.setValue("geometry", self.saveGeometry())
            except Exception as e:
                logger.error(f"Error saving the minds_module geo{e}", exc_info=True)
            try:
                self.settings.setValue("windowState", self.saveState())
            except Exception as e:
                logger.error(f"Error saving the minds_module geo{e}", exc_info=True)
    
    def restore_state(self) -> None:
        """
        Restores the window geometry and state.

        This method restores the previous geometry and state of the window
        by retrieving the values from the settings. If an error occurs during
        the restoration process, an error message is logged.

        Raises:
            Exception: If an error occurs while restoring the window geometry or state.
        """
        try:
            # restore window geometry state
            self.restoreGeometry(self.settings.value("geometry", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring the minds module : stress state {e}")
        
        try:
            self.restoreState(self.settings.value("windowState", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring WINDOW STATE {e}", exc_info=True)
    
    def closeEvent(self, event: QCloseEvent) -> None:
            """
            Event handler for the close event of the window.

            Saves the state before closing the window.

            Args:
                event (QCloseEvent): The close event object.

            Returns:
                None
            """
            try:
                self.save_state()
            except Exception as e:
                logger.error(f"error saving state during closure: {e}", exc_info=True)
