window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};
document.body.addEventListener('click', (event) => {
  if (!event.target.matches('.delete-button')) return;
  delete_venue();
});
function delete_venue(){
  const deleteBtns  = document.querySelectorAll('.delete-button');
  for (let i=0; i < deleteBtns .length; i++){
      const btn = deleteBtns[i];
      btn.onclick = function(e){
          const venueID = e.target.dataset['id'];
          fetch('/venues/'+ venueID, {
              method: 'DELETE'
          })
          .then(function() {
              const item = e.target.parentElement;
              console.log(item);
              item.remove();
          })
      }
  }}
