import jaydebeapi
from singleton import Singleton


@Singleton
class HiveClient(object):
    def __init__(self, config):

        self.database = config['profile']['hive']['jdbc']['database']
        self.driver = config['profile']['hive']['jdbc']['driver']
        self.server = config['profile']['hive']['jdbc']['server']
        self.principal = config['profile']['hive']['jdbc']['principal']
        self.port = config['profile']['hive']['jdbc']['port']

        # JDBC connection string
        self.url = ("jdbc:hive2://" + self.server + ":" + str(self.port) +
                    "/" + self.database + ";principal=" + self.principal + ";")

    #Connect to HiveServer2
    def get_conn(self):

        self.conn = jaydebeapi.connect("org.apache.hive.jdbc.HiveDriver",
                                       self.url)
        self.cursor = self.conn.cursor()

        return self.cursor

    def close(self):
        self.conn.close()
