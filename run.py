from planty import app

app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])
