"""Demo GUI for the Reef Controller project using PySide6."""
from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from drivers.mock import (
    MockAutoFeeder,
    MockLightingController,
    MockPowerMonitor,
    MockReturnPump,
    MockWaveMaker,
)


class ReefControllerWindow(QMainWindow):
    """Main window for the reef controller demo."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Reef Controller (Demo)")

        # TODO: Replace mock devices with real hardware drivers wired to GPIO/PWM.
        self.pump = MockReturnPump()
        self.wavemaker = MockWaveMaker()
        self.feeder = MockAutoFeeder()
        self.lighting = MockLightingController()
        self.power_monitor = MockPowerMonitor()

        self.status_label = QLabel("PV: --.- V | Load: --.- V | Current: --.- A")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)

        title = QLabel("Reef Controller (Demo)")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        layout.addLayout(self._build_pump_controls())
        layout.addLayout(self._build_wavemaker_controls())
        layout.addLayout(self._build_feeder_controls())
        layout.addLayout(self._build_lighting_controls())
        layout.addWidget(self.status_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Initialize with default readings.
        self._update_power_status()

    def _build_pump_controls(self) -> QHBoxLayout:
        container = QHBoxLayout()

        label = QLabel("Return Pump speed (%):")
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(50)
        value_display = QLabel("50")

        def on_speed_change(value: int) -> None:
            value_display.setText(str(value))
            # TODO: Connect to actual pump speed control via PWM/driver IC.
            self.pump.set_speed(value)

        slider.valueChanged.connect(on_speed_change)

        container.addWidget(label)
        container.addWidget(slider)
        container.addWidget(value_display)
        return container

    def _build_wavemaker_controls(self) -> QHBoxLayout:
        container = QHBoxLayout()

        toggle = QCheckBox("Enable Wavemaker")
        toggle.setChecked(True)

        def on_toggle_changed(checked: bool) -> None:
            # TODO: Integrate with wavemaker relay or DC control hardware.
            self.wavemaker.set_enabled(checked)

        toggle.toggled.connect(on_toggle_changed)

        container.addWidget(toggle)
        return container

    def _build_feeder_controls(self) -> QHBoxLayout:
        container = QHBoxLayout()

        button = QPushButton("Feed Now")

        def on_feed_clicked() -> None:
            # TODO: Connect to auto feeder motor/servo control via GPIO.
            self.feeder.dispense()

        button.clicked.connect(on_feed_clicked)

        container.addWidget(button)
        return container

    def _build_lighting_controls(self) -> QHBoxLayout:
        container = QHBoxLayout()

        label = QLabel("Lighting intensity (%):")
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(75)
        value_display = QLabel("75")

        def on_intensity_change(value: int) -> None:
            value_display.setText(str(value))
            # TODO: Integrate with LED driver over I²C or dimming interface.
            self.lighting.set_intensity(value)

        slider.valueChanged.connect(on_intensity_change)

        container.addWidget(label)
        container.addWidget(slider)
        container.addWidget(value_display)
        return container

    def _update_power_status(self) -> None:
        readings = self.power_monitor.readings()
        self.status_label.setText(
            f"PV: {readings['pv_voltage']:.1f} V | "
            f"Load: {readings['load_voltage']:.1f} V | "
            f"Current: {readings['current']:.1f} A"
        )
        # TODO: Replace mock readings with real-time solar input and load monitoring.


def main() -> None:
    app = QApplication(sys.argv)
    window = ReefControllerWindow()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
