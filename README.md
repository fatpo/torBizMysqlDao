# torBizMysqlDao
Business DAO for tornado + mysql, great productivity gains .
Mainly used in writing business logic code, CRUD is indeed a large number of duplicate code, it is not pythonic . 
So with the configuration of the program to write a specific business DAO, is pythonic.    

# Simulate the scene
Suppose there is a module now called: Student, you need to add or delete "Student".    
Database Table:
```
CREATE TABLE `student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) not NULL  DEFAULT '' comment 'student's name',
  `age` int(11) not NULL  DEFAULT 0 comment 'student's age',
  `del_flag` int(11) NOT NULL DEFAULT 0 comment 'soft delete flag，0-normal，1-deleted',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP comment 'create time',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment 'last update time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

```
We define a student Info:    
(or you can remove the info layer, direct control of the dict from db returns, if u want ...):
```
class StudentInfo(BaseInfo):
    def __init__(self, _item):
        self.id = 0
        self.name = ''
        self.age = 0
        self.del_flag = 0
        self.create_time = ''
        self.update_time = ''

        if isinstance(_item, dict):
            for key, value in _item.iteritems():
                self.__dict__[key] = value
```
then config a StudentDao：
```
class StudentDao(BaseDao):
    DataInfo = StudentInfo
    table_name = 'student'  # table name
    escape_list = ['name']  # the list need to be escaped 
    quot_list = ['create_time', 'update_time']  # the list requires quoted
    not_append_list = ['del_flag']  # int list like: img_id
    append_list = ['age']  # int list, but sometimes need to += n, like: add_cnt = add_cnt+10, view_cnt=view_cnt+1
```

# Test case-1：
get the student which id=1 and name='tom'   
```
pool = db.app_pool
with (yield pool.Connection()) as conn:
    yield conn.commit()
    
    context = None  # the context for app request...
    stu_id = 1   
    stu_name = 'tom'
    
    # get the student which id=1 and name ='tom'
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
```

# Test case-2：
update the sutdent age+=1 who's name='tom'   
```
pool = db.app_pool
with (yield pool.Connection()) as conn:
    yield conn.commit()
    
    context = None # the context for app request...
    stu_name = 'tom'  

    # update age += 1
    dic = {
        'name': stu_name,
        'age': (1, True)
    }
    yield StudentDao.update(context, conn, dic)
    yield conn.commit()
```
