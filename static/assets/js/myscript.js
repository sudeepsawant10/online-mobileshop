
$('.plus-cart').click(function() {
    console.log("Plus clicked");
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log(id);

    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id : id,
        },
        success: function(data) {
            console.log(data);
            console.log("PlusCart-> suceess");
            eml.innerText=data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount

        }
    })
})

$('.minus-cart').click(function() {
    console.log("Minus clicked");
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log(id);

    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id : id,
        },
        success: function(data) {
            console.log(data);
            console.log("MinusCart -> suceess");
            eml.innerText=data.quantity
            quantity_value = data.quantity
            if(quantity_value == 1){
                console.log("one value...."+data.quantity)
                // document.getElementById("fa-minus-square").disabled = true;
                document.getElementById("amount").innerText = data.amount
                document.getElementById("total_amount").innerText = data.total_amount
            }  
            else {
                // document.getElementById("fa-minus-square").disabled = false;
                document.getElementById("amount").innerText = data.amount
                document.getElementById("total_amount").innerText = data.total_amount
            } 
            

           
             
        }
    })
})

$('.remove-cart').click(function() {
    console.log("Removed clicked");
    var id = $(this).attr("pid").toString();
    var eml = this;
    console.log(id);

    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id : id,
        },
        success: function(data) {
            //reduce amount and delte the product
            console.log("delete suceess");
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
            
            eml.parentNode.parentNode.parentNode.parentNode.remove();
        }
    })
})
