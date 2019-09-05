from app.fadmin import bp
from flask import url_for
from flask_user import current_user

from flask_admin.menu import MenuLink
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from app import db
from app.models import User, Role
from flask import current_app


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return (not current_user.is_anonymous) and current_user.has_role('admin')


app_name = current_app.config['USER_APP_NAME']

admin = Admin(name=app_name+' Admin', template_mode='bootstrap3',
              index_view=MyAdminIndexView())


class MyModelView(ModelView):
    def is_accessible(self):
        return (not current_user.is_anonymous) and current_user.has_role('admin')
    page_size = 25
    can_view_details = True
    edit_modal = True
    column_hide_backrefs = False
    can_export = True


class MyUserModelView(MyModelView):
    column_exclude_list = ['password_hash', ]
    column_searchable_list = ['username', 'email']
    column_list = ('username', 'email', 'date_created', 'date_modified', 'roles')
    form_excluded_columns = ['date_created', 'date_modified', 'password']


class MyRoleModelView(MyModelView):
    column_list = ('name', 'date_created', 'date_modified')
    form_excluded_columns = ['date_created', 'date_modified', ]


admin.add_view(MyUserModelView(User, db.session))
admin.add_view(MyRoleModelView(Role, db.session))


@bp.before_app_first_request
def assign_links_to_admin():
    admin.add_link(MenuLink(name='Public Website', category='', url=url_for('main.index')))
    admin.add_link(MenuLink(name='Logout', category='', url=url_for('user.logout')))
