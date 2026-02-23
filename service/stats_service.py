import psutil
import subprocess


def get_cpu_usage():
    """
    Get the current CPU usage percentage.
    
    Returns:
        float: CPU usage percentage (0-100)
    """
    return psutil.cpu_percent(interval=1)


def get_ram_usage():
    """
    Get the current RAM usage information.
    
    Returns:
        dict: Dictionary containing RAM usage details
            - percent: RAM usage percentage (0-100)
            - used_gb: Used RAM in GB
            - total_gb: Total RAM in GB
            - available_gb: Available RAM in GB
    """
    memory = psutil.virtual_memory()
    return {
        'percent': memory.percent,
        'used_gb': round(memory.used / (1024 ** 3), 2),
        'total_gb': round(memory.total / (1024 ** 3), 2),
        'available_gb': round(memory.available / (1024 ** 3), 2)
    }


def get_temperature():
    """
    Get the current CPU temperature on macOS.
    Uses the 'osx-cpu-temp' command if available, otherwise returns None.
    
    To install osx-cpu-temp: brew install osx-cpu-temp
    
    Returns:
        float: Temperature in Celsius, or None if unavailable
    """
    try:
        # Try using osx-cpu-temp command
        result = subprocess.run(
            ['osx-cpu-temp'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            # Output format is typically "XX.X°C"
            temp_str = result.stdout.strip().replace('°C', '')
            return float(temp_str)
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError, ValueError):
        pass
    
    # Alternative: try using SMC (if psutil has sensor support on this platform)
    try:
        temps = psutil.sensors_temperatures() # type: ignore
        if temps and 'coretemp' in temps:
            # Get the average of all core temperatures
            core_temps = [temp.current for temp in temps['coretemp']]
            return round(sum(core_temps) / len(core_temps), 1)
    except (AttributeError, KeyError):
        pass
    
    return None


def get_all_stats():
    """
    Get all system statistics in a single dictionary.
    
    Returns:
        dict: Dictionary containing all system stats
            - cpu_percent: CPU usage percentage
            - ram: Dictionary with RAM usage details
            - temperature: CPU temperature in Celsius (or None if unavailable)
    """
    return {
        'cpu_percent': get_cpu_usage(),
        'ram': get_ram_usage(),
        'temperature': get_temperature()
    }


if __name__ == '__main__':
    # Test the stats service
    stats = get_all_stats()
    print("System Statistics:")
    print(f"CPU Usage: {stats['cpu_percent']}%")
    print(f"RAM Usage: {stats['ram']['percent']}% ({stats['ram']['used_gb']} GB / {stats['ram']['total_gb']} GB)")
    if stats['temperature'] is not None:
        print(f"Temperature: {stats['temperature']}°C")
    else:
        print("Temperature: Not available (install 'osx-cpu-temp' with: brew install osx-cpu-temp)")

