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

function filter(parentId, filterItem, word){
    const table = document.getElementById(parentId);
    const rows = table.getElementsByTagName(filterItem);
    for (let i = 1; i < rows.length; i++) {
        const rowText = rows[i].textContent.toLowerCase();
        if (!rowText.includes(word.toLowerCase())) {
            rows[i].style.display = 'none';
        } else {
            rows[i].style.display = '';
        }
    }
}

