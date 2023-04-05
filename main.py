from app import app
from waitress import serve
if __name__ == '__main__':
    # serve(app, host="0.0.0.0", port=8080)
    app.run(debug=True,host='0.0.0.0',port='8080')

