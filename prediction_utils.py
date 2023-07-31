import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model

from storage_utils import fetch_model

def getOutput(arr):
    max = 0
    index = 0;
    winner = 0;
    for num in arr[0]:
        num = float(num)
        print("------------- indice:", index, round(num, 4))
        if( num > max ):
            max = num;
            winner = index;
        index += 1;
    return winner


def predict_number(table):
    
    # if(not model):
    #     return jsonify({'error': 'model not fetched'});
    
    # tmp 
    # cwd = Path.cwd().parent / 'mldev' / 'data' / 'model.keras';
    ############################################################
    # load the model
    # get the model from the minio server
    cwd = None;
    try:
        cwd = fetch_model();
    except e:
        return jsonify({'error': 'model not fetched'});
    
    if(not cwd):
        return jsonify({'error': 'model not fetched'});

    model = load_model(cwd);
    # reshape the table
    table = tf.cast(tf.reshape(table, (1, 28*28)), tf.float32);
    # predict
    raw_prediction = model.predict(table);
    # apply softmax
    prediction = getOutput(tf.nn.softmax(raw_prediction));
    # get the index of the highest value
    print(prediction)
    return prediction;
    