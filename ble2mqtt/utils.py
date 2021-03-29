MAX_RSSI = 10
MIN_RSSI = -87


def format_binary(data: bytes, delimiter=' '):
    return delimiter.join(format(x, '02x') for x in data)


def cr2032_voltage_to_percent(mvolts: int):
    return max(min(int(round((mvolts/1000 - 2.1), 2) * 100), 100), 0)


def rssi_to_linkquality(rssi):
    return round(255 * (rssi - MIN_RSSI)/(MAX_RSSI-MIN_RSSI))
