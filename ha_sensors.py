from typing import Type
from mqtt_homeassistant_utils import HAAvailability, HADevice, HASensor, HABinarySensor, HASensorEnergy, HASensorBattery, HASensorTemperature, HADeviceClassSensor, HADeviceClassBinarySensor

def createSensors(nodeId: str, hadevice: HADevice, qos: int):
    
    def createBlueprint(classType: Type, nodeId: str, device: HADevice, name: str, **kwargs):
        # Check if classType is a known class
        if isinstance(classType, type):
            
            avail = HAAvailability(topic=nodeId + "/state")

            # Create instance of wanted class
            return classType(
                state_topic=nodeId + "/values",
                node_id=nodeId,
                name=name,
                device=device,
                qos=qos,
                availability=avail,
                **kwargs
            )
        else:
            raise ValueError("The provided type is not a class.")

    sensors = []

    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Betriebsart", device_class=HADeviceClassSensor.ENUM, icon="mdi:knob"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "BSZ EQ Betriebsstunden", device_class=HADeviceClassSensor.DURATION, unit_of_measurement="h", icon="mdi:wrench-clock", suggested_display_precision=0))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "BSZ EQ Schaltungen", icon="mdi:counter", suggested_display_precision=0))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "BSZ HKP Betriebsstunden", device_class=HADeviceClassSensor.DURATION, unit_of_measurement="h", icon="mdi:wrench-clock", suggested_display_precision=0))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "BSZ HKP Schaltung", icon="mdi:counter", suggested_display_precision=0))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "BSZ Verdichter akt. Laufzeit", device_class=HADeviceClassSensor.DURATION, unit_of_measurement="s", icon="mdi:wrench-clock", suggested_display_precision=0))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "BSZ Verdichter Betriebsst. ges", device_class=HADeviceClassSensor.DURATION, unit_of_measurement="h", icon="mdi:wrench-clock", suggested_display_precision=0))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "BSZ Verdichter Betriebsst. HKR", device_class=HADeviceClassSensor.DURATION, unit_of_measurement="h", icon="mdi:wrench-clock", suggested_display_precision=0))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "BSZ Verdichter Betriebsst. WW", device_class=HADeviceClassSensor.DURATION, unit_of_measurement="h", icon="mdi:wrench-clock", suggested_display_precision=0))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "BSZ Verdichter Schaltung WW", icon="mdi:counter"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "BSZ Verdichter Schaltungen", icon="mdi:counter"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "BSZ WWV Betriebsstunden", device_class=HADeviceClassSensor.DURATION, unit_of_measurement="h", icon="mdi:wrench-clock"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "BSZ WWV Schaltungen", icon="mdi:counter"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "BSZ ZIPWW Betriebsstunden", device_class=HADeviceClassSensor.DURATION, unit_of_measurement="h", icon="mdi:wrench-clock"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "BSZ ZIPWW Schaltungen", icon="mdi:counter"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Energiezaehler", icon="mdi:counter"))
    sensors.append(createBlueprint(HABinarySensor, nodeId, hadevice, "EQ Pumpe (Ventilator)", device_class=HADeviceClassBinarySensor.RUNNING, icon="mdi:pump"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Frischwasserpumpe"))
    sensors.append(createBlueprint(HABinarySensor, nodeId, hadevice, "FWS Stroemungsschalter", device_class=HADeviceClassBinarySensor.RUNNING, icon="mdi:light-switch-off"))
    sensors.append(createBlueprint(HABinarySensor, nodeId, hadevice, "FWS Type"))
    sensors.append(createBlueprint(HABinarySensor, nodeId, hadevice, "Hauptschalter", device_class=HADeviceClassBinarySensor.RUNNING, icon="mdi:light-switch-off"))
    sensors.append(createBlueprint(HABinarySensor, nodeId, hadevice, "Heizkreispumpe", device_class=HADeviceClassBinarySensor.RUNNING, icon="mdi:pump"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "HKR Absenktemp. (K)", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="K", icon="mdi:thermometer-chevron-down", suggested_display_precision=0))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "HKR Aufheiztemp. (K)", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="K", icon="mdi:thermometer-chevron-up", suggested_display_precision=0))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "HKR Heizgrenze", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer-high"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "HKR RLT Soll_0 (Heizkurve)", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer-lines"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "HKR RLT Soll_oHG (Heizkurve)", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer-lines"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "HKR RLT Soll_uHG (Heizkurve)", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer-lines"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "HKR Soll_Raum", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:home-thermometer-outline"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "HKR_Sollwert", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:home-thermometer-outline"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Hochdruck (bar)", device_class=HADeviceClassSensor.PRESSURE, unit_of_measurement="bar", icon="mdi:gauge"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Niederdruck (bar)", device_class=HADeviceClassSensor.PRESSURE, unit_of_measurement="bar", icon="mdi:gauge"))
    sensors.append(createBlueprint(HABinarySensor, nodeId, hadevice, "Puffer Type"))
    sensors.append(createBlueprint(HABinarySensor, nodeId, hadevice, "Stoerung", device_class=HADeviceClassBinarySensor.PROBLEM, icon="mdi:alert"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Temp. Aussen", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Temp. Aussen verzoegert", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Temp. Brauchwasser", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Temp. EQ_Austritt", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Temp. EQ_Eintritt", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Temp. Frischwasser_Istwert", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Temp. Heissgas", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Temp. Kondensation", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Temp. Ruecklauf", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Temp. Sauggas", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Temp. Verdampfung", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Temp. Vorlauf", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer"))
    sensors.append(createBlueprint(HABinarySensor, nodeId, hadevice, "Verdichter", device_class=HADeviceClassBinarySensor.RUNNING, icon="mdi:pump"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Verdichter Einschaltverz.(sec)", device_class=HADeviceClassSensor.DURATION, unit_of_measurement="s", icon="mdi:timer-lock-outline"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Verdichter laeuft seit", device_class=HADeviceClassSensor.DURATION, unit_of_measurement="h", icon="mdi:wrench-clock"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Verdichter_Status"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "Verdichteranforderung"))
    sensors.append(createBlueprint(HABinarySensor, nodeId, hadevice, "Warmwasservorrang", device_class=HADeviceClassBinarySensor.RUNNING, icon="mdi:priority-high"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "WP_System"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "WW Hysterese Minimaltemp.", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer-water"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "WW Hysterese Normaltemp.", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer-water"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "WW Minimaltemp.", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer-water"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "WW Normaltemp.", device_class=HADeviceClassSensor.TEMPERATURE, unit_of_measurement="°C", icon="mdi:thermometer-water"))
    sensors.append(createBlueprint(HASensor, nodeId, hadevice, "WW Type"))
    sensors.append(createBlueprint(HABinarySensor, nodeId, hadevice, "Zirkulationspumpe WW", device_class=HADeviceClassBinarySensor.RUNNING, icon="mdi:pump"))

    return sensors
