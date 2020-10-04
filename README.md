# calc_conditional_avg

## What Does it Do?

`calc_conditional_avg` Calculates an Average, conditionally. It takes the average of multiple sensors, but only includes that sensor in the average if a condition is met.

A use case for this would be to calculate the average temperature of any occupied rooms.

## Using it!

This works as an "app" in `pyscript`. Therefore, pyscript is required and configuration is done through Home Assistant's `configuration.yaml` file.

You can see a [full configuration example](config.sample.yaml) in this repository.

These are the configuration keys:

key | description | example | default
--- | --- | --- | ---
entity_id (required) | the full `entity_id` for this app to publish the calculation to. use caution to select an entity_id that is not already in use as this app will overwrite any existing value | sensor.conditional_avg | No Default
unit_of_measurement (optional) | the units for the sensor you are creating | °F | No Unit
friendly_name (optional) | the human readable name for this sensor | Conditional Average | entity_id
precision (optional) | the number of decimal places the result should be rounded to | 1 | 0
conditions (required) | a list of conditions | see below | No Default

  \
  \
Each Condition Should have the following keys:
key | description | example | default
--- | --- | --- | ---
condition (required) | a entity_id that will have a state of `on` when this sensor should be included in the average | binary_sensor.room1_occupied | No Default
entity (required) | the entity_id of the sensor whose value should be included in the average | sensor.room1_temperature | No Default



## Requirements

* [PyScript custom_component](https://github.com/custom-components/pyscript)

## Install

### Install this script
```
# get to your homeassistant config directory
cd /config

cd pyscript
mkdir -p apps/
cd apps
git clone https://github.com/dlashua/pyscript-calc_conditional_avg.git calc_conditional_avg
```

### Edit `configuration.yaml`

```yaml
pyscript:
  apps:
    calc_conditional_avg:
      - entity_id: sensor.avg_occupied_temperature
        unit_of_measurement: "°F"
        friendly_name: Avg Occupied Temperature
        precision: 1
        conditions:
          - condition: binary_sensor.room1_occupied
            entity: sensor.room1_temperature
          - condition: binary_sensor.room2_occupied
            entity: sensor.room2_temperature
```

### Reload PyScript
