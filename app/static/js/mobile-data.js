$(document).ready(function() {
    // Fetch JSON data from Flask endpoint
    $.ajax({
        url: '/items/json',
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            // Iterate over each item in the JSON response
            response.forEach(function(item) {
                // Example: Append item details to a container using Bootstrap elements
                $('#items-container').append(
                    `<div class="card">
                        <img src="${item.image}" class="card-img-top" alt="...">
                        <div class="card-body">
                            <h5 class="card-title">${item.name}</h5>
                            <p class="card-text">${item.description}</p>
                            <p class="card-text">$${item.price}</p>
                        </div>
                    </div>`
                );
            });
        },
        error: function(error) {
            console.error('Error fetching items:', error);
        }
    });
});
