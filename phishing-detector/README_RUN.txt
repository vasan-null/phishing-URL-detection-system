HOW TO RUN (Windows)
1. Install Python 3.9+ from python.org (tick "Add Python to PATH").
2. Open this folder in VS Code (File > Open Folder), then open Terminal > New Terminal.
3. pip install -r requirements.txt
4. python train.py     (creates phish_model.pkl)
5. python app.py       (starts the web app)
6. Open http://127.0.0.1:5000 in your browser.

NOTE: data/urls.csv is only a tiny DEMO file made so the code runs.
For your project, replace it with a real labelled dataset
(columns: url,label  where 1 = phishing, 0 = legitimate) and run train.py again.
