# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, Length


class LoginForm(FlaskForm):
    username = StringField(label=u'用户名', validators=[DataRequired()])
    password = PasswordField(label=u'密码', validators=[DataRequired()])
    submit = SubmitField(label=u'登录')

# class ChangePasswordForm(Form):
#     old_password = PasswordField(u'原始password', validators=[Required()])
#     password = PasswordField(u'新的password', validators=[
#         Required(), EqualTo('password2', message='Passwords must match')])
#     #表单中完成密码与确认密码一致性的验证
#     password2 = PasswordField(u'确认password', validators=[Required()])
#     submit = SubmitField('更新成功')
