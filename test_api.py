import requests

url_upload = 'http://127.0.0.1:8000/upload'
url_process = 'http://127.0.0.1:8000/process'
url_derived = 'http://127.0.0.1:8000/add-derived'

with open(r'adana\adana_complete_merged_data29062026 (3).csv', 'rb') as f:
    files = [('files', ('adana.csv', f, 'text/csv'))]
    r = requests.post(url_upload, files=files)
    print("Upload:", r.status_code, r.text[:100])

r_proc = requests.post(url_process, data={'file_index': 0})
print("Process:", r_proc.status_code)

data = {
    'name': 'Total_Coal_Flow',
    'formula': 'Consumption Hood Total Coal + Consumption Calciner Total Coal'
}
r2 = requests.post(url_derived, data=data)
print("Derived 1:", r2.status_code, r2.text)
