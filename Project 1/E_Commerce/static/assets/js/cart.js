document.addEventListener("DOMContentLoaded", function() {
    console.log('DOM Loaded');

    const increaseButtons = document.querySelectorAll(".increase-quantity");
    const decreaseButtons = document.querySelectorAll(".decrease-quantity");
    const quantityElements = document.querySelectorAll(".item-quantity");
    const priceElements = document.querySelectorAll(".cart-item-price");
    const totalPriceElement = document.getElementById("total-price");

    console.log('priceElements:', priceElements);
    console.log('totalPriceElement:', totalPriceElement);

    let totalPrice = 0;

    increaseButtons.forEach((button, index) => {
        button.addEventListener("click", (event) => {
            console.log('Increase button clicked');
            event.preventDefault();
            const currentItem = event.target.closest(".cart-item");
            const quantityElement = currentItem.querySelector(".item-quantity");
            const priceElement = currentItem.querySelector(".cart-item-price");
            const pricePerItem = parseFloat(priceElement.getAttribute("data-price"));
            const currentQuantity = parseInt(quantityElement.textContent);

            quantityElement.textContent = currentQuantity + 1;
            const itemTotalPrice = pricePerItem * (currentQuantity + 1);
            updateCartItemPrice(priceElement, itemTotalPrice);
            updateTotalPrice();
        });
    });

    decreaseButtons.forEach((button, index) => {
        button.addEventListener("click", (event) => {
            console.log('Decrease button clicked');
            event.preventDefault();
            const currentItem = event.target.closest(".cart-item");
            const quantityElement = currentItem.querySelector(".item-quantity");
            const priceElement = currentItem.querySelector(".cart-item-price");
            const pricePerItem = parseFloat(priceElement.getAttribute("data-price"));
            const currentQuantity = parseInt(quantityElement.textContent);

            if (currentQuantity > 1) {
                quantityElement.textContent = currentQuantity - 1;
                const itemTotalPrice = pricePerItem * (currentQuantity - 1);
                updateCartItemPrice(priceElement, itemTotalPrice);
                updateTotalPrice();
            }
        });
    });

    function updateCartItemPrice(priceElement, itemTotalPrice) {
        priceElement.textContent = "Rs. " + itemTotalPrice.toFixed(2);
        console.log('updateCartItemPrice called. Item Total Price:', itemTotalPrice);
    }

    function updateTotalPrice() {
        totalPrice = Array.from(priceElements)
            .map(priceElement => parseFloat(priceElement.textContent.replace("Rs. ", "")))
            .reduce((sum, price) => sum + price, 0);
        
        totalPriceElement.textContent = "Rs. " + totalPrice.toFixed(2);
        console.log('updateTotalPrice called. Total Amount:', totalPrice);
    }
});