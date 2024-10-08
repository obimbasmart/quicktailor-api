from enum import Enum


class OrderStageStatus(str, Enum):
    COMPLETED = 'completed'
    NOT_COMPLETED = 'not completed'


ORDER_STAGES = {
    "stage_one": {
        "id": 0,
        "title": "order comfirmed",
        "updated_at": None,
        "status": OrderStageStatus.NOT_COMPLETED.value
    },

    "stage_two": {
        "id": 1,
        "title": "material sourcing",
        "updated_at": None,
        "status": OrderStageStatus.NOT_COMPLETED.value
    },

    "stage_three": {
        "id": 2,
        "title": "sewing",
        "updated_at": None,
        "status": OrderStageStatus.NOT_COMPLETED.value
    },

    "stage_four": {
        "id": 3,
        "title": "packaging",
        "updated_at": None,
        "status": OrderStageStatus.NOT_COMPLETED.value
    },

    "stage_five": {
        "id": 4,
        "title": "ready for pickup",
        "updated_at": None,
        "status": OrderStageStatus.NOT_COMPLETED.value
    },

    "stage_six": {
        "id": 5,
        "title": "order is picked up",
        "updated_at": None,
        "status": OrderStageStatus.NOT_COMPLETED.value
    }
}
