% include('header.tpl')

<h1 align="center"> Проект "{{pr.name}}" завершён</h1>

<div class="pure-g">
	<div class="pure-u-1-2">
        <pre id="editor">{{pr.md}}</pre>
	</div>
	<div class="pure-u-1-24"></div>
	<div class="pure-u-11-24">
		<h3>Закрытые тикеты:</h3>

		% tick = pr.tickets.split('/') 
		<p><b>Критические:</b> {{tick[0]}} из {{tick[1]}} </p>
		<p><b>Всего:</b> {{tick[2]}} из {{tick[3]}} </p>
		<h3>Хронология:</h3>
		<p><b>Дата создания:</b> {{pr.create_time}}</p>
		<p><b>Дата закрытия:</b> {{pr.close_time}}</p>
	</div>
</div>

<script src="/static/ace/ace.js" type="text/javascript" charset="utf-8"></script>

<script>
function ready(fn) {
    if (document.readyState != 'loading'){
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}
function onloadinit() {
	var i = ace.edit('editor');

    i.setTheme('ace/theme/dreamweaver');
    i.getSession().setMode('ace/mode/markdown');
    i.setFontSize('16px');
    i.setReadOnly(true);
}
ready(onloadinit);
</script>

<style>
    #editor {
        height: {{pr.md.count('\n')+2}}em;
        max-height: 50%;
    }
</style>

% include('footer.tpl', ver=ver, date=date)