from flask import Flask, request, render_template
from explain import explain

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error = None
    url = ''
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if not url or ' ' in url or '.' not in url:
            error = 'Please enter a valid URL, for example https://example.com'
        else:
            result = explain(url)
    return render_template('index.html', result=result, error=error, url=url)

if __name__ == '__main__':
    app.run(debug=True)
