% show_help = 3
% include('header.tpl')

<h1>Приёмка проекта</h1>

<p> Просмотрите пункты ТЗ и отметьте галочками те, которые вы считаете выполнеными.</p>

<p> Отмечено всеми участниками: <b> <span id="ac0">{{all_count[0]}}</span> из 
<span id="ac1">{{all_count[1]}}</span> </b></p>

<ul>
% for i in vector:
    <li>
        <h3>{{i[0].name}}</h3>
        <p> Отмечено всеми участниками (подпунктов): <b> <span id = "h1_{{i[0].id}}_0"> {{i[2][0]}}</span> из <span id = "h1_{{i[0].id}}_1">{{i[2][1]}}</span> </b> </p>

        <ul>
% for h in i[1]:
% j = h[0]
            <li>
                <form>
                    <h4>{{j.name}}
                    % if not readonly:
                    <input type = "checkbox" id="{{j.id}}"
                    onchange="javascript:change_app_status({{j.id}}, {{i[0].id}}, {{sow_id}}, {{pid}});"
% if h[2]:
checked="" 
% end
                    >
                    % end
                    (<span id = "h2_{{j.id}}_0"> {{h[1][0]}}</span> из <span id = "h2_{{j.id}}_1">{{h[1][1]}}</span>)
                    </h4>
                </form>
            </li>
% end
        </ul>
    </li>
% end
</ul>

<span id="ac0_2">{{all_count[0]}}</span>/<span id="ac1">{{all_count[1]}}</span>


<script type="text/javascript" src="/static/andrew/jquery-2.1.3.min.js"></script>
<script type="text/javascript" src="/static/first/stage3.js"></script>

% include('footer.tpl', ver=ver, date=date)