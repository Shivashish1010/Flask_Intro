from flask import Flask, request, jsonify, render_template, redirect, Response
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:12345@localhost/test_flask_db'
db = SQLAlchemy(app)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    type = db.Column(db.String(20))

    def __repr__(self):
        return '<Assignment %r>' % self.id

def calculate_value(data):
    curr_value = 0
    for ele in data:
        if ele.type == "increment":
            curr_value += ele.value
        else:
            curr_value -= ele.value

    return(curr_value)


@app.route('/', methods=['POST', 'GET']) #home
def home():
    if request.method == "POST":
        pass
    else:
        return render_template("index.html")


@app.route('/events', methods=['GET']) #show all
def all_events():
    values = Assignment.query.all()
    return render_template("events.html", values=values)

@app.route('/value', methods=['GET']) #show current value
def curr_value():
    values = Assignment.query.all()
    curr_value = calculate_value(values)

    return render_template("current_value.html", value = curr_value)

@app.route('/events/<int(signed=True):id>', methods=['GET']) #show value upto point t
def value_upto_t(id):
    values = Assignment.query.all()

    temp_list = []
    print(id)
    if id>0:
        try:
            for i in range(id):
                temp_list.append(values[i])
                curr_value = calculate_value(temp_list)

        except IndexError:
            pass

    else:
        return Response(
            "give positive values",
            status=400,
        )

    return render_template("current_value.html", value=curr_value)

@app.route('/event', methods=['POST']) #add new value
def add_value():
    data = request.json
    print(data)
    # return jsonify(data)
    new_value = Assignment(value=data.get('value', None) ,type=data.get('type', None))
    print(new_value.value)
    try:
        db.session.add(new_value)
        db.session.commit()
        return jsonify(data)

    except:
        print("exception")

if __name__ == "__main__":
    app.run(debug=True)