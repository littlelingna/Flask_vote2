from . import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime



class Action(db.Model):
    __tablename__ = 'coinaction'
    ActionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FromUser = db.Column(db.String)
    ToUser = db.Column(db.String)
    AeroCoin_type = db.Column(db.String)
    AeroCoin_Num = db.Column(db.Integer)
    Reason = db.Column(db.String)
    ReasonNote = db.Column(db.String)
    ActionTime = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)
    remark = db.Column(db.String)
    ActionPreiod = db.Column(db.String)
    # users = db.relationship('User', backref='role')

    # @staticmethod
    # def seed():
    #     db.session.add_all(map(lambda r: Action(name=r), ['Guests', 'Administrators']))
    #     db.session.commit()

class Turnover(db.Model):
    __tablename__ = 'actionturnover'
    TurnoverId = db.Column(db.Integer,primary_key=True,autoincrement=True)
    FromUser = db.Column(db.String)
    directLeader = db.Column(db.String)
    AeroCoin_Num = db.Column(db.Integer)
    TurnoverTime = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)
    TurnoverPreiod = db.Column(db.String)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    # email = db.Column(db.String)
    password = db.Column(db.String)
    userole = db.Column(db.String)
    directLeader = db.Column(db.String)
    AeroCoin_type = db.Column(db.String)
    AeroCoin_Num = db.Column(db.Integer)
    employee_date = db.Column(db.Date)

#以为报错 NotImplementedError('No `id` attribute - override `get_id`')，所以override get_id方法
    def get_id(self):
        return self.userid

    def get_name(self):
        return self.username

    def get_leader(self):
        return self.directLeader


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

# class Post(db.Model):
#     __tablename__ = 'posts'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String)
#     body = db.Column(db.String)
#     body_html = db.Column(db.String)
#     created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#
#     comments = db.relationship('Comment', backref='post')
#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#
#     @staticmethod
#     def on_body_changed(target, value, oldvalue, initiator):
#         if value is None or (value is ''):
#             target.body_html = ''
#         else:
#             target.body_html = markdown(value)
#
#
# db.event.listen(Post.body, 'set', Post.on_body_changed)


class Assign(db.Model):
    __tablename__ = 'coinassign'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    AeroCoin_lefted = db.Column(db.Integer)
    AeroCoin_givetoLeader = db.Column(db.Integer)
    AeroCoin_fromuser = db.Column(db.Integer)
    AeroCoin_received = db.Column(db.Integer)
    AeroCoin_type = db.Column(db.String)
    # created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    # author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Ranking(db.Model):
    __tablename__ = 'rankinghistory'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    AeroCoin_lefted = db.Column(db.Integer)
    AeroCoin_givetoLeader = db.Column(db.Integer)
    AeroCoin_received = db.Column(db.Integer)
    ActionPreiod = db.Column(db.String)

class Department(db.Model):
    __tablename__ = 'department'
    DeptId = db.Column(db.Integer,primary_key=True)
    Deptname = db.Column(db.String)
    DeptLeader = db.Column(db.String)
    ParentDeptId = db.Column(db.Integer)
    Note = db.Column(db.String)

class Role(db.Model):
    __tablename__ = 'role'
    RoleId = db.Column(db.Integer,primary_key=True)
    Rolename = db.Column(db.String)
    AeroCoin_type = db.Column(db.String)
    AeroCoin_num = db.Column(db.Integer)

class Reason(db.Model):
    __tablename__ = 'actionreason'
    ReasonId = db.Column(db.Integer,primary_key=True)
    ReasonText = db.Column(db.String)
