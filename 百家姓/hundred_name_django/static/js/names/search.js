

$(document).ready(function() {

    var url =location.search;
    //获取？后面的URL
    // alert(url);
    var input = url.split('search=')[1];
    // alert(input);

    if (input != undefined){

        location.href = '/names/search/'+input+'/'

    }


});






