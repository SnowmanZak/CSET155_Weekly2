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


@app.route('/boatDelete', methods = ['GET'])
def findBoat():
    return render_template('delete.html')



@app.route('/boatDelete', methods = ['POST'])
def deleteBoat():
    try:
        delete_id = request.form['delete_id']
        result = conn.execute(text("delete from boats where id = :delete_id"), {'delete_id': delete_id})
        conn.commit()

        if result.rowcount > 0:
            return render_template('delete.html', success="Boat deleted successfully", error=None)
        else:
            return render_template('delete.html', success=None, error="No boat found with that ID")
    except:
        return render_template('delete.html', success=None, error="Failed to delete boat")



@app.route('/boatUpdate', methods = ['GET'])
def locateBoat():
    return render_template('update.html')


@app.route('/boatUpdate', methods = ['POST'])
def updateBoat():
    try:
        update_id = request.form.get('update_id')

        if not update_id:
            return render_template('update.html', error="Please enter a boat ID", boat_data=None)

        result = conn.execute(text("SELECT * FROM boats WHERE id = :update_id"), {'update_id': update_id})
        boat = result.fetchone()

        if boat:
            return render_template('update.html', boat_data=boat, error=None)
        else:
            return render_template('update.html', error="No boat found with that ID", boat_data=None)
    
    except:
        return render_template('update.html', error="Failed to search for boat", boat_data=None)

@app.route('/boatUpdateConfirm', methods=['POST'])
def updateBoatConfirm():
    try:
        boat_id = request.form.get('boat_id')
        name = request.form.get('name')
        type = request.form.get('type')
        owner_id = request.form.get('owner_id')
        rental_price = request.form.get('rental_price')

        result = conn.execute(
            text("""
                UPDATE boats
                SET name = :name, type = :type, owner_id = :owner_id, rental_price = :rental_price
                WHERE id = :boat_id
            """),
            {'name': name, 'type': type, 'owner_id': owner_id, 'rental_price': rental_price, 'boat_id': boat_id}
        )
        conn.commit()

        if result.rowcount > 0:
            return render_template('update.html', success="Boat updated successfully", error=None)
        else:
            return render_template('update.html', error="Failed to update boat", success=None)
    
    except:
        return render_template('update.html', error="Failed to update boat", success=None)



if __name__ == '__main__':
    app.run(debug = True)

