"""
System command handlers for volume, keyboard, and mouse control.
"""

from system_control import VolumeController, KeyboardController, MouseController
import re

# Initialize controllers
volume_controller = VolumeController()
keyboard_controller = KeyboardController()
mouse_controller = MouseController()

# TTS will be initialized on first use (lazy loading)
_tts = None

def get_tts():
    """Get TTS engine with lazy initialization."""
    global _tts
    if _tts is None:
        try:
            from tts_engine import get_tts_engine
            _tts = get_tts_engine()
        except:
            _tts = None
    return _tts


def handle_volume_set(command):
    """Set volume to a specific level."""
    # Extract number from command
    numbers = re.findall(r'\d+', command)
    if numbers:
        level = int(numbers[0])
        volume_controller.set_volume(level)
        tts = get_tts()
        if tts:
            tts.speak_async(f"Volume set to {level} percent")
    else:
        print("Please specify a volume level (0-100)")


def handle_volume_up(command):
    """Increase volume."""
    # Check if amount is specified
    numbers = re.findall(r'\d+', command)
    amount = int(numbers[0]) if numbers else 10
    volume_controller.increase_volume(amount)
    tts = get_tts()
    if tts:
        tts.speak_async("Volume up")


def handle_volume_down(command):
    """Decrease volume."""
    # Check if amount is specified
    numbers = re.findall(r'\d+', command)
    amount = int(numbers[0]) if numbers else 10
    volume_controller.decrease_volume(amount)
    tts = get_tts()
    if tts:
        tts.speak_async("Volume down")


def handle_mute(command):
    """Mute system volume."""
    volume_controller.mute()
    tts = get_tts()
    if tts:
        tts.speak_async("Muted")


def handle_unmute(command):
    """Unmute system volume."""
    volume_controller.unmute()
    tts = get_tts()
    if tts:
        tts.speak_async("Unmuted")


def handle_press_key(command):
    """Press a specific key."""
    # Extract key name from command
    command_lower = command.lower()

    key_mappings = {
        'enter': 'enter',
        'return': 'enter',
        'tab': 'tab',
        'escape': 'escape',
        'esc': 'escape',
        'space': 'space',
        'backspace': 'backspace',
        'delete': 'delete',
        'up': 'up',
        'down': 'down',
        'left': 'left',
        'right': 'right',
        'home': 'home',
        'end': 'end',
        'page up': 'pageup',
        'page down': 'pagedown'
    }

    for key_word, key_name in key_mappings.items():
        if key_word in command_lower:
            keyboard_controller.press_key(key_name)
            return

    print("Key not recognized. Try: enter, tab, escape, space, etc.")


def handle_type_text(command):
    """Type text using system keyboard (not browser)."""
    # Remove the command trigger and type the rest
    text = command.lower()
    triggers = ['type', 'write', 'keyboard']
    for trigger in triggers:
        if text.startswith(trigger):
            text = text[len(trigger):].strip()
            break

    if text:
        keyboard_controller.type_text(text)
    else:
        print("Please specify text to type")


def handle_copy(command):
    """Perform copy action."""
    keyboard_controller.copy()


def handle_paste(command):
    """Perform paste action."""
    keyboard_controller.paste()


def handle_cut(command):
    """Perform cut action."""
    keyboard_controller.cut()


def handle_mouse_click(command):
    """Click mouse."""
    if 'right' in command.lower():
        mouse_controller.right_click()
    elif 'double' in command.lower():
        mouse_controller.double_click()
    else:
        mouse_controller.click()


def handle_mouse_move(command):
    """Move mouse cursor."""
    # Extract direction and distance
    command_lower = command.lower()

    # Get distance if specified
    numbers = re.findall(r'\d+', command)
    distance = int(numbers[0]) if numbers else 100

    if 'up' in command_lower:
        mouse_controller.move_relative(0, -distance, duration=0.3)
    elif 'down' in command_lower:
        mouse_controller.move_relative(0, distance, duration=0.3)
    elif 'left' in command_lower:
        mouse_controller.move_relative(-distance, 0, duration=0.3)
    elif 'right' in command_lower:
        mouse_controller.move_relative(distance, 0, duration=0.3)
    else:
        print("Please specify direction: up, down, left, or right")


def handle_mouse_scroll(command):
    """Scroll using mouse wheel."""
    command_lower = command.lower()

    # Get amount if specified
    numbers = re.findall(r'\d+', command)
    amount = int(numbers[0]) if numbers else 3

    if 'down' in command_lower:
        mouse_controller.scroll(-amount)
    else:
        mouse_controller.scroll(amount)


def get_system_commands():
    """Return dictionary of system command handlers."""
    return {
        # Volume commands
        'volume_set': handle_volume_set,
        'volume_up': handle_volume_up,
        'volume_down': handle_volume_down,
        'mute': handle_mute,
        'unmute': handle_unmute,

        # Keyboard commands
        'press_key': handle_press_key,
        'system_type': handle_type_text,
        'copy': handle_copy,
        'paste': handle_paste,
        'cut': handle_cut,

        # Mouse commands
        'mouse_click': handle_mouse_click,
        'mouse_move': handle_mouse_move,
        'mouse_scroll': handle_mouse_scroll,
    }
