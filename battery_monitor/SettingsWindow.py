#!/usr/bin/env python3

# standard library
import configparser
import os

# third-party library
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# imports from current project
from .config import CONFIG_FILE
from .config import ICONS
from .ErrorLib import ValidationError



class SettingsWindow(Gtk.Window):
    """GUI class for Settings Window.

    This class displays the Settings window in where the user can manage the configurations for Battery Monitor.
    """

    def __init__(self):
        Gtk.Window.__init__(self, title='Battery Monitor')
        self.set_default_size(400, 300)
        self.set_resizable(True)
        self.set_border_width(0)
        self.get_focus()
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_icon_from_file(ICONS['app'])
        self.config_dir = os.path.dirname(CONFIG_FILE)
        self.config = configparser.ConfigParser()
        self.__load_config()

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        self.notebook.append_page(self.__configuration_page(), Gtk.Label('Configuration'))

    def __configuration_page(self):
        label0 = Gtk.Label('Critical Battery Warning')
        label0.set_justify(Gtk.Justification.LEFT)
        label0.set_halign(Gtk.Align.START)
        label0.set_hexpand(True)
        label1 = Gtk.Label('Low Battery Warning')
        label1.set_justify(Gtk.Justification.LEFT)
        label1.set_halign(Gtk.Align.START)
        label1.set_hexpand(True)
        label2 = Gtk.Label('Custom Warning')
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_halign(Gtk.Align.START)
        label2.set_hexpand(True)
        label3 = Gtk.Label('Custom Charge Warning')
        label3.set_justify(Gtk.Justification.LEFT)
        label3.set_halign(Gtk.Align.START)
        label3.set_hexpand(True)
        label4 = Gtk.Label('Notification Stability Time')
        label4.set_justify(Gtk.Justification.LEFT)
        label4.set_halign(Gtk.Align.START)
        label4.set_hexpand(True)

        self.entry0 = Gtk.Entry()
        self.entry0.set_text(str(self.critical_battery))
        self.entry0.set_tooltip_text('Value as percentage')
        self.entry1 = Gtk.Entry()
        self.entry1.set_text(str(self.low_battery))
        self.entry1.set_tooltip_text('Value as percentage')
        self.entry2 = Gtk.Entry()
        self.entry2.set_text(str(self.custom_warning))
        self.entry2.set_tooltip_text('Value as percentage')
        self.entry3 = Gtk.Entry()
        self.entry3.set_text(str(self.custom_charge_warning))
        self.entry3.set_tooltip_text('Value as percentage')
        self.entry4 = Gtk.Entry()
        self.entry4.set_text(str(self.notification_stability))
        self.entry4.set_tooltip_text('Value in seconds')

        save_button = Gtk.Button(label='Save')
        save_button.connect('clicked', self.__save_config)

        grid = Gtk.Grid()
        grid.set_row_spacing(15)
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        grid.set_border_width(10)
        grid.set_column_spacing(2)
        grid.set_column_homogeneous(False)
        grid.attach(label0, 0, 0, 14, 1)
        grid.attach(self.entry0, 14, 0, 1, 1)
        grid.attach(label1, 0, 1, 14, 1)
        grid.attach(self.entry1, 14, 1, 1, 1)
        grid.attach(label2, 0, 2, 14, 1)
        grid.attach(self.entry2, 14, 2, 1, 1)
        grid.attach(label3, 0, 3, 14, 1)
        grid.attach(self.entry3, 14, 3, 1, 1)
        grid.attach(label4, 0, 4, 14, 1)
        grid.attach(self.entry4, 14, 4, 1, 1)
        grid.attach(save_button, 0, 7, 15, 1)

        return grid

    def __load_config(self):
        """Loads configurations from config file.

        Tries to read and parse from config file. If the config file is missing or not readable, then it triggers default configurations.
        """

        try:
            self.config.read(CONFIG_FILE)
            self.critical_battery = self.config['settings']['critical_battery']
            self.low_battery = self.config['settings']['low_battery']
            self.custom_warning = self.config['settings']['custom_warning']
            self.custom_charge_warning = self.config['settings']['custom_charge_warning']
            self.notification_stability = self.config['settings']['notification_stability']
        except:
            print('Config file is missing or not readable. Using default configurations.')
            self.critical_battery = '10'
            self.low_battery = '30'
            self.custom_warning = ''
            self.custom_charge_warning = ''
            self.notification_stability = '5'

    def __save_config(self, widget):
        """Saves configurations to config file.

        Saves user-defined configurations to config file. If the config file does not exist, it creates a new config file (~/.config/battery-monitor/battery-monitor.cfg) in user's home directory.
        """

        if os.path.exists(self.config_dir):
            pass
        else:
            os.makedirs(self.config_dir)

        self.config['settings'] = {
            'critical_battery': self.entry0.get_text(),
            'low_battery': self.entry1.get_text(),
            'custom_warning': self.entry2.get_text(),
            'custom_charge_warning': self.entry3.get_text(),
            'notification_stability': self.entry4.get_text()
        }

        try:
            self.__validate_config(self.config['settings'])
            with open(CONFIG_FILE, 'w') as f:
                self.config.write(f)
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, 'Successfully Saved!')
                dialog.format_secondary_text(
                    'You settings have been saved successfully.')
                response = dialog.run()
                if response == Gtk.ResponseType.OK:
                    self.close()
                dialog.destroy()
        except ValidationError as message:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, 'Validation Error!')
            dialog.format_secondary_text(str(message))
            dialog.run()
            dialog.destroy()

    def __validate_config(self, config):
        """validates config before saving to config file."""

        if bool(config['critical_battery']) and bool(config['low_battery']):
            if int(config['critical_battery']) >= int(config['low_battery']):
                raise ValidationError('The value of low battery warning must be greater than the value of critical battery warning.')
        else:
            if bool(config['critical_battery']):
                raise ValidationError('Low battery warning can not be empty.')
            else:
                raise ValidationError('Critical battery warning can not be empty.')

        if bool(config['low_battery']) and bool(config['custom_warning']):
            if int(config['low_battery']) >= int(config['custom_warning']):
                raise ValidationError('The value of custom warning must be greater than the value of low battery warning.')

        if bool(config['custom_warning']) and bool(config['custom_charge_warning']):
            if int(config['custom_warning']) >= int(config['custom_charge_warning']):
                raise ValidationError('The value of the custom charge warning must be greater than the value of the custom warning.')
        elif bool(config['low_battery']) and bool(config['custom_charge_warning']):
            if int(config['low_battery']) >= int(config['custom_charge_warning']):
                raise ValidationError('The value of the custom charge warning must be greater than the value of the low battery warning.')

        if bool(config['notification_stability']):
            if int(config['notification_stability']) <= 0:
                raise ValidationError('Notification stability time must be greater than zero.')
        else:
            raise ValidationError('Notification stability time can not be empty.')
