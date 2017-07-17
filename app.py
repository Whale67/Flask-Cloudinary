from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

client = MongoClient(app.config['MONGO_URI'])


#html template that will launch cloudinary upload widget
@app.route('/cloudinary_upload')
def cloudinary_upload():
    return render_template('cloudinary.html')

#creates a public id for the user. Allows every upload to be store with logged in user's username hash
@app.route('/create_public_id')
@login_required
def create_public_id(find_user,users):
    public_id_1 = find_user['username'].encode('utf-8')
    public_id = hashlib.sha1(public_id_1).hexdigest()
    users.update(find_user, {'$set': { 'public_id' : public_id}})
    return redirect(url_for('upload_image'))

#renders the template to begin the upload
@app.route('/upload_image')
@login_required
def upload_image(find_user,users):
    title = '- Profile Image'
    return render_template('cloudinary.html', find_user=find_user, title=title)

#receives public_id and version from the widget 
@app.route('/image_id', methods=['POST'])
@login_required
def image_id(find_user,users):
    public_id = request.form['public_id']
    version = request.form['version']
    users.update(find_user, {'$set':{'profile_image_url' : version + '/' + public_id, 'public_id' : public_id, 'version' : version}})
    return 'Thank you for your upload'

#signature that must be matched to Cloudinary signature. Allows for overriding previous user uploads    
@app.route('/signature', methods=['POST'])
def signature():
    values = request.values
    timestamp = values.get('data[timestamp]')
    public_id = values.get('data[public_id]')
    custom_coordinates = values.get('data[custom_coordinates]')
    api_secret = app.config['CLOUDINARY_API_SECRET']
    signature = 'callback=https://widget.cloudinary.com/cloudinary_cors.html&custom_coordinates=%s&public_id=%s&timestamp=%s&upload_preset=thka8ije%s' % (custom_coordinates,public_id,timestamp,api_secret)
    signature2 = signature.encode('utf-8')
    h = hashlib.sha1(signature2).hexdigest()
    return '%s' % (h)

if __name__ == '__main__':
    app.run()