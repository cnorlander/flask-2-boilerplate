document.addEventListener("DOMContentLoaded", function(event){
    document.addEventListener('click', handleClickEvent);
    document.addEventListener('touchstart', handleClickEvent);
      // Check if URL has #aside-open hash
    function handleClickEvent(event) {
      var nav = document.querySelector('nav');
      var isNavOpen = window.location.hash == '#sidenav-open';
      var isDescendant = nav.contains(event.target);


      if (!isDescendant && isNavOpen) {
        document.getElementById("sidenav-close").click()
      }
    }
});

