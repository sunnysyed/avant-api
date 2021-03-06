def requires_post(callee):
    def wrapper():
        if request.env.request_method != 'POST':
            raise HTTP(500, response.json({'error' : 'Method Not Supported'}))
        else:
            return callee()
    return wrapper

def requires_get(callee):
    def wrapper():
        if request.env.request_method != 'GET':
            raise HTTP(500, response.json({'error' : 'Method Not Supported'}))
        else:
            return callee()
    return wrapper

def requires_get_or_post(callee):
    def wrapper():
        if request.env.request_method not in ['GET','POST']:
            raise HTTP(500, response.json({'error' : 'Method Not Supported'}))
        else:
            return callee()
    return wrapper


 
def requires_valid_token(callee):
    def wrapper():
        token_in_header = request.env.http_authorization
        if token_in_header:
            parts = token_in_header.split()
            if parts[0].lower() != 'bearer':
                raise HTTP(401, response.json({'error' : 'Invalid JWT header'}))
            elif len(parts) == 1:
                raise HTTP(401, response.json({'error' : 'Invalid JWT header, missing token'}))
            elif len(parts) > 2:
                raise HTTP(401, response.json({'error' : 'Invalid JWT header, token contains spaces'}))
            token = parts[1]
        else:
            token = request.vars._token
        table = db.auth_user
        query = table.access_token == token
        valid_token = not db(query).isempty()
        
        if valid_token:
            auth_user = db(query).select(table.id).first()
            auth_user_id = auth_user.id
            session.auth_user_id = auth_user_id
            return callee()
        else:
            raise HTTP(401, response.json({'error' : 'Not Authorized'}))
    return wrapper



def requires_valid_access_code(callee):
    def wrapper():
        data = request.post_vars
                
        phone_number = data.get('phone_number', False)
        access_code = data.get('access_code', False)
        
        if not (phone_number and access_code):
            raise HTTP(403, response.json({'error' : 'Malformed Request'}))
    
        oldest_allowed_code = request.utcnow - datetime.timedelta(minutes=VERIFICATION_CODE_EXPIRATION_MINUTES)
    
        # Check for a code that matches the phone and is new enough
        
        table = db.user_access_codes
                
        query = table.phone_number == phone_number
        query &= table.access_code == access_code
        query &= table.issued_at >= oldest_allowed_code
        
        valid_code = not db(query).isempty() 
        
        if valid_code:
            return callee()
        else:
            raise HTTP(401, response.json({'error' : 'Not Authorized'}))
    return wrapper

def generate_phone_token(size=5, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_access_token():
    token = generate_phone_token()
    return token

def get_profile(db, user_id):
    result = {}
    row = db.auth_user(id=user_id)
    result["profile"] = row
    table = db.loan_application
    query = table.customer_id == row["id"]
    loan_applications = db(query).select()
        
    loan_applications_ids = [row.id for row in loan_applications]
    
    table = db.loan_application_attachments
    query = table.loan_application_id.belongs(loan_applications_ids)
    
    loan_application_attachments = db(query).select()

    result["loan_applications"] = []
    
    for loan_application in loan_applications:
        loan_application["loan_application_attachments"] = []
        for loan_application_attachment in loan_application_attachments:
            if (loan_application_attachment.loan_application_id == loan_application.id):
                loan_application["loan_application_attachments"].append(loan_application_attachment)    
    result["loan_applications"] = loan_applications
    return response.json(result)
    

def handle_photo_updates(s,f):
    row = s.select().first()
    
    for photo_index in range(1,6):
        photo_index = str(photo_index)

        for profile_side in ["client","hero"]:
            photo_file_key = profile_side + '_photo_' + photo_index + '_file'
            photo_url_key = profile_side + '_photo_' + photo_index + '_url'        
            
            if f.get(photo_file_key,False):
                filename = row[photo_file_key]
                url = URL('default','download',args=filename,host=True,scheme=True)
                photo_update = {photo_url_key:url}
                row.update_record(**photo_update)
