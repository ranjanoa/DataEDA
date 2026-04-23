import requests

def test_upload():
    print("Testing /upload...")
    with open("test_data.csv", "rb") as f:
        response = requests.post("http://127.0.0.1:8000/upload", files={"files": f})
    print("Upload Status:", response.status_code)
    print("Upload Response:", response.text)
    
def test_process():
    print("\nTesting /process...")
    response = requests.post("http://127.0.0.1:8000/process", data={"min_nonzero": 0.0, "merge_strategy": "linear"})
    print("Process Status:", response.status_code)
    print("Process Response:", response.text)

if __name__ == "__main__":
    test_upload()
    test_process()
