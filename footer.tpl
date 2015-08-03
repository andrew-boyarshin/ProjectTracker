% if 'pr_id' in dir():
</div>
<div class="pure-u-1-4">
% include('chat/chat.tpl', pr_id=pr_id, cur_author=cur_author)
</div>
</div>
% end
<div class="footer-margin"></div>
<footer>
<div class="pure-menu pure-menu-open pure-menu-horizontal">
    <a class="pure-menu-heading" style="line-height: 1.7em;">WS10: Project Tracker</a>
    <ul class="pure-menu-heading" style="float: right; vertical-align: middle; line-height: 1.7em;">
	    <li>Версия {{ver}}</li>
	    <li>Время сервера: {{date}}</li>
    </ul>
</footer>
</body>
</html>