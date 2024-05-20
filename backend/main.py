#create
#first_name
#last_name
#email
#phone_number
from flask import request, jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts =  list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})

#creating contact
@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    phone_number = request.json.get("phoneNumber")

    if not first_name or not last_name or not email or not phone_number:
        return (
            jsonify({"message": "You must include a first name, last name, email and phone number"}), 400,
        )

    new_contact = Contact(first_name=first_name, last_name=last_name, email= email, phone_number=phone_number)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}),400
    
    return jsonify({"message": "User created!"}),201

#updating contact
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)
    contact.phone_number = data.get("phoneNumber", contact.phone_number)

    db.session.commit()

    return jsonify({"message": "User updated"}), 200

#deleting contact
@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
