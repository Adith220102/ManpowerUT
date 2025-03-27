# -*- coding: utf-8 -*-
"""main

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1V_nhngSdFiZn97SYhW9igxInwHmBPXtr
"""

!pip install fastapi uvicorn nest_asyncio

from fastapi import FastAPI
from pydantic import BaseModel
import nest_asyncio
import uvicorn

app = FastAPI()

facility_constants = {
    "Mumbai_KurlaWest_R": 0.075,
    "Mumbai_AshokNagar_R": 0.067,
    "Coimbatore_Pudhupalayam_R": 0.167,
}

class FacilityInput(BaseModel):
    facility_name: str
    dispatch_load: int
    touchpoints: int
    old_mandays: float

@app.post("/calculate/")
async def calculate_mandays(data: FacilityInput):
    if data.facility_name not in facility_constants:
        return {"error": "Invalid facility name"}

    setup_time_per_touchpoint = facility_constants[data.facility_name]
    setup_time = data.touchpoints * setup_time_per_touchpoint
    scanning_time = data.dispatch_load / 600
    total_time = setup_time + scanning_time
    mandays = round(total_time / 3.5, 2)

    response = {
        "processing_time": round(total_time, 2),
        "mandays_required": mandays,
    }

    if mandays < data.old_mandays:
        response["reduction"] = round(data.old_mandays - mandays, 2)
    else:
        response["message"] = "No need to change."

    return response

# Run FastAPI in Colab
nest_asyncio.apply()
uvicorn.run(app, host="0.0.0.0", port=7860)
