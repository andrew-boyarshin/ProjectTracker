% include('header.tpl')

<!--suppress XmlUnboundNsPrefix -->
<h1> Проект: {{pr.name}} </h1>

% if len (users):

<form class="pure-form" action = "/sadm/edit_apply" method = "POST">

% x = 0
% for i in users:
%   x = x + 1
    <input type="hidden" name="uid{{x}}" value="{{i[0].id}}">
    <input type="hidden" name="cid{{x}}" value="{{i[1].id}}">
    <p> <input class="pure-form" type = "checkbox"
% if ('a' in i[1].priv):
checked="" 
% end
 name = "isadm{{x}}"> {{i[0].name}} ({{i[1].name}})</p>
% end
<input type="hidden" value ="{{x}}" name = "users_count">
<input class="pure-button" type="submit" value = "Применить">
</form>

% end

% if len (users) == 0:
    %if len (req):
        <div>
        <h4> Новые заявки: </h4>
            <table class="pure-table pure-table-bordered">
                <thead>
                    <td> Имя </td>
                    <td>  Комментарий </td>
                    <td> Принять </td>
                </thead>
        % for i in req:
                    <tr>
                        <td>
                            {{i[1].name}}
                        </td>
                        <td>
                        % if (i[0].comment != "(no comment)"):
                            {{i[0].comment}}
                        % else:
                            Нет комментария
                        % end
                        </td>
                        <td>
                            <form action="/sadm/{{pr.id}}/new_user" method="POST">
                                <input class="pure-button" type="submit" name = "yes" value="Принять">
                                <input type="hidden" value ="{{i[1].id}}" name = "user_id">
                                <input type="hidden" value ="{{i[0].id}}" name = "req_id">
                            </form>
                        </td>
                    </tr>
            %end
        % end

        </table>
        </div>
    % end
% end

% include('footer.tpl', ver=ver, date=date) 