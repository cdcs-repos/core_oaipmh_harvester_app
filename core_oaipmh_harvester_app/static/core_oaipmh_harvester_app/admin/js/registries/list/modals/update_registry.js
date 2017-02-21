/**
 * Check the availability of a registry
 */
updateRegistry = function(event)
{
    event.preventDefault();

    var $registryRow = $(this).parent().parent();
    var objectID = $registryRow.attr("objectid");
    $("#bannerUpdate"+objectID).show(200);
    $("#update"+objectID).hide(200);

    $.ajax({
        url : updateRegistryGetUrl,
        type : "GET",
        dataType: "json",
        async: true,
        data : {
        	id : objectID,
        },
        success: function(data){
            checkUpdateData();
        },
        error:function(data){

        },
    });
}

checkUpdateData = function()
{
    return $.ajax({
        url : checkUpdateRegistryGetUrl,
        type : "GET",
        dataType: "json",
        async: true,
        data : {
        },
        success: function(data){
            $.map(data, function (item) {
                if(item.is_updating)
                {
                    $("#update" + item.registry_id).hide(200);
                    $("#bannerUpdate"+ item.registry_id).show(200);
                }
                else
                {
                    $("#bannerUpdate"+ item.registry_id).hide(200);
                    $("#update" + item.registry_id).show(200);
                    $("#name"+ item.registry_id).html(item.name);
                }
             });
        },
        error:function(data){
	    }
    });
}

updateAllRegistries = function(event)
{
    $('.update-registry-btn').click();
}

$(document).ready(function() {
    $('.update-registry-btn').on('click', updateRegistry);
    $('.update-all-registries-btn').on('click', updateAllRegistries);
});