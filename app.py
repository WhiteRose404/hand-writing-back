from flask import Flask, request, jsonify
import base64
# import the prediction function
from prediction_utils import predict_number

# import the storage function
from storage_utils import store_model, fetch_model

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return 'The server is running!'




# storing objects
@app.route('/store', methods=['POST'])
def store():
    return 'The server is running!'


@app.route('/store/model', methods=['POST'])
def modelstorage():
    # Get the data from the POST request.
    # expect a raw data of binary.
    data = request.get_data();
    # store the object to the minio server
    result = store_model(data);
    if(result):
        return jsonify({'success': 'model stored'});
    else:
        return jsonify({'error': 'model not stored'});

@app.route('/fetch/model', methods=['GET'])
def modelfetch():
    # fetch the object from the minio server
    data = fetch_model();
    data_base64 = base64.b64encode(data).decode('utf-8')
    if(data):
        return jsonify({'success': 'model fetched', 'data': data_base64});
    else:
        return jsonify({'error': 'model not fetched'});
    # need to convert the data to base64

#  prediction serivce
@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)
    # check if the data is correct
    if('table' not in data):
        return jsonify({'error': 'no table'});
    table = data['table'];
    if(not isinstance(table, list)):
        return jsonify({'error': 'table must be a list'});
    if(len(table) != 28*28):
        return jsonify({'error': 'table must be 28x28'});
    # looks good, let's predict
    # call a function that will predict the number
    predict = predict_number(table)
    # predict = 12

    output = {
        'prediction': predict
    }
    return jsonify(output)





if __name__ == '__main__':
    app.run(debug=True)
