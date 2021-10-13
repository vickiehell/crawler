
import pymysql
from pymysql.converters import escape_string
s=['a','b','c']
s=escape_string(s)
print(s)