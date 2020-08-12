# -*- coding: utf-8 -*-

from flask import render_template, request, flash, redirect, url_for, current_app, abort, jsonify, json, Response
from . import main
from .. import db
from ..models import Action, Assign, User, Ranking, Department, Turnover, Reason
from flask_login import login_required, current_user

from .forms import userGiveToActionForm, ChangePasswordForm, UserRankingqueryForm


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@main.route('/')
def index():
    # posts=Post.query.all()

    # page_index = request.args.get('page', 1, type=int)

    # query = Post.query.order_by(Post.created.desc())

    # pagination = query.paginate(page_index, per_page=20, error_out=False)
    #
    # posts = pagination.items

    #    return render_template('index.html',
    #                          title=u'Aero币应用管理')
    return redirect(url_for('main.userhome'))


@main.route('/about')
def about():
    return render_template('about.html', title=u'关于')


@main.route('/userhome', methods=['GET', 'POST'])
@login_required
def userhome():
    if request.method == 'POST':
        # pass
        #####  从 usergivetoAction form 读取赠予操作。 但是还要get到 提交的记录显示到 列表里
        form1 = userGiveToActionForm()
        # form2 = userGiveToLeaderForm()

        if form1.submit1.data and form1.validate():

            print("------------give to user--", dict(form1.ToUser.choices).get(form1.ToUser.data))
            #### 执行投币后当前user需要从assign扣除AeroCoinLefted
            fromUserLefted = Assign.query.filter_by(username=current_user.username).first_or_404()

            print("--------------for now left", fromUserLefted.AeroCoin_lefted)
            print("-------------will give ", form1.AeroCoinNum._value(), " coins")
            if int(form1.AeroCoinNum._value()) <= int(fromUserLefted.AeroCoin_lefted):
                #######  从Form表单获取存入数据库的字段
                userGiveToAction = Action(FromUser=current_user.username,
                                          ToUser=dict(form1.ToUser.choices).get(form1.ToUser.data),
                                          AeroCoin_type=dict(form1.AeroCoinType.choices).get(form1.AeroCoinType.data),
                                          AeroCoin_Num=form1.AeroCoinNum._value(),
                                          Reason=dict(form1.Reasonlist.choices).get(form1.Reasonlist.data),
                                          ReasonNote=form1.ReasonText.data,
                                          ActionPreiod='current'
                                          )
                #### 因为提示 translate 问题，debug字段信息
                if current_user.username == dict(form1.ToUser.choices).get(form1.ToUser.data):
                    print("-----POST--- 自己给自己投币判断---")
                    flash("赠予者与赠予对象不能相同。")
                    return redirect(url_for('main.userhome'))

                # print("------------give to user--",userGiveToAction.ToUser)
                print("---POST----余额充足，执行session.add")
                db.session.add(userGiveToAction)
                # db.session.commit()
                # fromUserLefted.update({"AeroCoin_lefted": int(AeroCoin_lefted - AeroCoin_Num)})
                # ----update用来批量更新，因为assign表username是唯一的 ,故不需要
                Assign.query.filter_by(username=current_user.username) \
                    .update({"AeroCoin_lefted": int(fromUserLefted.AeroCoin_lefted) - int(form1.AeroCoinNum._value())})
                #######--- 需要给投币的ToUser添加AeroCoin_Received
                toUser = dict(form1.ToUser.choices).get(form1.ToUser.data)
                toUserReceieved = Assign.query.filter_by(username=toUser).first_or_404()
                Assign.query.filter_by(username=toUser). \
                    update(
                    {"AeroCoin_received": int(toUserReceieved.AeroCoin_received) + int(form1.AeroCoinNum._value())})
                db.session.commit()
            else:
                print("-----POST--- 余额不足---")
                flash("Aero币余额不足")
                db.session.rollback()
        # if form2.submit2.data and form2.validate():
        #
        #     #### 执行投币后当前user需要从assign扣除AeroCoinLefted,添加AeroCoinGivetoLeader
        #     fromUserAssign = Assign.query.filter_by(username=current_user.username).first_or_404()
        #     fromUser = User.query.filter_by(username=current_user.username).first_or_404()
        #     fromLeaderAssign = Assign.query.filter_by(username=fromUser.directLeader).first_or_404()
        #
        #     print("--------------for now left", fromUserAssign.AeroCoin_lefted)
        #     print("--------------for now give to leader", fromUserAssign.AeroCoin_givetoLeader)
        #     print("--------------leader", fromUser.directLeader)
        #     print("--------------Leader for now left", fromLeaderAssign.AeroCoin_lefted)
        #     print("-------------will give to leader", fromUserAssign.AeroCoin_lefted, " coins")
        #     if int(fromUserAssign.AeroCoin_lefted) > 0:
        #         userTurnover = Turnover(FromUser=current_user.username,
        #                                 directLeader=fromUser.directLeader,
        #                                 AeroCoin_Num=fromUserAssign.AeroCoin_lefted,
        #                                 TurnoverPreiod='current'
        #                                 )
        #         db.session.add(userTurnover)
        #         Assign.query.filter_by(username=fromUser.directLeader). \
        #             update({"AeroCoin_lefted": int(fromLeaderAssign.AeroCoin_lefted) +
        #                                        int(fromUserAssign.AeroCoin_lefted),
        #                     "AeroCoin_fromuser": int(
        #                         fromUserAssign.AeroCoin_lefted) + fromLeaderAssign.AeroCoin_fromuser})
        #         Assign.query.filter_by(username=current_user.username) \
        #             .update(
        #             {"AeroCoin_lefted": 0,
        #              "AeroCoin_givetoLeader": int(fromUserAssign.AeroCoin_lefted)})
        #         #######--- 需要给Leader添加AeroCoin_lefted
        #         db.session.commit()
        #     else:
        #         print("-----POST--- 余额不足---")
        #         flash("Aero币余额不足")
        #         db.session.rollback()

        # ToUser=dict(form.ToUser.choices).get(form.ToUser.data)
        # toUserReceived = Assign.query.filter_by(username=ToUser).first_or_404()
        # toUserReceived.update({models.Assign.AeroCoin_received:int(AeroCoin_received + AeroCoin_Num)})

        # db.session.add(userGiveToAction)
        # db.session.commit()

        ########### 提交记录后需要重新读取, 但使用redirect后就可以不用重复GET #####
        # userGiveToRecords=db.session.query(Action.FromUser,Action.ToUser,Action.AeroCoin_type,
        #                                    Action.AeroCoin_Num,Action.ActionTime,Action.Reason).filter_by(FromUser=current_user.username).all()
        #
        # AeroCoinReceived=Assign.query.with_entities(Assign.AeroCoin_received).filter_by(username=current_user.username).first()
        # AeroCoinLefted=Assign.query.with_entities(Assign.AeroCoin_lefted).filter_by(username=current_user.username).first()
        # db.session.commit()
        # ###---debug--
        # print("--POST----------userGiveToRecords----", userGiveToRecords)
        # print("--POST------AeroCoinReceived-----",AeroCoinReceived)
        # print("--POST----------AeroCoinLefted------",AeroCoinLefted)
        # return render_template('userhome.html', form=form, GivetoRecords=userGiveToRecords,AeroCoinLefted=AeroCoinLefted,
        #                        AeroCoinReceived=AeroCoinReceived,title=u'用户首页')
        return redirect(url_for('main.userhome'))

    if request.method == 'GET':
        # pass
        form1 = userGiveToActionForm()
        # form2 = userGiveToLeaderForm()
        print("--GET----current_user----", current_user.username)
        # userGiveToRecords=Action.query().filter_by(FromUser=current_user.username).all()
        ###----  使用session查询可以批量制定字段
        userGiveToRecords = db.session.query(Action.ActionId, Action.FromUser, Action.ToUser, Action.AeroCoin_type,
                                             Action.AeroCoin_Num, Action.ActionTime, Action.Reason,
                                             Action.ReasonNote).filter_by(FromUser=current_user.username,
                                                                          ActionPreiod='current').all()

        AeroCoinReceived = Assign.query.with_entities(Assign.AeroCoin_received).filter_by(
            username=current_user.username).first()
        AeroCoinLefted = Assign.query.with_entities(Assign.AeroCoin_lefted).filter_by(
            username=current_user.username).first()
        AeroCoinFromuser = Assign.query.with_entities(Assign.AeroCoin_fromuser).filter_by(
            username=current_user.username).first()
        ReasonList = db.session.query(Reason.ReasonText)
        Leader = Department.query.with_entities(Department.DeptLeader).all()
        # print("部门领导",Leader)
        sign = False
        for leader in Leader:
            if current_user.username == leader[0]:
                sign = True
        db.session.commit()
        ###---debug--
        print("---GET---------userGiveToRecords----", userGiveToRecords)
        print("---GET-----AeroCoinReceived-----", AeroCoinReceived)
        print("---GET---------AeroCoinLefted------", AeroCoinLefted)
        return render_template('userhome.html', form1=form1, GivetoRecords=userGiveToRecords,
                               AeroCoinLefted=AeroCoinLefted, AeroCoinFromuser=AeroCoinFromuser,
                               AeroCoinReceived=AeroCoinReceived, ReasonList=ReasonList, sign=sign, title=u'用户首页')


@main.route('/userhome/turnover', methods=['GET', 'POST'])
@login_required
def turnover():
    #### 执行投币后当前user需要从assign扣除AeroCoinLefted,添加AeroCoinGivetoLeader
    fromUserAssign = Assign.query.filter_by(username=current_user.username).first_or_404()
    fromUser = User.query.filter_by(username=current_user.username).first_or_404()
    toLeaderAssign = Assign.query.filter_by(username=fromUser.directLeader).first_or_404()
    userTurnover = Turnover(FromUser=current_user.username,
                            directLeader=fromUser.directLeader,
                            AeroCoin_Num=fromUserAssign.AeroCoin_lefted,
                            TurnoverPreiod='current'
                            )
    db.session.add(userTurnover)
    Assign.query.filter_by(username=fromUser.directLeader). \
        update({"AeroCoin_lefted": int(toLeaderAssign.AeroCoin_lefted) +
                                   int(fromUserAssign.AeroCoin_lefted),
                "AeroCoin_fromuser": int(
                    fromUserAssign.AeroCoin_lefted) + toLeaderAssign.AeroCoin_fromuser})
    Assign.query.filter_by(username=current_user.username) \
        .update(
        {"AeroCoin_lefted": 0,
         "AeroCoin_givetoLeader": int(fromUserAssign.AeroCoin_lefted)})
    db.session.commit()
    return redirect(url_for('main.userhome'))


@main.route('/userhome/delete/<actionid>', methods=['GET', 'POST'])
@login_required
def actiondelete(actionid):
    Action_delete = Action.query.filter_by(ActionId=actionid).first_or_404()
    FromUserAssign = Assign.query.filter_by(username=Action_delete.FromUser).first_or_404()
    ToUserAssign = Assign.query.filter_by(username=Action_delete.ToUser).first_or_404()
    Assign.query.filter_by(username=Action_delete.FromUser).update(
        {"AeroCoin_lefted": int(FromUserAssign.AeroCoin_lefted) + int(Action_delete.AeroCoin_Num)})
    Assign.query.filter_by(username=Action_delete.ToUser).update(
        {"AeroCoin_received": int(ToUserAssign.AeroCoin_received) - int(Action_delete.AeroCoin_Num)})
    db.session.delete(Action_delete)
    db.session.commit()
    return redirect(url_for('main.userhome'))


@main.route('/userhome/modify', methods=['GET', 'POST'])
@login_required
def modify():
    actionid = request.form.get("actionid")
    touser = request.form.get("touser")
    aerocoin_type = request.form.get("aerocoin_type")
    aerocoin_num = request.form.get("aerocoin_num")
    reason = request.form.get("reason")
    reasonnote = request.form.get("reasonnote")
    Action_Modify = Action.query.filter_by(ActionId=actionid).first_or_404()
    FromUserAssign_Modify = Assign.query.filter_by(username=Action_Modify.FromUser).first_or_404()
    ToUserAssign_Modify = Assign.query.filter_by(username=Action_Modify.ToUser).first_or_404()
    ToUserAssign_New = Assign.query.filter_by(username=touser).first_or_404()
    Assign.query.filter_by(username=Action_Modify.FromUser).update({
        "AeroCoin_lefted": int(FromUserAssign_Modify.AeroCoin_lefted) + int(Action_Modify.AeroCoin_Num) - int(
            aerocoin_num)})
    Assign.query.filter_by(username=Action_Modify.ToUser).update({
        "AeroCoin_received": int(ToUserAssign_Modify.AeroCoin_received) - int(Action_Modify.AeroCoin_Num)})
    Assign.query.filter_by(username=touser).update({
        "AeroCoin_received": int(ToUserAssign_New.AeroCoin_received) + int(aerocoin_num)})
    Action.query.filter_by(ActionId=actionid).update({"ToUser": touser, "AeroCoin_type": aerocoin_type,
                                                      "AeroCoin_Num": aerocoin_num, "Reason": reason,
                                                      "ReasonNote": reasonnote})
    db.session.commit()
    Action_Now = Action.query.filter_by(ActionId=actionid).first()
    actiontime = str(Action_Now.ActionTime)
    FromUserAssign_Now = Assign.query.filter_by(username=Action_Modify.FromUser).first()
    return jsonify(
        {'touser': touser, 'aerocoin_type': aerocoin_type, 'aerocoin_num': aerocoin_num, 'actiontime': actiontime,
         'reason': reason, 'reasonnote': reasonnote, 'aerocoin_lefted': FromUserAssign_Now.AeroCoin_lefted})


# @main.route("/userhome/<username>", methods=['GET', 'POST'])
# @login_required
# def userhome(username):
#     pass


@main.route('/usersetting', methods=['GET', 'POST'])
@login_required
def usersetting():
    # @login_required
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.password == form.old_password.data:
            current_user.password = form.newpassword.data
            db.session.add(current_user)
            flash('密码重置成功.')
            return redirect(url_for('main.userhome'))
        else:
            flash('Invalid password.')
    return render_template("usersetting.html", form=form, title=u'用户设置')

    # return render_template('usersetting.html', title=u'用户设置')


@main.route('/userranking', methods=['GET', 'POST'])
@login_required
def userranking():
    # if request.method == 'POST':
    form = UserRankingqueryForm()
    #######---- TODO 针对查询按钮返回rankinghistory表的数据库查询结果

    if form.validate_on_submit():
        period = dict(form.period.choices).get(form.period.data)
        print("------select period is ---", period)
        # rankingquery = db.session.query(Ranking.username,Ranking.AeroCoin_received,Ranking.ActionPreiod).filter_by(ActionPreiod=period).limit(5)
        # rankingquery = Ranking.query.filter_by(ActionPreiod=period).order_by(Ranking.AeroCoin_received.desc()).limit(5)
        rankingquery = db.session.query(Ranking.username, Ranking.AeroCoin_received, Ranking.ActionPreiod).filter_by(
            ActionPreiod=period).order_by(Ranking.AeroCoin_received.desc()).limit(5)
        print("------GET rankingquery---", rankingquery)
        # db.session.commit()
        ####-----debug for querying
        print("------get results as---")
        for r in rankingquery:
            print(r)

        return render_template('userranking.html', form=form, rankingquery=rankingquery, title=u'查询优秀员工排名')

    return render_template('userranking.html', form=form, title=u'查询优秀员工排名')


@main.route('/shoutdown')
def shutdown():
    if not current_app.testing:
        abort(404)

    shoutdown = request.environ.get('werkzeug.server.shutdown')
    if not shoutdown:
        abort(500)

    shoutdown()
    return u'正在关闭服务端进程...'
