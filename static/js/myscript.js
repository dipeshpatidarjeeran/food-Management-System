function increaseQty() {
  let qty = document.getElementById("quantity");
  qty.value = parseInt(qty.value) + 1;
}

function decreaseQty() {
  let qty = document.getElementById("quantity");
  if (parseInt(qty.value) > 1) {
    qty.value = parseInt(qty.value) - 1;
  }
}
