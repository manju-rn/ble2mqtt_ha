# Service to export BLE devices to MQTT with Home Assistant discovery

## !!! It is a very early alpha release !!! 

**Use this software at your own risk.**

Default config should be located in `/etc/ble2mqtt.json` or 
can be overridden with `BLE2MQTT_CONFIG` environment variable.

Example run command:

```sh 
BLE2MQTT_CONFIG=./ble2mqtt.json ble2mqtt
```

The configuration file is a JSON with the following content:

```json
{
    "mqtt_host": "localhost",
    "mqtt_port": 1883,
    "mqtt_user": "",
    "mqtt_password": "",
    "log_level": "INFO",
    "devices": [
        {
            "address": "11:22:33:aa:cc:aa",
            "type": "presence"
        },
        {
            "address": "11:22:33:aa:bb:cc",
            "type": "redmond200",
            "key": "ffffffffffffffff"
        },
        {
            "address": "11:22:33:aa:bb:cd",
            "type": "mikettle",
            "product_id": 275
        },
        {
            "address": "11:22:33:aa:bb:dd",
            "type": "xiaomihtv1"
        },
        {
            "address": "11:22:34:aa:bb:dd",
            "type": "xiaomihtv1",
            "passive": false
        },
        {
            "address": "11:22:33:aa:bb:ee",
            "type": "xiaomilywsd"
        },
        {
            "address": "11:22:33:aa:bb:ff",
            "type": "xiaomilywsd_atc"
        },
        {
            "address": "11:22:33:aa:aa:aa",
            "type": "atomfast"
        }
    ]
}
```

You can omit a line, then default value will be used.

Supported devices:

**Any device**
- Any bluetooth device can work as a presence tracker

**Kettles:**
- Redmond G2xx series (redmond200)
  The default key that is used is `"ffffffffffffffff"`
  and can be omitted in the config.
  In some cases kettles don't accept it. Just use another 
  key in the config file for the device: 
  `"key": "16 random hex numbers"`
- Mi Kettle (mikettle)
  Use correct `product_id` for your kettle:
  - yunmi.kettle.v1: `131`
  - yunmi.kettle.v2: `275` (default)
  - yunmi.kettle.v7: `1116`

**Humidity sensors:**
- Xiaomi MJ_HT_V1 (xiaomihtv1)
- Xiaomi LYWSD03MMC (xiaomilywsd)
- Xiaomi LYWSD03MMC with custom ATC firmware (xiaomilywsd_atc)

**Dosimeters**
- Atom Fast (atomfast)

By default, a device works in the passive mode without connection by 
listening to advertisement packets from a device.
To use connection to the device provide `"passive": false` parameter.

**Supported devices in passive mode:**
- Xiaomi MJ_HT_V1 (xiaomihtv1)
- Xiaomi LYWSD03MMC with custom ATC firmware (xiaomilywsd_atc)


## OpenWRT installation

Execute the following commands in the terminal:

```shell script
opkg update
opkg install python3-pip python3-asyncio
pip3 install "bleak>=0.11.0"
pip3 install -U ble2mqtt
```

Create the configuration file in /etc/ble2mqtt.json and
append your devices.

Bluetooth must be turned on.

```shell script
hciconfig hci0 up
```

Run the service in background

```shell script
ble2mqtt 2> /tmp/ble2mqtt.log &
```

## Container

Build the image as:

```shell script
podman build -t ble2mqtt:dev .
```

Start the container and share the config file and DBus for Bluetooth connectivity:
```shell script
podman run \
-d \
--net=host \
-v $PWD/ble2mqtt.json.sample:/etc/ble2mqtt.json:z \
-v /var/run/dbus:/var/run/dbus:z \
ble2mqtt:dev
```

Instead of sharing `/var/run/dbus`, you can export `DBUS_SYSTEM_BUS_ADDRESS`.

NOTE: `--net=host` is required as it needs to use the bluetooth interface
