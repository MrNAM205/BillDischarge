
import psutil

def get_system_status():
    """Gathers CPU, memory, and disk usage statistics."""
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')

        return {
            "cpu_percent": cpu_usage,
            "memory_percent": memory_info.percent,
            "disk_percent": disk_info.percent
        }
    except Exception as e:
        return {"error": str(e)}
