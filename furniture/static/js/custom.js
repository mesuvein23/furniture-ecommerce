$('.addToCartBtn').click(function (e) { 
    e.preventDefault();
    
    var product_id = this.dataset.product
    var action = this.dataset.action
    var cart_quantity = $('#cartValue').val();
    console.log('Product ID:', product_id, 'Action:', action,'CartQty:', cart_quantity)

    $.ajax({
        method: "POST",
        url: "/add-to-cart/",
        data: {
            'product_id' : product_id,
            'action': action,
            'cart_quantity' : cart_quantity,
            'csrfmiddlewaretoken' : csrftoken,
        },
        success: function (response) {
            console.log(response)
            alertify.success(response.status)
        }
    })
})    


$(document).ready(function() {

    $('.incrementBtn').click(function (e){
        e.preventDefault();

        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(inc_value,10);
        value = isNaN(value) ? 0 : value;
        if(value < 10)
        {
            value++;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });
});

$(document).ready(function() {

    $('.decrementBtn').click(function (e){
        e.preventDefault();

        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(inc_value,10);
        value = isNaN(value) ? 0 : value;
        if(value > 1)
        {
            value--;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });
});

$('.changeQuantity').click(function (e) {
    e.preventDefault();

    var product_id = this.dataset.product
    var cart_quantity = $(this).closest('.product_data').find('.qty-input').val();
    console.log('Product ID:', product_id,'CartQty:', cart_quantity)

    $.ajax({
        method: "POST",
        url: "/update_item/",
        data: {
            'product_id' : product_id,
            'cart_quantity' : cart_quantity,
            'csrfmiddlewaretoken': csrftoken,
        },
        success: function (response) {
            alertify.success(response.status);
            setTimeout(function() {
                location.reload();
            }, 3); 
        }

    })
})


$('.delete-cart-item').click(function (e) {
    e.preventDefault();

    var product_id = this.dataset.product
    // var product_id = $(this).closest('.product_data').find('.prod_id').val()
    console.log('Product ID:', product_id)

    $.ajax({
        method: "POST",
        url: "/delete-cart-item/",
        data: {
            'product_id' : product_id,
            'csrfmiddlewaretoken': csrftoken,
        },
        success: function (response) {
            alertify.success(response.status)
            $('.cartdata').load(location.href + " .cartdata");
        }
    })
})




