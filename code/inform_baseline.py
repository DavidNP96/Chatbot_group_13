

def classify_request(request, test_data):
    predictions = []
    for line in test_data:
        predictions.append("inform")
    return predictions


def process_incoming_string():
    request = input("Enter your value: ")
    return("inform")

if __name__ == "__main__":
    process_incoming_string()