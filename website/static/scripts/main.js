function hideAlert(alert) {
  document.getElementById(alert).remove();
}

function deletePost(id) {
  fetch("/delete-post", {
    method: "POST",
    body: JSON.stringify({ id: id }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
