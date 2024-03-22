$(document).ready(function() {
    $('#acceptoffer').click(function() {
        var cateofferIdVar;
        cateofferIdVar = $(this).attr('data-listingid');
        $.get('/techtreasure/accept_offer/',
            {'listing_id': cateofferIdVar},
            function(data) {
                $('#offer_accepted').html(data);
                $('#acceptoffer').hide();
        })
    });
});
