from planty import app
from planty.models import connect_to_db

connect_to_db(app)

app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])
