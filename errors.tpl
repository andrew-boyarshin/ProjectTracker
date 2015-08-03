% from bottle import *
% include('header.tpl')
<h1>Доброе утро!</h1>
<p>К сожалению, страница <tt>{{repr(request.url)}}</tt>
являлась причиной следующей ошибки:</p>
<pre>{{e.status}}</pre>
<pre>{{e.body}}</pre>
% if DEBUG and e.traceback:
<h2>Служебная информация для администратора (нажмите сюда для отображения)</h2>
<pre id="habracut" style="display: block;">
% if e.exception:
<h2>Ошибка:</h2>
{{repr(e.exception)}}
% end
<br />
<br />
{{e.traceback}}
</pre>
<script type="text/javascript" src="/static/andrew/jquery-2.1.3.min.js"></script>
<script type="text/javascript">
  $(document).ready (function() {
    var c = document.getElementById('habracut');
    c.previousElementSibling.onclick = function(event) {
      if (c.style.display === 'none') {
        c.style.display = '';
      } else {
        c.style.display = 'none';
      }
    };
  })
</script>
% end
% include('footer.tpl', ver=ver, date=date)