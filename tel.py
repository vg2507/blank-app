import bluetooth
import subprocess

def find_bluetooth_devices():
    """
    Поиск Bluetooth-устройств и измерение их уровня сигнала (RSSI).
    """
    try:
        print("Сканирование Bluetooth-устройств...")
        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, lookup_class=False)

        if not nearby_devices:
            print("Устройства не найдены.")
            return

        print("Найдено устройств:", len(nearby_devices))
        for addr, name in nearby_devices:
            print(f"\nУстройство: {name} ({addr})")
            rssi = get_device_rssi(addr)
            if rssi is not None:
                print(f"Уровень сигнала (RSSI): {rssi} дБм")
            else:
                print("Не удалось определить RSSI.")
    except Exception as e:
        print(f"Ошибка при поиске устройств: {e}")

def get_device_rssi(addr):
    """
    Получение RSSI для устройства с указанным MAC-адресом.
    """
    try:
        # Вызов команды hcitool для получения RSSI
        result = subprocess.run(
            ["hcitool", "rssi", addr],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            # Извлечение RSSI из вывода команды
            output = result.stdout.strip()
            if "RSSI return value" in output:
                return int(output.split(":")[-1].strip())
        return None
    except Exception as e:
        print(f"Ошибка при получении RSSI для устройства {addr}: {e}")
        return None

if __name__ == "__main__":
    find_bluetooth_devices()