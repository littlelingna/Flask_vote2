# coding=utf-8


from flask import render_template, request, flash, redirect, url_for, current_app, abort
from . import admin
from .. import db
from ..models import Action, Assign, User, Ranking, Department, Turnover, Role, Reason
from flask_login import login_required, current_user


# from .forms import userGiveToActionForm, userGiveToLeaderForm, ChangePasswordForm, UserRankingqueryForm


@admin.route('/adminhome', methods=['GET', 'POST'])
@login_required
def adminhome():
    # 赠予操作记录总数
    AeroCoinActionNum = Action.query.count()
    # Aero币总数
    AeroCoinNum = db.session.query(db.func.sum(User.AeroCoin_Num)).scalar()
    # 回收记录总数
    AeroCoinTurnoverNum = Turnover.query.count()
    # 剩余Aero币数量
    AeroCoinLeftNum = db.session.query(db.func.sum(Assign.AeroCoin_lefted)).scalar()
    UserList = db.session.query(User.username, User.userole, User.AeroCoin_type,
                                User.AeroCoin_Num, User.employee_date, User.directLeader,
                                ).filter(User.username != 'admin').all()
    db.session.commit()
    return render_template("adminhome.html", AeroCoinActionNum=AeroCoinActionNum, AeroCoinNum=AeroCoinNum,
                           AeroCoinTurnoverNum=AeroCoinTurnoverNum, AeroCoinLeftNum=AeroCoinLeftNum, UserList=UserList,
                           title=u'管理员首页')

@admin.route('/adminhome/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    return render_template("adminhome.html",title=u'管理员首页')


@admin.route('/adminsetting', methods=['GET', 'POST'])
@login_required
def adminsetting():
    DepartmentList = db.session.query(Department.Deptname, Department.DeptLeader)
    RoleList = db.session.query(Role.Rolename, Role.AeroCoin_type, Role.AeroCoin_num)
    ReasonList = db.session.query(Reason.ReasonText)
    db.session.commit()
    return render_template("adminsetting.html", DepartmentList=DepartmentList, RoleList=RoleList, ReasonList=ReasonList,
                           title=u'系统设置')


@admin.route('/adminrecord', methods=['GET', 'POST'])
@login_required
def adminrecord():
    # 赠予操作记录总数
    AeroCoinActionNum = Action.query.count()
    # 赠予Aero币数量
    AeroCoinNum = db.session.query(db.func.sum(Assign.AeroCoin_received)).scalar()
    # 剩余Aero币数量
    AeroCoinLeftNum = db.session.query(db.func.sum(Assign.AeroCoin_lefted)).scalar()
    ActionList = db.session.query(Action.FromUser, Action.ToUser, Action.AeroCoin_type,
                                  Action.AeroCoin_Num, Action.Reason, Action.ActionTime,
                                  Action.ActionPreiod).all()
    db.session.commit()
    return render_template("adminrecord.html", AeroCoinActionNum=AeroCoinActionNum, AeroCoinNum=AeroCoinNum,
                           AeroCoinLeftNum=AeroCoinLeftNum, ActionList=ActionList, title=u'赠予操作记录')


@admin.route('/admincount', methods=['GET', 'POST'])
@login_required
def admincount():
    ActionPreiodList = Ranking.query.with_entities(Ranking.ActionPreiod).distinct().all()
    RankingHistory=db.session.query(Ranking.username,Ranking.AeroCoin_received,Ranking.ActionPreiod)
    return render_template("admincount.html", ActionPreiodList=ActionPreiodList,RankingHistory=RankingHistory, title=u'月度统计')


@admin.route('/admincount/search', methods=['GET', 'POST'])
@login_required
def search():
    # if request.method == 'GET':
    ActionPreiodList = Ranking.query.with_entities(Ranking.ActionPreiod).distinct().all()
    return render_template("admincount.html", ActionPreiodList=ActionPreiodList, title=u'月度统计')
