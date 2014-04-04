$.get('/api/popular-tags/?num=10', function(tags) {
  var source = $('#tag-list-template').html();
  var tag_list_template = Handlebars.compile(source);
  $('#tag-list').append(tag_list_template(tags));
});
