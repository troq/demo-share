function setZIndex () {
  var imageLinks = $('#showcase .item-link');
  var count = imageLinks.length;
  imageLinks.each(function(i) {
    $(this).css('z-index', count-i+1).siblings('.item-caption').css('z-index', count-i);
  });
}

$('#detailed').endlessPaginate({
  paginateOnScroll: true,
  paginateOnScrollMargin: 20,
});

$('#showcase').endlessPaginate({
  paginateOnScroll: true,
  paginateOnScrollMargin: 20,
  onCompleted: setZIndex,
});

$.fn.editable.defaults.ajaxOptions = {type: "PUT"};
$('#tagline').editable({
  send: 'always',
  params: function(params) {
    return {tagline: params.value};
  }
});

setZIndex();
