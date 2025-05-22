from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re
import traceback

app = Flask(__name__)

def fetch_water_level():
    try:
        url = "https://www.fortum.com/se/om-oss/energiproduktion/vattenkraft/vattenkraftverk/gullspangsalven/gullspangs-kraftverk"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        match = re.search(r'Vattennivare:\s*\+([\d.,]+)\s*m', text)
        if match:
            return f"+{match.group(1)} m"
        else:
            return None
    except Exception:
            print(f"Error: {traceback.format_exc()}")
    
@app.route('/api/vattenniva')
def get_vattenniva():
    try:
        level = fetch_water_level()
        if level:
            return jsonify({'vattenniva': level})
        else:
            return jsonify({'error': 'Water level not found'}), 404
    except Exception:
            print(f"Error: {traceback.format_exc()}")
        
if __name__ == '__main__':
    app.run(host="192.168.50.50", port="9500", debug=False)