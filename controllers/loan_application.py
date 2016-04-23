@requires_post
@requires_valid_token
def create():
    loan_type = request.vars.loan_type
    if not loan_type:
        raise HTTP(500, response.json({'error' : 'Invalid loan_type.'}))
    user_id = session.auth_user_id
    row = db.loan_application.validate_and_insert(customer_id=user_id, application_status="incomplete", loan_application_type=loan_type)
    if row.errors:
        raise HTTP(500, response.json({'error' : 'Invalid loan_type.'}))
    return get_profile(db, user_id)


@requires_post
@requires_valid_token
def upload_attachment():
    loan_application_id = request.vars.loan_application_id
    image = request.vars.image
    if not loan_application_id:
        raise HTTP(500, response.json({'error' : 'loan_application_id not set'}))
    if not image.filename :
        raise HTTP(500, response.json({'error' : 'image not set'}))
      
    row = db.loan_application_attachments.validate_and_insert(loan_application_id=loan_application_id, image=image)
    if (row.errors):
        raise HTTP(500, response.json({'error' : 'Could not upload Attachment please try again.'}))
    row = db.loan_application_attachments(id=row.id)
    data = {}
    data["image_url"] = URL('default','download',args=row["image"],host=True,scheme=True)
    update_result = db(db.loan_application_attachments.id == row.id).validate_and_update(**data)
    return get_profile(db, session.auth_user_id)

@requires_get
def loan_types():
    return response.json({"loan_types" : VALID_LOAN_TYPES})
