#!/usr/bin/env python3

# standard library
import os

_path = os.path.dirname(os.path.abspath(__file__))
_icon_path = _path + '/icons/'

APPINDICATOR_ID = 'batterymonitor'

CONFIG_FILE = os.path.expanduser('~/.config/battery-monitor/battery-monitor.cfg')

ICONS = {
    "app": "icon.png",
    "success": "icon.png",
    "fail": "icon.png",
    "acpi": "icon.png",
    "charging": "charging.png",
    "discharging": "discharging.png",
    "full":  "full-charge.png",
    "custom_charge_warning": "charging.png",
    "unknown":  "not-charging.png",
    "low_battery": "low-battery.png",
    "critical_battery": "critical-battery.png",
    "custom_warning": "discharging.png",
}

for key in ICONS:
	ICONS[key] = _icon_path + ICONS[key]

MESSAGES = {
    "success": (
        u"Battery Monitor",
        u"Battery Monitor started"
    ),

    "fail": (
        u"Battery Monitor",
        u"Battery is not present!"
    ),

    "acpi": (
        u"Battery Monitor",
        u"Dependency Error! acpi is not installed.",
    ),

    "charging": (
        u"Charging",
        u"Now {battery_percentage} %, {remaining_time}"
    ),

    "discharging": (
        u"Discharging",
        u"Now {battery_percentage} %, {remaining_time}"
    ),

    "full": (
        u"Fully Charged",
        u"{battery_percentage} %"
    ),

    "unknown": (
        u"Battery Monitor",
        u"{battery_percentage} % Remaining"
    ),

    "low_battery": (
        u"Low Battery",
        u"Now {battery_percentage} %, {remaining_time}"
    ),

    "critical_battery": (
        u"Critically Low Battery",
        u"Only {battery_percentage} %, {remaining_time}"
    ),

    "custom_charge_warning": (
        u"Custom Charge Warning",
        u"Charged to {battery_percentage} %"
    ),

    "custom_warning": (
        u"Custom Warning",
        u"Now {battery_percentage} %, {remaining_time}"
    ),
}

TEST_CASES = {
    "state": [
        "Full",
        "Charging",
        "Discharging",
    ],
    "remaining": [
        "00:10:12 remaining",
        "01:47:31 remaining",
        "02:33:47 remaining",
        "03:24:25 remaining",
        "discharging at zero rate - will never fully discharge",
    ],
}
