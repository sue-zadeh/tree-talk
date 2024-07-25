

# These details are available on the first MySQL Workbench screen
# Usually called 'Local Instance'
dbuser = "root" #PUT YOUR MySQL username here - usually root
dbpass = "123Suezx." #PUT YOUR PASSWORD HERE
dbhost = "localhost"
dbport = "3306"
dbname = "TreeTalk"


# def getCursor():
#     if 'db' not in g:
#         g.db = mysql.connector.connect(
#             user=dbuser, password=dbpass, host=dbhost, database=dbname, auth_plugin='mysql_native_password'
#         )
#     return g.db.cursor(dictionary=True), g.db

# def close_connection(exception):
#     db = g.pop('db', None)
#     if db is not None:
#         db.close()
