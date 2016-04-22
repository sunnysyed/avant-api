# -*- coding: utf-8 -*-

db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])

auth = Auth(db, jwt = {'secret_key':'secret','user_param':'username','verify_expiration':False})
auth.settings.extra_fields['auth_user'] = EXTRA_AUTH_FIELDS
auth.settings.use_username = False
auth.settings.login_userfield = 'email'
#auth.settings.password_field = 'user_access_token'
#auth_jwt = AuthJWT(auth, secret_key='secret',pass_param='user_access_token')


## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.actions_disabled = ["register","login","request_reset_password"]
