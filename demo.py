from pycqu import model
from pycqu import const
from pycqu import api
sess = api.Session()
print(sess.schedule())
print(sess._sess.cookies)