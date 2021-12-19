from flask import Flask, jsonify,request
import time
import operator

app=Flask(__name__)

counters=[]


def makeStats(start_range , end_range):
    filtered = []
    for dict in counters:
        if dict['timestamp'] < end_range and dict['timestamp'] > start_range:
            filtered.append(dict)
    domains_request_counter = {}
    for dict in filtered:
        for key, value in dict.items():
            if key != "timestamp":
                if key not in domains_request_counter:
                    domains_request_counter[key] = value
                else:
                    domains_request_counter[key] += value
    topTenDomains = sorted(domains_request_counter.items(), key=operator.itemgetter(1), reverse=True)[:10]
    return topTenDomains


@app.route('/counters', methods=['POST'])
def create_counter():
    request_data=request.get_json()
    request_data[ 'timestamp']=int(time.time())
    counters.append(request_data)
    print(request_data)
    return jsonify(request_data)

@app.route('/counters')
def get_conters():
    return jsonify({'counters':counters})

@app.route('/stats/minutes')
def get_minutes_stats():
    now=int(time.time())
    end_range=int(now//60 * 60)
    start_range = end_range - 60
    topTenDomains=makeStats(start_range,end_range)
    return jsonify({"Top ten domains" :topTenDomains})

@app.route('/stats/hours')
def get_hours_stats():
    now=int(time.time())
    end_range = now - now % 3600
    start_range=end_range-3600
    topTenDomains = makeStats(start_range, end_range)
    return jsonify({"Top ten domains" :topTenDomains})


app.run(port=5000)