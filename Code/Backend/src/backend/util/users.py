import hashlib, binascii, os

class UserUtils():
    def __init__(self, db):
        self.db = db

    @property
    def execute_sql(self):
        return self.db.execute_sql

    @property
    def get_one_row(self):
        return self.db.get_one_row

    @property
    def get_rows(self):
        return self.db.get_rows

    def check_token(self, token):
        row = self.get_one_row('SELECT core_users_sessions.user_id FROM core_users_sessions INNER JOIN core_tokens ON core_users_sessions.token_id=core_tokens.token_id WHERE core_tokens.token=%s', [token])

        if row == None:
            return False
        return True

    def create_user(self, user):
        hashed_password = self.hash_password(user['password'])

        self.execute_sql('INSERT INTO core_users (username, email, password) VALUES (%s, %s, %s)', [user['name'], user['email'], hashed_password])

    def create_session(self, uid):
        token = self.generate_token()

        result = self.execute_sql('INSERT INTO core_tokens (token, token_type) VALUES (%s, %s)', [token, 3])
        result = self.execute_sql('INSERT INTO core_users_sessions (user_id, token_id) VALUES (%s, %s)', [uid, result])

        if result == None:
            return -1
        return token

    def destroy_session(self, token):
        result = self.execute_sql('DELETE S FROM core_users_sessions S INNER JOIN core_tokens ON core_tokens.token_id=S.token_id WHERE core_tokens.token = %s', [token])

        if result == 1:
            return True
        return False

    def generate_token(self):
        # 1 on 8 billion chance of returning the same token twice, seen as "good enough"
        return hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')

    def hash_password(self, plain):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verify_password(self, hashed, plain):
        salt = hashed[:64]
        hashed = hashed[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      plain.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == hashed
