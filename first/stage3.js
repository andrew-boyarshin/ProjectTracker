function change_app_status (app_id, h1_id, sow_id, pr_id){
    var ch = document.getElementById (app_id);
    link = '/projects/'+pr_id+'/ack/change?sow='+sow_id+'&h1='+h1_id+'&h2='+app_id+'&st='+ch.checked;
    $.getJSON (link, function(json){
        var cur = document.getElementById ('h2_'+app_id+'_0');
        cur.innerHTML = json.ac;
        var cur2 = document.getElementById ('h2_'+app_id+'_1');
        cur2.innerHTML = json.uc;
        if (json.inc) {
            var cur = document.getElementById ('h1_'+h1_id+'_0');
            var cur2 = parseInt(document.getElementById ('h1_'+h1_id+'_1').innerHTML);
            var val = parseInt(cur.innerHTML);
            if (json.st) val++; else val--;
            if (val===cur2) document.location = '/projects/'+pr_id+'/ack';
            cur.innerHTML = val;
            cur = document.getElementById ('ac0');
            val = parseInt(cur.innerHTML);
            if (json.st) val++; else val--;
            cur.innerHTML = val;
            cur = document.getElementById ('ac0_2');
            cur.innerHTML = val;
        }
    })
}