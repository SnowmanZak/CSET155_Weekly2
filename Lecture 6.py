from flask import Flask, render_template, request
from sqlalchemy import create_engine, text


app = Flask(__name__)
# connection string
conn_str = "mysql://root:cset155@localhost/boatdb"
engine = create_engine(conn_str, echo = True)
conn = engine.connect()




@app.route('/')
def greeting():
    return render_template('index.html')


# @app.route('/<name>')
# def hello(name): 
#     return render_template('user.html', name = name)


# @app.route('/num/<int:number>')
# def num(number):
#     return f"The next number is {number + 1}"

@app.route('/Boats')
def boats():
    boats = conn.execute(text("select * from boats")).all()
    return render_template('boats.html', boats = boats)


@app.route('/boatCreate', methods = ['GET'])
def getBoat():
     return render_template('boat_create.html')


@app.route('/boatCreate', methods = ['POST'])
def createBoat():
    try:
        conn.execute(text("insert into boats values (:id, :name, :type, :owner_id, :rental_price)"), request.form)
        conn.commit()
        return render_template('boat_create.html', error = None, success = "Successful")
    except:
        return render_template('boat_create.html', error = "Failed", success = None)

@app.route('/boatSearch', methods = ['GET'])
def searchBoat():
    return render_template('search.html')

@app.route('/boatSearch', methods = ['POST'])
def returnBoat():
    try:
        search_id = request.form['search_id']
        result = conn.execute(text("select * from boats where id = :search_id"), {'search_id': search_id})
        boats = result.fetchall()  
        if boats:
            boat_data = boats[0]  
            return render_template('search.html', boat_data=boat_data, error=None, success="Found boat")
        else:
            return render_template('search.html', error="No boat found with that ID", success=None)
    except:
        return render_template('search.html', error="Failed", success=None)

@app.route('/boatDelete')
def deleteBoat():
    return render_template('delete.html')


@app.route('/boatUpdate')
def updateBoat():
    return render_template('update.html')



if __name__ == '__main__':
    app.run(debug = True)

