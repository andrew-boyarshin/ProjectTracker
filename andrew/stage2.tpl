% show_help = 2
% include('header.tpl', pr_id=pr_id, cur_author=cur_author)
<ul>
% for i in data.values():
    <li>
        <h1>{{i[0].name}}</h1>
        <p>{{i[0].html}}</p>
        <ul>
% for k in range(1, len(i)):
% j = i[k]
            <li id="parent-{{j.id}}">
                <h2 onclick="javascript:load_data({{pr_id}}, {{j.id}});">{{j.name}}</h2>
            </li>
% end
        </ul>
    </li>
% end
</ul>

<script type="text/javascript" src="/static/andrew/jquery-2.1.3.min.js"></script>
<script type="text/javascript" src="/static/andrew/stage2.js"></script>

% include('footer.tpl', ver=ver, date=date, pr_id=pr_id, cur_author=cur_author)