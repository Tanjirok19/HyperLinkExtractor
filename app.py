from flask import Flask

app = Flask(__name__)

# Your app routes and logic here

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
