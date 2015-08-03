% include('header.tpl')

<div>
% if isadm == 1:
<center>
     <div>
        <div class="pure-group">
        % for i in range (10):
        <br>
        % end
            <input onclick="javascript:document.location = '{{redirect_href}}';" type="submit" class="pure-button button-success" value="Войти как пользователь">
            <input onclick="javascript:document.location = '/admin/{{pr.id}}';" class="pure-button button-error"  type="button" value="Панель администратора">
            
        </div>
    </div>
</center>
% end
</div>

% include('footer.tpl', ver=ver, date=date)