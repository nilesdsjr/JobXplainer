import jaydebeapi
import os
from singleton import Singleton
from settings import Settings, Configuration


class HiveClient(object, metaclass=Singleton):
    

    def __init__(self):


        settings = Settings()
        _config = Configuration()
        config = _config.load_config(path_config=settings.CONFIG_PATH)
        _path_dependencies = config['profile']['hive']['jdbc']['dependencies']
        _database = config['profile']['hive']['jdbc']['database']
        _driver = config['profile']['hive']['jdbc']['driver']
        _server = config['profile']['hive']['jdbc']['server']
        _principal = config['profile']['hive']['jdbc']['principal']
        _port = config['profile']['hive']['jdbc']['port']
        _url = ('jdbc:hive2://{}:{}/{};principal={};'.format(_server, str(_port), _database, _principal))
        path_dependencies = os.path.join(settings.CONFIG_PATH, 'dependencies/hive-jdbc-3.1.2-standalone.jar')

        if _path_dependencies: 

            try:
            
                _conn = jaydebeapi.connect(jclassname='org.apache.hive.jdbc.HiveDriver', url=_url, jars=_path_dependencies)

            except Exception as e:
               
                raise e

        elif os.path.isfile(path_dependencies):
            
            try:

                _conn = jaydebeapi.connect(jclassname='org.apache.hive.jdbc.HiveDriver', url=_url, jars=path_dependencies)
            
            except Exception as e:
                    
                raise e

        else:
            
            try:
                
                _conn = jaydebeapi.connect(jclassname='org.apache.hive.jdbc.HiveDriver', url=_url)

            except Exception as e:
                    
                raise e

        self.cursor = _conn.cursor()


    def execute(self, sql):


        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        return results


    def close(self):


        return self.cursor.close()

