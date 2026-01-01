from enum import Enum


class DetectableObjectEnum(Enum):
    # NOTE: enum values must be kept in sync with values used in model(s)
    
    CAR = "car"
    MOTORBIKE = "motorbike"
    BICYCLE = "bicycle"
    BUS = "bus"
    TRUCK = "truck"
