import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import PyTouchBar.items
from service.stats_service import get_all_stats


def get_color_for_percentage(percent):
    """
    Get a color gradient from green (low) to yellow (medium) to red (high).
    
    Args:
        percent: Value between 0 and 100
        
    Returns:
        tuple: RGBA color tuple (r, g, b, a) with values 0-1
    """
    # Clamp percentage between 0 and 100
    percent = max(0, min(100, percent))
    
    if percent <= 50:
        # Green to Yellow (0-50%)
        ratio = percent / 50
        r = ratio  # 0 -> 1
        g = 1.0
        b = 0.0
    else:
        # Yellow to Red (50-100%)
        ratio = (percent - 50) / 50
        r = 1.0
        g = 1.0 - ratio  # 1 -> 0
        b = 0.0
    
    return (r, g, b, 1.0)


def get_color_for_temperature(temp):
    """
    Get a color for temperature display.
    Maps temperature to a color gradient (assuming reasonable CPU temps 30-100°C).
    
    Args:
        temp: Temperature in Celsius or None
        
    Returns:
        tuple: RGBA color tuple (r, g, b, a) with values 0-1
    """
    if temp is None:
        return (0.7, 0.7, 0.7, 1.0)  # Gray if unavailable
    
    # Map temperature to percentage (30°C = 0%, 100°C = 100%)
    temp_min = 30
    temp_max = 100
    percent = ((temp - temp_min) / (temp_max - temp_min)) * 100
    
    return get_color_for_percentage(percent)


def create_touchbar_labels():
    """
    Create three TouchBar labels displaying CPU, RAM, and Temperature.
    Labels are colored based on their percentage values (green=low, yellow=medium, red=high).
    
    Returns:
        list: List of three PyTouchBar.items.Label objects
    """
    # Get current system stats
    stats = get_all_stats()
    
    # CPU Label
    cpu_percent = stats['cpu_percent']
    cpu_color = get_color_for_percentage(cpu_percent)
    cpu_label = PyTouchBar.items.Label(
        text=f"CPU: {cpu_percent:.1f}%",
        text_color=cpu_color,
        font_size=14
    )
    
    # RAM Label
    ram_percent = stats['ram']['percent']
    ram_color = get_color_for_percentage(ram_percent)
    ram_label = PyTouchBar.items.Label(
        text=f"RAM: {ram_percent:.1f}%",
        text_color=ram_color,
        font_size=14
    )
    
    # Temperature Label
    temp = stats['temperature']
    temp_color = get_color_for_temperature(temp)
    if temp is not None:
        temp_text = f"Temp: {temp:.1f}°C"
    else:
        temp_text = "Temp: N/A"
    
    temp_label = PyTouchBar.items.Label(
        text=temp_text,
        text_color=temp_color,
        font_size=14
    )
    
    return [cpu_label, ram_label, temp_label]


if __name__ == '__main__':
    # Test the visualization service
    labels = create_touchbar_labels()
    print(f"Created {len(labels)} TouchBar labels:")
    for i, label in enumerate(labels, 1):
        print(f"  {i}. Text: {label.textBase}, Color: {label.text_color_}")
