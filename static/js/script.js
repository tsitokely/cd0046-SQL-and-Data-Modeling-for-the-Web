window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

document.body.addEventListener('click', (event) => {
  if (event.target.matches('.delete-button-venue')){
          const venueID = event.target.dataset['id'];
          fetch('/venues/'+ venueID, {
              method: 'DELETE',
              headers: {
                'Content-type': 'application/json; charset=UTF-8'
              },
          }).then(() => window.location.replace("../"))
      }
  else if (event.target.matches('.delete-button-artist')){
    const artistID = event.target.dataset['id'];
    fetch('/artists/'+ artistID, {
        method: 'DELETE',
        headers: {
          'Content-type': 'application/json; charset=UTF-8'
        },
    }).then(() => window.location.replace("../"))
  }
    else {return}
  })