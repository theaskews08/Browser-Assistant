"""
System control module for volume, keyboard, and mouse control.
Provides cross-platform support for system-level operations.
"""

import platform
import subprocess
import pyautogui
import time

# Configure pyautogui for safety
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.1  # Small pause between actions


class VolumeController:
    """Controls system volume across different platforms."""

    def __init__(self):
        self.system = platform.system()
        print(f"Volume controller initialized for {self.system}")

    def set_volume(self, level):
        """
        Set system volume to a specific level.

        Args:
            level: Volume level (0-100)
        """
        level = max(0, min(100, level))  # Clamp between 0 and 100

        try:
            if self.system == "Windows":
                self._set_volume_windows(level)
            elif self.system == "Linux":
                self._set_volume_linux(level)
            elif self.system == "Darwin":  # macOS
                self._set_volume_mac(level)
            print(f"Volume set to {level}%")
        except Exception as e:
            print(f"Error setting volume: {e}")

    def increase_volume(self, amount=10):
        """Increase volume by specified amount."""
        try:
            if self.system == "Windows":
                # Use nircmd if available, otherwise use powershell
                subprocess.run(['powershell', '-c',
                    f'(New-Object -ComObject WScript.Shell).SendKeys([char]175)'] * (amount // 2),
                    check=False, capture_output=True)
            elif self.system == "Linux":
                subprocess.run(['amixer', '-D', 'pulse', 'sset', 'Master', f'{amount}%+'],
                    check=False, capture_output=True)
            elif self.system == "Darwin":
                current = self._get_volume_mac()
                new_vol = min(100, current + amount)
                subprocess.run(['osascript', '-e', f'set volume output volume {new_vol}'],
                    check=False)
            print(f"Volume increased by {amount}%")
        except Exception as e:
            print(f"Error increasing volume: {e}")

    def decrease_volume(self, amount=10):
        """Decrease volume by specified amount."""
        try:
            if self.system == "Windows":
                subprocess.run(['powershell', '-c',
                    f'(New-Object -ComObject WScript.Shell).SendKeys([char]174)'] * (amount // 2),
                    check=False, capture_output=True)
            elif self.system == "Linux":
                subprocess.run(['amixer', '-D', 'pulse', 'sset', 'Master', f'{amount}%-'],
                    check=False, capture_output=True)
            elif self.system == "Darwin":
                current = self._get_volume_mac()
                new_vol = max(0, current - amount)
                subprocess.run(['osascript', '-e', f'set volume output volume {new_vol}'],
                    check=False)
            print(f"Volume decreased by {amount}%")
        except Exception as e:
            print(f"Error decreasing volume: {e}")

    def mute(self):
        """Mute system volume."""
        try:
            if self.system == "Windows":
                subprocess.run(['powershell', '-c',
                    '(New-Object -ComObject WScript.Shell).SendKeys([char]173)'],
                    check=False, capture_output=True)
            elif self.system == "Linux":
                subprocess.run(['amixer', '-D', 'pulse', 'sset', 'Master', 'toggle'],
                    check=False, capture_output=True)
            elif self.system == "Darwin":
                subprocess.run(['osascript', '-e', 'set volume output muted true'],
                    check=False)
            print("Volume muted")
        except Exception as e:
            print(f"Error muting volume: {e}")

    def unmute(self):
        """Unmute system volume."""
        try:
            if self.system == "Linux":
                subprocess.run(['amixer', '-D', 'pulse', 'sset', 'Master', 'unmute'],
                    check=False, capture_output=True)
            elif self.system == "Darwin":
                subprocess.run(['osascript', '-e', 'set volume output muted false'],
                    check=False)
            print("Volume unmuted")
        except Exception as e:
            print(f"Error unmuting volume: {e}")

    def _set_volume_windows(self, level):
        """Windows-specific volume setting."""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100, None)
        except ImportError:
            # Fallback to powershell if pycaw not available
            for _ in range(50):  # Reset to 0
                subprocess.run(['powershell', '-c',
                    '(New-Object -ComObject WScript.Shell).SendKeys([char]174)'],
                    check=False, capture_output=True)
            # Then increase to desired level
            steps = level // 2
            for _ in range(steps):
                subprocess.run(['powershell', '-c',
                    '(New-Object -ComObject WScript.Shell).SendKeys([char]175)'],
                    check=False, capture_output=True)

    def _set_volume_linux(self, level):
        """Linux-specific volume setting."""
        subprocess.run(['amixer', '-D', 'pulse', 'sset', 'Master', f'{level}%'],
                      check=False, capture_output=True)

    def _set_volume_mac(self, level):
        """macOS-specific volume setting."""
        subprocess.run(['osascript', '-e', f'set volume output volume {level}'],
                      check=False)

    def _get_volume_mac(self):
        """Get current volume on macOS."""
        result = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'],
                              capture_output=True, text=True)
        return int(result.stdout.strip())


class KeyboardController:
    """Controls keyboard input using pyautogui."""

    @staticmethod
    def type_text(text):
        """Type text on keyboard."""
        try:
            pyautogui.write(text, interval=0.05)
            print(f"Typed: {text}")
        except Exception as e:
            print(f"Error typing text: {e}")

    @staticmethod
    def press_key(key):
        """Press a single key."""
        try:
            pyautogui.press(key)
            print(f"Pressed key: {key}")
        except Exception as e:
            print(f"Error pressing key: {e}")

    @staticmethod
    def hotkey(*keys):
        """Press a combination of keys."""
        try:
            pyautogui.hotkey(*keys)
            print(f"Pressed hotkey: {'+'.join(keys)}")
        except Exception as e:
            print(f"Error pressing hotkey: {e}")

    @staticmethod
    def press_enter():
        """Press Enter key."""
        KeyboardController.press_key('enter')

    @staticmethod
    def press_tab():
        """Press Tab key."""
        KeyboardController.press_key('tab')

    @staticmethod
    def press_escape():
        """Press Escape key."""
        KeyboardController.press_key('escape')

    @staticmethod
    def copy():
        """Perform copy action (Ctrl+C or Cmd+C)."""
        if platform.system() == "Darwin":
            KeyboardController.hotkey('command', 'c')
        else:
            KeyboardController.hotkey('ctrl', 'c')

    @staticmethod
    def paste():
        """Perform paste action (Ctrl+V or Cmd+V)."""
        if platform.system() == "Darwin":
            KeyboardController.hotkey('command', 'v')
        else:
            KeyboardController.hotkey('ctrl', 'v')

    @staticmethod
    def cut():
        """Perform cut action (Ctrl+X or Cmd+X)."""
        if platform.system() == "Darwin":
            KeyboardController.hotkey('command', 'x')
        else:
            KeyboardController.hotkey('ctrl', 'x')


class MouseController:
    """Controls mouse movement and clicks using pyautogui."""

    @staticmethod
    def get_position():
        """Get current mouse position."""
        return pyautogui.position()

    @staticmethod
    def move_to(x, y, duration=0.5):
        """Move mouse to specific coordinates."""
        try:
            pyautogui.moveTo(x, y, duration=duration)
            print(f"Moved mouse to ({x}, {y})")
        except Exception as e:
            print(f"Error moving mouse: {e}")

    @staticmethod
    def move_relative(x, y, duration=0.5):
        """Move mouse relative to current position."""
        try:
            pyautogui.moveRel(x, y, duration=duration)
            print(f"Moved mouse by ({x}, {y})")
        except Exception as e:
            print(f"Error moving mouse: {e}")

    @staticmethod
    def click(button='left', clicks=1):
        """Click mouse button."""
        try:
            pyautogui.click(button=button, clicks=clicks)
            print(f"{button.capitalize()} clicked {clicks} time(s)")
        except Exception as e:
            print(f"Error clicking mouse: {e}")

    @staticmethod
    def right_click():
        """Right click mouse."""
        MouseController.click(button='right')

    @staticmethod
    def double_click():
        """Double click mouse."""
        MouseController.click(clicks=2)

    @staticmethod
    def scroll(amount):
        """Scroll mouse wheel."""
        try:
            pyautogui.scroll(amount)
            direction = "up" if amount > 0 else "down"
            print(f"Scrolled {direction} by {abs(amount)}")
        except Exception as e:
            print(f"Error scrolling: {e}")

    @staticmethod
    def drag_to(x, y, duration=0.5, button='left'):
        """Drag mouse to specific coordinates."""
        try:
            pyautogui.dragTo(x, y, duration=duration, button=button)
            print(f"Dragged to ({x}, {y})")
        except Exception as e:
            print(f"Error dragging mouse: {e}")


# Convenience functions for common operations
def set_volume(level):
    """Set system volume (0-100)."""
    controller = VolumeController()
    controller.set_volume(level)

def volume_up(amount=10):
    """Increase volume."""
    controller = VolumeController()
    controller.increase_volume(amount)

def volume_down(amount=10):
    """Decrease volume."""
    controller = VolumeController()
    controller.decrease_volume(amount)

def mute_volume():
    """Mute system volume."""
    controller = VolumeController()
    controller.mute()
