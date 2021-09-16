

def classify_request(sents, labels):
    predictions = []
    y_true = 0
    y_pred = 0
    positives = 0
    for line, label in zip(sents, labels):
        if label == "inform":
            y_true += 1
            positives += 1
        
        y_pred += 1
    return y_true, y_pred, positives 


def process_incoming_string():
    request = input("Enter your value: ")
    return("inform")

if __name__ == "__main__":
    process_incoming_string()