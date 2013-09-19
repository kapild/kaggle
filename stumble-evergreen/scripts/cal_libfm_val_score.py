import sys

def get_label(val):
    if float(val) >= 0.5:
        return '1'
    else:
        return '0'


if __name__ == '__main__':
    actual_file_name = sys.argv[1]
    predict_file_name  = sys.argv[2]
    
    actual_file = open(actual_file_name, "r")
    predict_file = open(predict_file_name, "r")
    
    count = 0

    actual_lines = actual_file.readlines()
    
    true_prediction = 0
    for prediction in predict_file: 
        actual_label = actual_lines[count]
        actual_label = str(int(float(actual_label)))
        count+=1
        predict_label = get_label(prediction)
        if predict_label == actual_label:
            true_prediction+=1

    print float(true_prediction)/count * 100
    



