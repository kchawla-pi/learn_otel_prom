from typing import Union

import uvicorn
from fastapi import FastAPI
from opentelemetry import metrics


from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
# from opentelemetry.sdk import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter


meter_provider = MeterProvider(
                metric_readers=[
                    PeriodicExportingMetricReader(
                        ConsoleMetricExporter(), export_interval_millis=5000
                    ),
                    PeriodicExportingMetricReader(
                        OTLPMetricExporter(endpoint="collector:4317", insecure=True),
                        export_interval_millis=5000,
                    ),
                ]
            )
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(name="simple")
counter = meter.create_counter(name="api_calls")



app = FastAPI()


@app.get("/")
def read_root():
    counter.add(1)
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == '__main__':
    uvicorn.run(app, port=8193)
