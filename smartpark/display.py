### Class: Display
class Display:
    """The SenseHAT object to control the LED display."""
    self.sense_hat = None
    
    def __init__(self):
        """Initialize the Display object with a SenseHAT instance."""
        pass
    '''Use the `sense.show_message()` method to display text on the LED display (e.g., `sense.show_message("Hello, World!")`).
    - Configure the text scroll speed, text color, and background color using optional parameters:
    For example: `sense.show_message("Hello, World!", scroll_speed=0.1, text_colour=(255, 255, 255), back_colour=(0, 0, 0))`).'''
    def show_message(self, message):
        """Display a message on the LED display."""
        pass
