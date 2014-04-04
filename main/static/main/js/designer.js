/*
 *"""    !!!!!!!!!!!!!!!"""
 *"""    there are todos"""
 *"""    !!!!!!!!!!!!!!!"""
 */
(function() {
  $.tshirt_data = {
    colors : {},
    num_colors: 0,
  }

  var $tshirtToggle = $('#tshirt-toggle');
  var $currentFabric = new fabric.Canvas('c'), $hiddenFabric = new fabric.Canvas('c2');
  var $currentCanvas = $('#c'), $hiddenCanvas = $('#c2');
  $hiddenCanvas.parent().hide();

  function rgbToHex(r, g, b) {
      return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
  }

  function updateBasePrice() {
    /*
     *get the new base price from the server using $.tshirt_data and
     *update the displayed base price
     */
    var base_tshirt = $('#tshirt-list>.active');
    var base_tshirt_rgb = base_tshirt.find('.selected-color').css('color').slice(4,-1).split(',');

    $.tshirt_data.base_tshirt_id = base_tshirt.data('id');
    $.tshirt_data.base_tshirt_color = rgbToHex(+base_tshirt_rgb[0], +base_tshirt_rgb[1], +base_tshirt_rgb[2]).toLowerCase(); //+ converts str to int
    //the num_colors is already set, but only is the count of text colors for now

    //sets tshirt_data.num_orders
    var min_orders_input = $('.tshirt-form-fields #id_min_orders');
    $.tshirt_data.num_orders = min_orders_input.val();
    /*
     *sets num_orders and min_orders input to upper/lower limit if
     *num_orders if outside the limit
     */
    if ($.tshirt_data.num_orders < 5) {
      $.tshirt_data.num_orders = 5;
      min_orders_input.val(5);
    } else if ($.tshirt_data.num_orders > 4999) {
      $.tshirt_data.num_orders = 4999;
      min_orders_input.val(4999);
    }
    
    $.get('/api/base-price/', $.tshirt_data, function(data) {
      $('.base-price-display .base-price').text(data.base_price);
      updateProfit();
    });
  }

  var $profit = $('#profit');
  function updateProfit() {
    var selling_price = parseFloat($('#id_selling_price').val()); 
    var base_price = parseFloat($('.base-price-display .base-price').first().text());

    //sets selling_price to base_price + 2 if it's less
    if (selling_price < base_price || isNaN(selling_price)) {
      selling_price = base_price+2;
      $('#id_selling_price').val(selling_price);
    }

    var diff = selling_price - base_price;
    var profit;
    $profit.siblings('#profit-premsg').text('Estimated profit:');
    profit = +(diff*parseInt($('#id_min_orders').val())).toFixed(2);
    $profit.text('$'+profit);
  }

  function resetForm(form) {
    var form = typeof form !== 'undefined'? form: $('#user-text-enter');

    form.find('#user-text-input').val("");
    form.find('a[data-option="Helvetica"]').click();
    form.find('.selected-color').css('color', '#000');

    form.children('button#add').show();
    form.children('button.edit').addClass('hide');

    //resets the image form
    $('#add-image-form').children('button.edit').addClass('hide');
  }

  function getFormData(form) {
    var form = typeof form !== 'undefined'? form: $('#user-text-enter');

    return {
      text       : form.find('#user-text-input').val(),
      fontFamily : form.find('#selected-font').val(),
      fill       : form.find('.selected-color').css('color'),
    }
  }

  function toggleCanvas () {
    /*
     *changes canvas between display and edit mode
     *also toggles printable area
     */
    var cArray = [$currentFabric, $hiddenFabric];
    for (var i = 0; i<2; i++) {
      var c = cArray[i];
      if (c.selection) {
        //makes canvas uneditable
        c.selection=false;
        c
          .deactivateAllWithDispatch()
          .forEachObject(function(o) {
            o.selectable = false;
          })
          .renderAll();
      } else {
        //makes c editable
        c.selection=true;
        c.forEachObject(function(o) {
          o.selectable = true;
        });
      }
    }
    $currentCanvas.add($hiddenCanvas).parent().toggleClass('uneditable');
  }

  function initForm () {
    $('#campaign-tip').tooltip({
      placement: 'right',
      title: 'Launching your tshirt as a campaign allows you to enter how many shirts you estimate you will sell.  Depending on how many shirts you sell, the base price per shirt decreases, allowing you to make more profit!',
      trigger: 'click',
    });

    var input_tags = $('#id_tags');
    input_tags.tagsinput({
      maxTags: 10,
    });

    var source = $('#tshirt-tag-template').html();
    var tshirt_tag_template = Handlebars.compile(source);

    input_tags.tagsinput('input').typeahead({
      prefetch: '/api/popular-tags/',
      remote: '/api/popular-tags/?q=%QUERY',
      valueKey: 'name',
      template: tshirt_tag_template,
      limit: 10,
    }).bind('typeahead:selected',function (obj, datum) {  
      input_tags.tagsinput('add', datum.name);
      input_tags.tagsinput('input').typeahead('setQuery', '');
    });
  }

  function setFormForSelected() {
    //sets up the edit form for when canvas object is selected
    resetForm();

    var canvas = $currentFabric;

    var object = canvas.getActiveObject();
    object.bringToFront();
    if (object.type === 'text') {
      var form = $('#user-text-enter');

      form.children('button#add').hide();
      form.children('button.edit').removeClass('hide');

      form.find('#user-text-input').val(object.getText());
      form.find('a[data-option="'+object.getFontFamily()+'"]').click();
      form.find('.selected-color').css('color', object.getFill());
      $('.nav-tabs a[href="#addtext"]').tab('show');
    } else {
      var form = $('#add-image-form');
      form.children('button.edit').removeClass('hide');
      $('.nav-tabs a[href="#uploadimage"]').tab('show');
    }
  }

  function setFormForSelectionCleared() {
      resetForm();
  }

  function removeObject() {
    //deletes the active canvas object
    var canvas = $currentFabric;
    var object = canvas.getActiveObject();
    
    //decrements the object color in $.tshirt_data.colors
    if (object.type === 'text') {
      $.tshirt_data.colors[object.fill] -= 1;

      //deletes the color if no other objects have that color
      if ($.tshirt_data.colors[object.fill] === 0) {
        delete $.tshirt_data.colors[object.fill];
        $.tshirt_data.num_colors -= 1;
      }
    } else {
      //todo: calculate the image's colors and remove them
    }
    updateBasePrice();

    object.remove();
    resetForm();
  }


  $currentFabric
    .on('object:selected', setFormForSelected)
    .on('selection:cleared', setFormForSelectionCleared);
  $hiddenFabric
    .on('object:selected', setFormForSelected)
    .on('selection:cleared', setFormForSelectionCleared);

  $('#save-changes').click(function() {
    //saves changes to selected text object
    var canvas = $currentFabric;
    var text = canvas.getActiveObject();
    var data = getFormData();

    //decrements the text color in $.tshirt_data.colors
    $.tshirt_data.colors[text.fill] -= 1;

    //deletes the color if no other objects have that color
    if ($.tshirt_data.colors[text.fill] === 0) {
      delete $.tshirt_data.colors[text.fill];
      $.tshirt_data.num_colors -= 1;
    }

    text.set({
      text       : data.text,
      fontFamily : data.fontFamily,
      fill       : data.fill,
    });

    canvas.deactivateAllWithDispatch().renderAll();

    //updates $.tshirt_data.colors
    if (data.fill in $.tshirt_data.colors) {
      $.tshirt_data.colors[data.fill] += 1;
    } else {
      $.tshirt_data.colors[data.fill] = 1;
      $.tshirt_data.num_colors += 1;
    }

    updateBasePrice();

  });

  $('#user-text-enter')
    .submit(function(event) {
      //prevents the form from submitting
      event.preventDefault();
    })
    .children('button#add')
      .click(function(event) {
        //adds a new text object
        var canvas = $currentFabric;
        var form = $(this).parent();
        var data = getFormData(form);

        var text = new fabric.Text(data.text, {
          left: canvas.getWidth()/2,
          top: canvas.getHeight()/2,
          fontFamily: data.fontFamily,
          fill: data.fill,
        });
        canvas.add(text);

        //updates $.tshirt_data.colors
        if (data.fill in $.tshirt_data.colors) {
          $.tshirt_data.colors[data.fill] += 1;
        } else {
          $.tshirt_data.colors[data.fill] = 1;
          $.tshirt_data.num_colors += 1;
        }

        updateBasePrice();

        resetForm(form);
      });

  $('#colorpalette').colorPalette()
    .on('selectColor', function(e) {
      $('#colorpicker .selected-color').css('color', e.color);
    });

  $('#add-image-form').submit(function (event) {
    event.preventDefault();
  })
    .children('#add-image-input')
      .change(function() {
        var canvas = $currentFabric;
        var reader = new FileReader();
        var newImg = $('<img id="newimg"/>');

        reader.onload = function (e) {
          newImg.attr('src', e.target.result);
          var image = new fabric.Image(newImg[0], {
            left: canvas.getWidth()/2,
            top: canvas.getHeight()/2,
          });

          //this scales the image down to fit in the canvas
          //todo: handle if image is smaller than the canvas
          //easy to do but right now it's not even known if images
          //smaller than the canvas will be allowed that's why it's not done yet
          var widthScale = canvas.width/image.width;
          var heightScale = canvas.height/image.height;
          image.scale(widthScale<heightScale? widthScale: heightScale);

          canvas.add(image);
        }

        reader.readAsDataURL($(this)[0].files[0]);
        $(this).val('');
      });

  $('#c, #c2').parent().hover(
    function () {
      if (!$(this).hasClass('uneditable')) {
        $('#canvas-tag').removeClass('hide');
      }
    },
    function () {
      if (!$(this).hasClass('uneditable')) {
        $('#canvas-tag').addClass('hide');
      }
    }
  );


  //todo: add 2nd canvas
  $('#tshirt-form').submit(function (e) {
    e.preventDefault();
    if ($('#logged-out-nav').length) {
      $('#login-modal div.alert').removeClass('hide').closest('#login-modal').modal('show');
    } else {
      tshirtForm = $(this);
      if (!tshirtForm.hasClass('submitted')) {
        tshirtForm.addClass('submitted');
        //posts form
        var form = $('.tshirt-form-fields');

        if ($tshirtToggle.data('front')) {
          var frontFabric = $currentFabric;
          var backFabric = $hiddenFabric;
        } else {
          var frontFabric = $hiddenFabric;
          var backFabric = $currentFabric;
        }
        //sets #id_design input
        form.find('#id_design').val(frontFabric.toDataURL().slice(22)); //the slice gets rid of data:image/png;base64,
        form.find('#id_design_back').val(backFabric.toDataURL().slice(22)); //the slice gets rid of data:image/png;base64,
        //sets #id_base_tshirt_id and #id_base_tshirt_color inputs
        form.find('#id_base_tshirt_id').val($.tshirt_data.base_tshirt_id);
        form.find('#id_base_tshirt_color').val($.tshirt_data.base_tshirt_color);

        $.post(window.location, form.find('*').serialize(), function(data) {
          if (data.success) {
            window.location.href = data.tshirt_page_url;
          } else {
            $('.tshirt-form-fields')
              .first().html(data.form_part_1)
              .end()
              .last().html(data.form_part_2);
            initForm();
            tshirtForm.removeClass('submitted');
          }
        });
      }
    }
  });

  $.get('/api/base-tshirts/', function(tshirts) {
    var tshirt_list = $('#tshirt-list');
    var source = $('#base-tshirt-template').html();
    var base_tshirt_template = Handlebars.compile(source);

    //makes the first base tshirt be active
    tshirts[0].active = 'active';
    //this adds the list of base tshirts to tshirt-list
    tshirt_list.html(base_tshirt_template({'tshirts': tshirts}));

    $('#tshirt-list>li.base-tshirt')
      .each(function(index) {
        var options = {
          colors: [tshirts[index].colors],
        };
        var tshirt_li = $(this);
        tshirt_li.find('.colorpalette').colorPalette(options)
          .on('selectColor', function(e) {
            tshirt_li.find('.selected-color').css('color', e.color);
          });
        tshirt_li.find('.base-tshirt-popover')
          .popover({placement: 'bottom', content: tshirts[index].description, trigger: 'hover',});
      })
      .click(function() {
        $('#background-tshirt').css('background-color', $(this).find('.selected-color').css('color'));
        $(this).addClass('active').siblings('.active').removeClass('active');

        updateBasePrice();
      });

    //this first call is to get the initial base price
    updateBasePrice();
  });

  $('#next-button').click (function() {
    if (!$(this).hasClass('clicked')) {
      /*
       *this if statement and this code makes
       *sure double clicks don't run the code twice
       */
      $(this).addClass('clicked');
      $('#prev-button').removeClass('clicked');

      $('.fade-out').fadeOut(function() {
        $('.fade-in').removeClass('hide').fadeIn();
      });

      toggleCanvas();
      $tshirtToggle.children('span:first').text('See');
    }
  });

  $('#prev-button').click (function() {
    if (!$(this).hasClass('clicked')) {
      /*
       *this if statement and this code makes
       *sure double clicks don't run the code twice
       */
      $(this).addClass('clicked');
      $('#next-button').removeClass('clicked');

      $('.fade-in').fadeOut(function() {
        $('.fade-out').fadeIn();
      });

      toggleCanvas();
      $tshirtToggle.children('span:first').text('Edit');
    }
  });

  //this variable used in 2nd .on below
  var stoppedInput;
  var stoppedInput2;
  $('.tshirt-form-fields')
    //updates base price when user stops changing min_orders for 1 second
    .on('input', '#id_min_orders', function() {
      // is there already a timer? clear if if there is
      if (stoppedInput) clearTimeout(stoppedInput);
      // set a new timer to execute 1 second from last keypress
      stoppedInput = setTimeout(function(){
        updateBasePrice();
      }, 1000); // 1 second
    })
    .on('input', '#id_selling_price', function() {
      // is there already a timer? clear if if there is
      if (stoppedInput2) clearTimeout(stoppedInput2);
      // set a new timer to execute 1 second from last keypress
      stoppedInput2 = setTimeout(function(){
        updateProfit();
      }, 1000); // 1 second
    });

  //sets the first tshirt as the active one by default, there's probably a more efficient way to do this but whatever
  $('#tshirt-list>li:eq(0)').click();

  initForm();

  //closes the campaign tooltip if a click is outside the tooltip
  $('body').on('click', function (e) {
    var campaignTooltip = $('#campaign-tip');
    //if the campaign tooltip isn't click
    if (!campaignTooltip.is(e.target)) {
      //hides the campaign tooltip
      campaignTooltip.tooltip('hide');
    }
  });

  var $backgroundTshirt = $('#background-tshirt');
  $tshirtToggle.click(function() {
    //toggles between front and back tshirt editing
    if ($(this).data('front')) {
      $(this).data('front', false).children('span:eq(1)').text('front');
      //switches to back tshirt
      $backgroundTshirt.attr('src', $backgroundTshirt.attr('src').slice(0,-4)+'_back.png');
    } else {
      $(this).data('front', true).children('span:eq(1)').text('back');
      //switches to front tshirt
      $backgroundTshirt.attr('src', $backgroundTshirt.attr('src').slice(0,-9)+'.png');
    }
    //deactivates back canvas
    $currentFabric.deactivateAllWithDispatch().renderAll();

    //hides current canvas and shows hidden canvas and resets hidden canvas offset bc it is moved
    $currentCanvas.parent().hide();
    $hiddenCanvas.parent().show();
    $hiddenFabric.calcOffset();

    var tmp;
    //switches $currentCanvas and $hiddenCanvas
    tmp = $currentCanvas;
    $currentCanvas = $hiddenCanvas;
    $hiddenCanvas = tmp;
    //switches $currentFabric and $hiddenFabric
    tmp = $currentFabric;
    $currentFabric = $hiddenFabric;
    $hiddenFabric = tmp;
  });

  // Prevent the backspace key from navigating back.
  $(document)
    .unbind('keydown')
    .bind('keydown', function (event) {
      var doPrevent = false;
      if (event.keyCode === 8) {
          var d = event.srcElement || event.target;
          if ((d.tagName.toUpperCase() === 'INPUT' && (d.type.toUpperCase() === 'TEXT' || d.type.toUpperCase() === 'PASSWORD' || d.type.toUpperCase() === 'FILE' || d.type.toUpperCase() === 'NUMBER')) 
               || d.tagName.toUpperCase() === 'TEXTAREA') {
              doPrevent = d.readOnly || d.disabled;
          }
          else {
              doPrevent = true;
          }
      }

      if (doPrevent) {
          event.preventDefault();
          removeObject();
      }
    })
    .click(function(e) {
      var target = $(e.target);
      if (!target.is($currentCanvas.siblings(('.upper-canvas'))) && !target.closest('.fade-out .tab-content').length) {
        $currentFabric.deactivateAllWithDispatch().renderAll();
      }
    });
})()
