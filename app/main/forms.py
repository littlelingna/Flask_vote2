# coding=utf-8

from flask_wtf import FlaskForm,Form
from wtforms import StringField,IntegerField, SubmitField,DateField,SelectField,TextAreaField,PasswordField
from wtforms.validators import DataRequired,NumberRange,EqualTo


# class userGivenToRecords(Form):
#     title = StringField(label=u"赠予记录")

###### userGivetoLeader 是将剩余aero币提交给上级
class userGivetoLeader(Form):
    pass

class userGiveToActionForm(FlaskForm):
    # title = StringField(label=u"赠予操作")
    ToUser = SelectField(label=u"赠予对象",coerce=str,choices=[
        (u'焦函', u'焦函'),
        (u'王亚伟', u'王亚伟'),
        (u'山丹', u'山丹'),
        (u'武卫文', u'武卫文'),
        (u'徐明洲', u'徐明洲'),
	(u'王姝',  u'王姝'),
	(u'肖金萍', u'肖金萍'),
	(u'王鑫龙', u'王鑫龙'),
        (u'李纪念', u'李纪念'),
        (u'张煜刚', u'张煜刚'),
        (u'张梦巧', u'张梦巧'),
        (u'章俊伟', u'章俊伟'),
        (u'范宇', u'范宇'),
        (u'滕一', u'滕一'),
        (u'王诗情', u'王诗情'),
	(u'许芳迪', u'许芳迪')],validators=[DataRequired()] )
    AeroCoinType = SelectField(label=u"Aero币类型", choices=[(u'Aero币',u'Aero币')])
    AeroCoinNum = IntegerField(label=u"赠予数量",validators=[DataRequired(),NumberRange(min=1,max=500)])
    Reasonlist = SelectField(label=u"赠予理由种类" , choices= [
        (u'取得阶段性成果或完成标志性工作', u'取得阶段性成果或完成标志性工作'),
        (u'对个人或组织影响力有较大正向提升', u'对个人或组织影响力有较大正向提升'),
        (u'获得公司及以上级表彰奖励', u'获得公司及以上级表彰奖励'),
        (u'管理类创新产生实效', u'管理类创新产生实效'),
        (u'技术类创新产生实效', u'技术类创新产生实效'),
        (u'承受较大工作强度和压力', u'承受较大工作强度和压力'),
        (u'其他（需备注明确内容）', u'其他（需备注明确内容）')
    ] , validators=[DataRequired()] )
    ReasonText = TextAreaField("赠予理由详情，其他类型时必填")
    submit1 = SubmitField("提交操作")

# class userGiveToLeaderForm(FlaskForm):
#     # 回收Aero币
#     submit2 = SubmitField(label="回收Aero币")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'原始password', validators=[DataRequired()])
    newpassword = PasswordField(u'新的password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    #表单中完成密码与确认密码一致性的验证
    password2 = PasswordField(u'确认password', validators=[DataRequired()])
    submit = SubmitField('更新password')

class UserRankingqueryForm(FlaskForm):
    # title = StringField(label=u"赠予操作")
    period = SelectField(label=u"选择时间段",coerce=str,choices=[
        (u'2020年4月至5月', u'2020年4月至5月'),
	(u'2020年5月至6月', u'2020年5月至6月'),
        (u'2020年6月至7月', u'2020年6月至7月')],
    validators = [DataRequired()]  )
    submit = SubmitField("查询")

