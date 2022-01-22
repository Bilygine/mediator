import rethinkdb as r
import config
import logging


def get_source(source_id):
	rdb = r.RethinkDB()
	conn = rdb.connect('db', config.DB_PORT).repl()
	ret = rdb.db(config.DB).table(config.SOURCE_TABLE).get(source_id).run()
	conn.close()
	return ret

def create_source(source):
	rdb = r.RethinkDB()
	conn = rdb.connect('db', config.DB_PORT).repl()
	try:
		rdb.db(config.DB).table_create(config.SOURCE_TABLE).run()
		rdb.db(config.DB).table(config.SOURCE_TABLE).index_create('url').run()
	except r.errors.ReqlOpFailedError:
		logging.info("Table source already created")
	ret = rdb.table(config.SOURCE_TABLE).insert(source.to_dict()).run()
	conn.close()
	return ret

def update_source(source):
	rdb = r.RethinkDB()
	conn = rdb.connect('db', config.DB_PORT).repl()
	try:
		ret = rdb.db(config.DB).table(config.SOURCE_TABLE).get(source.id).update(source.to_dict()).run()
		conn.close()
		return ret
	except:
		logging.info("error while updating source " + source.id)
		conn.close()
		raise

def delete_source(source):
	rdb = r.RethinkDB()
	conn = rdb.connect('db', config.DB_PORT).repl()
	try:
		ret = rdb.db(config.DB).table(config.SOURCE_TABLE).get(source.id).delete().run()
		conn.close()
		return ret
	except:
		logging.info("error while deleting source " + source.id)
		conn.close()
		raise
