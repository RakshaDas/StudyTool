$(document).ready(function() {

  // SideNav Button Initialization
  $(".button-collapse").sideNav({
    breakpoint: 1200
  });
  // SideNav Scrollbar Initialization
  var sideNavScrollbar = document.querySelector('.custom-scrollbar');
  var ps = new PerfectScrollbar(sideNavScrollbar);
});

// Material Select Initialization
$(document).ready(function () {
  $('.mdb-select').materialSelect();
});

/* WOW.js init */
new WOW().init();


toastr.options = {
  "positionClass": "md-toast-bottom-right"
}

// Tooltips Initialization
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});

// Tinymce Initialization
tinyMCE.init({
    selector: ".tinymce",
    menubar: false,
    plugins: 'wordcount codesample link lists table',
    toolbar: 'undo redo | formatselect | bold italic underline strikethrough superscript subscript | table blockquote codesample link | alignleft aligncenter alignright alignjustify | bullist numlist | outdent indent lineheight | removeformat',
    content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }',
    height : "300",
});