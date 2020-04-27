import jaydebeapi

class HiveConnection:

    database='testtdb'
    driver='org.apache.hive.jdbc.HiveDriver'
    server='192.168.200.100'
    principal='hive/example.domain.com@DOMAIN.COM.'
    port=10000

    # JDBC connection string
    url=("jdbc:hive2://" + server + ":" + str(port)
    + "/"+ database +";principal=" + principal + ";")

    #Connect to HiveServer2 
    def hive2conn(self, url=url):

        conn=jaydebeapi.connect("org.apache.hive.jdbc.HiveDriver", url)
        cursor = conn.cursor()
        return cursor

    # Execute SQL query
    def run_query(self, sql, cursor):

        sql="select * from item limit 10"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results