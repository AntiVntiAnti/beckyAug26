from PyQt6.QtCore import QDate, QTime
import tracker_config as tkc
from logger_setup import logger


def add_beck_data(main_window_instance, widget_names, db_insert_method):
    """
    Add mental solo data to the database.

    Args:
        main_window_instance (object): The instance of the main window.
        widget_names (dict): A dictionary containing the names of the widgets.
        db_insert_method (function): The method used to insert data into the database.

    Returns:
        None

    Raises:
        Exception: If there is an error getting the value from a widget or inserting data into the database.
    """
    widget_methods = {
        widget_names['beck_date']: (None, 'date', "yyyy-MM-dd"),
        widget_names['beck_time']: (None, 'time', "hh:mm:ss"),
        widget_names['b_slider']: (None, 'value', None),
        widget_names['b_slider_2']: (None, 'value', None),
        widget_names['b_slider_3']: (None, 'value', None),
        widget_names['b_slider_4']: (None, 'value', None),
        widget_names['b_slider_5']: (None, 'value', None),
        widget_names['b_slider_6']: (None, 'value', None),
        widget_names['b_slider_7']: (None, 'value', None),
        widget_names['b_slider_8']: (None, 'value', None),
        widget_names['b_slider_9']: (None, 'value', None),
        widget_names['b_slider_10']: (None, 'value', None),
        widget_names['b_slider_11']: (None, 'value', None),
        widget_names['b_slider_12']: (None, 'value', None),
        widget_names['b_slider_13']: (None, 'value', None),
        widget_names['b_slider_14']: (None, 'value', None),
        widget_names['b_slider_15']: (None, 'value', None),
        widget_names['b_slider_16']: (None, 'value', None),
        widget_names['b_slider_17']: (None, 'value', None),
        widget_names['b_slider_18']: (None, 'value', None),
        widget_names['b_slider_19']: (None, 'value', None),
        widget_names['b_slider_20']: (None, 'value', None),
        widget_names['b_slider_21']: (None, 'value', None),
        widget_names['beck_summary']: (None, 'value', None)
    }

    data_to_insert = []
    for widget_name, (widget_attr, method, format_type) in widget_methods.items():
        widget = getattr(main_window_instance, widget_name)
        try:
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)
        except Exception as e:
            logger.error(f"Error getting value from widget {widget_name}: {e}")

    try:
        db_insert_method(*data_to_insert)
        reset_beck_exam(main_window_instance, widget_names)
    except Exception as e:
        logger.error(f"Error inserting data into the database: {e}")


def reset_beck_exam(main_window_instance, widget_names):
    """
    Reset the values of the mental_mental form in the main window.

    Args:
        main_window_instance (object): An instance of the main window.
        widget_names (dict): A dictionary containing the names of the widgets used in the mental_mental form.

    Raises:
        Exception: If there is an error resetting the form.

    Returns:
        None
    """
    try:
        getattr(main_window_instance, widget_names['beck_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['beck_time']).setTime(QTime.currentTime())
        getattr(main_window_instance, widget_names['b_slider']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_2']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_3']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_4']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_5']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_6']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_7']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_8']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_9']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_10']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_11']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_12']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_13']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_14']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_15']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_16']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_17']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_18']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_19']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_20']).setValue(0)
        getattr(main_window_instance, widget_names['b_slider_21']).setValue(0)
        getattr(main_window_instance, widget_names['beck_summary']).setValue(0)
        getattr(main_window_instance, widget_names['model']).select()
    except Exception as e:
        logger.error(f"Error resetting pain levels form: {e}")
