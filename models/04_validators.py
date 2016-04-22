db.loan_application.customer_id.requires = IS_IN_DB(db,db.auth_user)
db.loan_application.loan_application_type.requires = IS_IN_SET(VALID_LOAN_TYPES)
db.loan_application.application_status.requires = IS_IN_SET(VALID_APPLICATION_STATUSES)
db.loan_application.application_status.default = 'incomplete'
db.loan_application_attachments.loan_application_id.requires = IS_IN_DB(db,db.loan_application)
db.loan_application_attachments.image.requires = IS_IMAGE()
