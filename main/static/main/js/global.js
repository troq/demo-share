//sets ajax csrf for django
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function setupAjax(csrftoken) {
  $.ajaxSetup({
      crossDomain: false, // obviates need for sameOrigin test
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type)) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
}
setupAjax(getCookie('csrftoken'));

function setupAccountForm(formId) {
  $(formId).submit(function (event) {
    event.preventDefault();
  })
    .children('input[type="submit"]')
      .click(function() {
        var form = $(this).parent();
        $.post(form.attr('action'), form.serialize(), function(data) {
          if (data.success) {
            $('#logged-out-nav').replaceWith(data.logged_in_nav);
            $('#login-modal').modal('hide');
            //resets ajax w/ new cookie
            setupAjax(getCookie('csrftoken'));
          } else {
            form.children(formId+'-fields').html(data.form);
          }
        });
      });
}

setupAccountForm('#login-form');
setupAccountForm('#registration-form');
