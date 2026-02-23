from tkinter import *
import PyTouchBar
import PyTouchBar.items
from service.visualization_service import create_touchbar_labels

root = Tk()
PyTouchBar.prepare_tk_windows(root)

# Hide the Tkinter window - we only want the TouchBar
root.withdraw()

# Optional: Set a minimal window title for the menu bar
root.title("TouchBar System Monitor")

def action(button):
    print("Button Pressed!")

btn = PyTouchBar.items.Button(title="Button", action=action)

def update_touchbar():
    """Update TouchBar labels with fresh stats"""
    labels = create_touchbar_labels()
    PyTouchBar.set_touchbar([btn] + labels)
    PyTouchBar.reload_touchbar()
    
    # Schedule next update (e.g., every 2000ms = 2 seconds)
    root.after(500, update_touchbar)

# Initial update
update_touchbar()

root.mainloop()