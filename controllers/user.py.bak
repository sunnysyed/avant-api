# -*- coding: utf-8 -*-
@requires_post
def register():
    email = request.vars.email
    password = request.vars.password
    first_name = request.vars.first_name
    last_name = request.vars.last_name
    row = db.auth_user(email=email)

    if not row:
        row = db.auth_user.validate_and_insert(password=password,
                                 email=email, last_name=last_name, first_name=first_name)
        if row.errors:
            raise HTTP(401, response.json({'error' : row.errors}))
        data = {}
        data["access_token"] = generate_access_token()
        update_result = db(db.auth_user.email == email).validate_and_update(**data)
        return get_profile(db, row.id)
        

    else:
        raise HTTP(401, response.json({'error' : 'Email is already Registered'}))
# -*- coding: utf-8 -*-
@requires_post
def login():
    email = request.vars.email
    password = request.vars.password
    row = db.auth_user(email=email)
    if row:
        valid = db.auth_user.password.validate(password) == (db(db.auth_user.email==email).select ().first ().password, None)
        if (valid):
            return get_profile(db, row['id'])
        else:
            raise HTTP(401, response.json({'error' : 'Password is Incorrect'}))
        

    else:
        raise HTTP(401, response.json({'error' : 'Email is Incorrect'}))
    return response.json(row)


@requires_get
@requires_valid_token
def profile():
    user_id = session.auth_user_id
    return get_profile(db, user_id)
