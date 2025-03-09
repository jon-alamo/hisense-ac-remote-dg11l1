import controller.features as features


class InvalidValue(ValueError):
    def __init__(self, enum: features.BaseEnum):
        valid_values = ", ".join(enum.values())
        message = f"'{enum.name}' parameter's value one of: {valid_values}"
        super().__init__(message)


class InvalidTemperature(ValueError):
    def __init__(self, name: str, range_values: list | tuple):
        message = f"{name.capitalize()} temperature must be between {range_values[0]} and {range_values[1]}"
        super().__init__(message)
