/**
 * Created by chirath on 13/6/17.
 */

function click_attendance(name) {
    var inp = document.getElementById(name);
    var div = document.getElementById(name+'_div');
    if (inp.checked) {
        inp.checked = false;
        inp.removeAttribute('checked');
        div.classList.add('btn-danger');
        div.classList.remove('btn-success');
    }
    else {
        inp.checked = true;
        inp.setAttribute('checked', '');
        div.classList.add('btn-success');
        div.classList.remove('btn-danger');
    }
}

// Reponsibility details scripts

 function showForm() {
        var form = document.getElementById('student-form');
        if (form.style.display === 'none') {
            form.style.display = 'block';
        }
        else {
            form.style.display = 'none';
        }
    }

    function myFunction() {
        // Declare variables
        var input, filter, items, i;
        input = document.getElementById('search');
        filter = input.value.toUpperCase();
        items = document.getElementsByClassName('dropdown-item');

        // Loop through all list items, and hide those who don't match the search query
        for (i = 0; i < items.length; i++) {
            if (items[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
                items[i].style.display = "";
            } else {
                items[i].style.display = "none";
            }
        }
    }

    function addText(id, name) {
        var inp1 = document.getElementById('search');
        var inp2 = document.getElementById('search-id');
        inp1.value = name;
        inp2.value = id;
    }