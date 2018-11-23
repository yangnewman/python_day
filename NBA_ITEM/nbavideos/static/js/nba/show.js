function hrefBack() {
    history.go(-1);
}


function NewTab(search_url){
    window.open('/nba/get_search/' + search_url + '/')
}


function openWin(new_url) {
            $('body').append($('<a href="'+new_url+'" target="_blank" id="openWin"></a>'))
            document.getElementById("openWin").click();//点击事件
            $('#openWin').remove();
        }


var url =location.search;
//获取？后面的URL
alert(url);

if(url) {
    var input = url.split('search=')[1];

    alert(input);

    location.href = '/nba/get_search/' + input + '/'

}



