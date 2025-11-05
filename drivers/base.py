"""Abstract base classes for reef controller hardware drivers."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class PumpDriver(ABC):
    """Interface for controlling a variable-speed pump."""

    @abstractmethod
    def set_speed(self, percent: int) -> None:
        """Set the pump speed as a percentage (0-100)."""
        raise NotImplementedError


class WaveMakerDriver(ABC):
    """Interface for toggling wavemaker power."""

    @abstractmethod
    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the wavemaker."""
        raise NotImplementedError


class AutoFeederDriver(ABC):
    """Interface for triggering the auto feeder."""

    @abstractmethod
    def dispense(self) -> None:
        """Trigger a feed cycle."""
        raise NotImplementedError


class LightingDriver(ABC):
    """Interface for adjusting lighting intensity."""

    @abstractmethod
    def set_intensity(self, percent: int) -> None:
        """Set lighting intensity as a percentage (0-100)."""
        raise NotImplementedError


class PowerMonitorDriver(ABC):
    """Interface for retrieving solar and load telemetry."""

    @abstractmethod
    def readings(self) -> Dict[str, float]:
        """Return a dictionary of telemetry values."""
        raise NotImplementedError