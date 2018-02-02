# coding=utf-8
import logging

import tornado.gen
from tornado.ioloop import IOLoop

import db
from BaseDao import BaseDao
from BaseInfo import BaseInfo


class GongxiuInfo(BaseInfo):
    def __init__(self, _item):
        self.id = 0
        self.name = ''
        self.creator_id = 0
        self.start_time = ''
        self.end_time = ''
        self.type = 0
        self.detail = ''
        self.img_id = 0  # 图片id
        self.join_cnt = 0
        self.status = 0  # 审核 0 - 未审核， 1 - 审核通过
        self.del_flag = 0
        self.create_time = ''
        self.update_time = ''

        if isinstance(_item, dict):
            for key, value in _item.items():
                self.__dict__[key] = value


class GongxiuDao(BaseDao):
    DataInfo = GongxiuInfo
    table_name = 'gongxiu'  # 数据库表名
    escape_list = ['name', 'detail']  # 需要转义的list
    quot_list = ['start_time', 'end_time', 'img_key', 'create_time', 'update_time']  # 需要带引号的list
    not_append_list = ['creator_id', 'type', 'status', 'img_id',
                       'del_flag']  # int list，但是不可能有append操作的list，如 img_id
    append_list = ['join_cnt']  # int list, 但是可能有append操作的list，如add_cnt, view_cnt


@tornado.gen.coroutine
def main():
    pool = db.app_pool
    try:
        with (yield pool.Connection()) as conn:
            yield conn.commit()

            # the context for app request...
            context = None

            gongxiu_id = 1
            user_id = 1001

            # get the gongxiu which id=1, user_id=1001
            user = yield GongxiuDao.get_by_cols(context, conn, where_lst=[
                {
                    'key': gongxiu_id,
                    'where_col': 'gongxiu_id',
                    'col_str': False
                },
                {
                    'key': user_id,
                    'where_col': 'user_id',
                    'col_str': False
                }
            ], is_fetchone=True, with_del=True)
            logging.info("get_by_cols:")
            logging.info(user)

            # update join_cnt += 1
            dic = {
                'id': gongxiu_id,
                'join_cnt': (1, True)
            }
            yield GongxiuDao.update(context, conn, dic)
            yield conn.commit()
    except Exception, ex:
        logging.error(ex, exc_info=1)


if __name__ == '__main__':
    ioloop = IOLoop.instance()
    ioloop.run_sync(main)
