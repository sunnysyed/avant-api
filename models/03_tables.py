auth.define_tables(username=False, signature=False)

db.define_table('loan_application',
    Field('customer_id','reference auth_user'),    
    Field('loan_application_type', 'string'),
    Field('application_status', 'string'))

db.define_table('loan_application_attachments',
                Field('loan_application_id','reference loan_application'),
                Field('image','upload'),
                Field('image_url','string'))
