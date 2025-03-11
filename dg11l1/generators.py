import json
import dg11l1.features as features

base_parameters = {
    "manufacturer": "Hisense",
    "supportedModels": ["DG11L1-12"],
    "supportedController": "Broadlink",
    "commandsEncoding": "Base64",
    "minTemperature": 16.0,
    "maxTemperature": 30.0,
    "precision": 1.0,
    "remoteThermostat": True,
    "minThermostatTemperature": 0,
    "maxThermostatTemperature": 36,
    "operationModes": [
        "heat",
        "cool",
        "fan",
        "dry"
    ],
    "fanModes": [
        "low",
        "medium_low",
        "medium",
        "medium_high",
        "high",
        "auto"
    ],
    "commands": {

    }
}


def generate_smart_ir_template(output: str):
    """ Method to generate a smart ir template for Hisense ac controller.
    """
    base_parameters["commands"]["off"] = features.get_remote_action_message_b64(state=features.States.off.value)
    for mode in base_parameters["operationModes"]:
        if mode not in base_parameters["commands"]:
            base_parameters["commands"][mode] = {}
        for fan_mode in base_parameters["fanModes"]:
            if fan_mode not in base_parameters["commands"][mode]:
                base_parameters["commands"][mode][fan_mode] = {}
            for temperature in range(int(base_parameters["minTemperature"]), int(base_parameters["maxTemperature"]) + 1):
                base_parameters["commands"][mode][fan_mode][str(temperature)] = features.get_remote_action_message_b64(
                    mode=mode,
                    fan_mode=fan_mode,
                    temperature=temperature
                )
    if base_parameters.get("remoteThermostat"):
        base_parameters["commands"]["thermostat"] = {}
        for temp in range(base_parameters["minThermostatTemperature"], base_parameters["maxThermostatTemperature"] + 1):
            base_parameters["commands"]["thermostat"][str(temp)] = features.get_remote_action_message_b64(
                ifeel_temp=temp
            )
    with open(output, 'w') as f:
        json.dump(base_parameters, f, indent=4)
