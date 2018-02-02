# coding=utf-8
import logging

import tornado.gen
from tornado.ioloop import IOLoop

import db
from BaseDao import BaseDao
from BaseInfo import BaseInfo


class StudentInfo(BaseInfo):
    def __init__(self, _item):
        self.id = 0
        self.name = ''
        self.del_flag = 0
        self.create_time = ''
        self.update_time = ''

        if isinstance(_item, dict):
            for key, value in _item.iteritems():
                self.__dict__[key] = value


class StudentDao(BaseDao):
    DataInfo = StudentInfo
    table_name = 'student'  # 数据库表名
    escape_list = ['name']  # 需要转义的list
    quot_list = ['create_time', 'update_time']  # 需要带引号的list
    not_append_list = ['del_flag']  # int list，但是不可能有append操作的list，如 img_id
    append_list = []  # int list, 但是可能有append操作的list，如add_cnt, view_cnt


@tornado.gen.coroutine
def main():
    pool = db.app_pool
    try:
        with (yield pool.Connection()) as conn:
            yield conn.commit()

            # the context for app request...
            context = None

            stu_id = 1
            stu_name = "tom"

            # get the student which id=1, user_id=1001
            user = yield StudentDao.get_by_cols(context, conn, where_lst=[
                {
                    'key': stu_id,
                    'where_col': 'id',
                    'col_str': False
                },
                {
                    'key': stu_name,
                    'where_col': 'name',
                    'col_str': True
                }
            ], is_fetchone=True, with_del=True)
            logging.info("get_by_cols:")
            logging.info(user)

            # update age += 1
            dic = {
                'name': stu_name,
                'age': (1, True)
            }
            yield StudentDao.update(context, conn, dic)
            yield conn.commit()
    except Exception, ex:
        logging.error(ex, exc_info=1)


if __name__ == '__main__':
    ioloop = IOLoop.instance()
    ioloop.run_sync(main)
