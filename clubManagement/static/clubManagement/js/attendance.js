/**
 * Created by chirath on 13/6/17.
 */

function click_attendance(name) {
    var inp = document.getElementById(name);
    var div = document.getElementById(name+'_div');
    if (inp.checked) {
        inp.setAttribute("checked", ""); // For IE
        inp.removeAttribute("checked"); // For other browsers
        inp.checked = false;
        div.classList.add('btn-danger');
        div.classList.remove('btn-success');
    }
    else {
        inp.checked = true;
        inp.setAttribute('checked', 'checked');
        div.classList.add('btn-success');
        div.classList.remove('btn-danger');
    }
}