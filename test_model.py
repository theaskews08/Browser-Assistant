from predict_intent import PredictIntent

# Initialize intent predictor
ip = PredictIntent()

# Test commands for different categories
test_commands = [
    # Browser commands
    ("scroll down", "down"),
    ("go back", "backward"),
    ("click the button", "click"),

    # Volume commands
    ("set volume to 50", "volume_set"),
    ("volume up", "volume_up"),
    ("mute", "mute"),

    # Keyboard commands
    ("press enter", "press_key"),
    ("type on keyboard hello", "system_type"),
    ("copy this", "copy"),

    # Mouse commands
    ("mouse click", "mouse_click"),
    ("move mouse up", "mouse_move"),
    ("mouse scroll down", "mouse_scroll"),
]

print("Testing model predictions:\n")
print("-" * 80)

correct = 0
total = len(test_commands)

for command, expected_intent in test_commands:
    predicted = ip.predict_intent(command)
    predicted_intent = predicted[0]
    confidence = predicted[1]

    is_correct = predicted_intent == expected_intent
    if is_correct:
        correct += 1
        status = "✓"
    else:
        status = "✗"

    print(f"{status} Command: '{command}'")
    print(f"  Expected: {expected_intent}, Got: {predicted_intent}, Confidence: {confidence:.4f}")
    print()

print("-" * 80)
print(f"Accuracy: {correct}/{total} ({100*correct/total:.1f}%)")
