$(".plus-cart").click(function () {
  console.log("Plus clicked");
  // take product id
  var id = $(this).attr("pid").toString();
  //
  var eml = this.parentNode.children[2];
  console.log(eml);
  console.log(id);
  // console.log(eml);
  $.ajax({
    type: "GET",
    url: "/pluscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      console.log(data);
      console.log("PlusCart-> suceess");
      eml.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("delivery-charges").innerText =
        data.delivery_charges;
      document.getElementById("total_amount").innerText = data.total_amount;
    },
  });
});

$(".minus-cart").click(function () {
  console.log("Minus clicked");
  var id = $(this).attr("pid").toString();
  var eml = this.parentNode.children[2];
  console.log(id);

  $.ajax({
    type: "GET",
    url: "/minuscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      console.log(data);
      console.log("MinusCart -> suceess");
      eml.innerText = data.quantity;
      quantity_value = data.quantity;
      if (quantity_value >= 2) {
        console.log("one value...." + data.quantity);
        document.getElementsByClassName("minus-cart").disabled = true;
        // document.getElementById("amount").innerText = data.amount
        // document.getElementById("total_amount").innerText = data.total_amount
      }

      // document.getElementById("fa-minus-square").disabled = false;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("delivery-charges").innerText =
        data.delivery_charges;
      document.getElementById("total_amount").innerText = data.total_amount;
    },
  });
});

$(".remove-cart").click(function () {
  console.log("Removed clicked");
  var id = $(this).attr("pid").toString();
  var eml = this;
  console.log(id);

  $.ajax({
    type: "GET",
    url: "/removecart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      //reduce amount and delte the product
      console.log("delete suceess");
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("delivery-charges").innerText =
        data.delivery_charges;
      document.getElementById("total_amount").innerText = data.total_amount;

      eml.parentNode.parentNode.parentNode.parentNode.remove();
    },
  });
});

function valueChange() {
  console.log("event gets called....");
  if (document.getElementById("credit-debit-card").checked == true) {
    alert("credit selected");
  }
}

$('.cancel-order').click(function(){
    alert("Your order will be cancelled and order amount refund within 24 hrs.");
});

function showPassword() {
    var pass = document.getElementById('myInput');
    console.log(pass);
    if (pass.type == 'password'){
        pass.type = 'text';
    }
    else {
      pass.type='password';
    }

}
function showPassword2() {
    var pass = document.getElementById('myInput2');
    console.log(pass);
    if (pass.type == 'password'){
        pass.type = 'text';
    }
    else {
      pass.type='password';
    }

}

$('.pay-by-card').click(function(){
  alert("After payment successful your order will be placed!");
});