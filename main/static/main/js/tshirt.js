(function() {
  var $frontTshirtImg = $('#tshirt-img');
  var $backTshirtImg = $('#tshirt-img-back');
  var $checkoutTshirtImg = $('#checkout-tshirt-img');
  var $form = $('form#payment-form');
  var $checkoutModal = $('#checkout-modal');

  $('#checkout-btn').click(function() {
    $checkoutModal.modal('hide');
    $.post("", $form.serialize(), function(data) {
      if (data.success) {
        var num_payments_span = $('#num-payments');
        var min_orders = parseInt($('#min-orders').text());
        var new_num_payments = parseInt(num_payments_span.text())+1;
        var new_width;

        if (new_num_payments > min_orders) {
          new_width = 100;
        } else {
          new_width = 100*new_num_payments/min_orders;
        }

        num_payments_span.text(new_num_payments);
        $('#campaign-progress-bar').css('width', new_width+"%");
        $('#form-success-modal').modal('show');
      } else {
        $('#form-fail-modal').modal('show');
      }
    });
  });

  var token = function(res, args){
    $form
      .find('#id_stripe_token').val(res.id)
      .siblings('#id_email').val(res.email)
      .siblings('#id_shipping_name').val(args.shipping_name)
      .siblings('#id_shipping_country').val(args.shipping_address_country)
      .siblings('#id_shipping_city').val(args.shipping_address_city)
      .siblings('#id_shipping_street').val(args.shipping_address_line1)
      .siblings('#id_shipping_state').val(args.shipping_address_state)
      .siblings('#id_shipping_zip').val(args.shipping_address_zip);
    $checkoutModal.modal('show');
  };

  var handler = StripeCheckout.configure({
      key             : tshirt.pub_key,
      amount          : tshirt.price*100,
      currency        : 'usd',
      name            : tshirt.username,
      description     : tshirt.title,
      shippingAddress : true,
      panelLabel      : 'Checkout',
      token           : token,
  });

  $('#customButton').click(function(event){
    event.preventDefault();
    handler.open();
  });

  $('.selectpicker').selectpicker();

  var tshirtRef = new Firebase(tshirt.firebaseTshirtUrl);
  tshirtRef.on('value', function(snapshot) {
    var image_url = snapshot.val();
    if (image_url) {
      $frontTshirtImg.attr('src', image_url);
      $checkoutTshirtImg.attr('src', image_url);
      $backTshirtImg.attr('src', image_url+'b');
    }
  });

  $('#tshirt-toggle').click(function() {
    if ($(this).data('front')) {
      $(this).data('front', false);
      $frontTshirtImg.hide();
      $backTshirtImg.show();
    } else {
      $(this).data('front', true);
      $backTshirtImg.hide();
      $frontTshirtImg.show();
    }
  });

  //sharethis
  stLight.options({publisher: "dffd3022-6ff9-44db-b81d-76a9c9c69830", doNotHash: false, doNotCopy: false, hashAddressBar: false});

})()
