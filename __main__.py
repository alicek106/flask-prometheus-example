from flask import Response, Flask, request
import prometheus_client
from prometheus_client import Summary, Counter, Histogram, Gauge

# Flask
app = Flask(__name__)

# Example values
example_summary = Summary('alicek106_summary', 'Summary example')
example_summary.observe(5.5)

example_histogram = Histogram('alicek106_histogram', 'Histogram example', buckets=(1, 5, 10, 50, 100, 200, 500, 1000))
example_histogram.observe(1)
example_histogram.observe(5)
example_histogram.observe(10)
example_histogram.observe(100)

example_counter = Counter('alicek106_counter', 'Counter example')

rate_example_gauge = Gauge('alicek106_gauge', 'Gauge example for rate()')
rate_example_gauge.set(5)
initial_value = 5
offset_value = 5

## group_left example. It should be 'counter' type if you want to use.

methods = ["get", "get", "put", "post", "post"]
queries = [500, 404, 501, 500, 404]
values = [24, 30, 3, 6, 21]
error_gauge = Gauge('alicek106_http_errors', 'Test', ['method', 'code'])
for i in range(0, len(methods)):
    error_gauge.labels(methods[i], queries[i]).set(values[i])

method_success = ["get", "del", "post"]
values_success = [600, 34, 120]
success_gauge = Gauge('alicek106_http_requests', 'Test', ['method', 'success_message'])
for i in range(0, len(method_success)):
    success_gauge.labels(methods[i], 'success').set(values_success[i])

##

@app.route("/update/count", methods=["GET"])
def update_count():
    example_counter.inc()
    return requests_count()

@app.route("/update/histogram", methods=["GET"])
def update_histogram():
    k = float(request.args.get('value'))
    example_histogram.observe(k)
    return requests_count()

@app.route("/metrics")
def requests_count():
    result = []

    global initial_value
    initial_value = initial_value + offset_value
    rate_example_gauge.set(initial_value)

    result.append(prometheus_client.generate_latest(rate_example_gauge))
    result.append(prometheus_client.generate_latest(example_counter))
    result.append(prometheus_client.generate_latest(example_histogram))
    result.append(prometheus_client.generate_latest(example_summary))
    result.append(prometheus_client.generate_latest(error_gauge))
    result.append(prometheus_client.generate_latest(success_gauge))
    return Response(result, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)