import flask


from opentelemetry.sdk.resources import SERVICE_NAME, Resource



from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader


reader = PeriodicExportingMetricReader(OTLPMetricExporter(), export_interval_millis=5000)
metrics.set_meter_provider(MeterProvider(resource=Resource.create(), metric_readers=[reader]))

meter = metrics.get_meter("metrics-app")
requests_total = meter.create_counter("app_requests", description="Requests handled")

app = flask.Flask(__name__)

@app.route('/')
def main():
    return "Hello from metrics-app!"

@app.route('/vote')
def vote():
    requests_total.add(1)
    return "Vote received!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
