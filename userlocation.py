from flask import Flask, render_template

from flask_googlemaps import GoogleMaps

from flask_googlemaps import Map


app = Flask(__name__)


# you can set key as config
app.config['GOOGLEMAPS_KEY']="AIzaSyBxdUM2ckxVo812l3paw6ucJeJ6CYZXUj8"

# Initialize the extension
GoogleMaps(app)

# you can also pass the key here if you prefer

#GoogleMaps(app, key="AIzaSyAu2TgA9Rc-LXhNAanmN8s2UCSN2ayiySo")




@app.route('/', methods=["GET"])
def my_map():
    mymap = Map(

                identifier="view-side",

                varname="mymap",

                style="height:720px;width:1100px;margin:0;", # hardcoded!
				
				lat=37.4419, # hardcoded!

                lng=-122.1419, # hardcoded!

                zoom=15,

                markers=[(37.4419, -122.1419)] # hardcoded!

            )

    return render_template('userlocation.html', mymap=mymap)





if __name__ == "__main__":

    app.run(debug=True)