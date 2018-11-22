


// var cur_page = 1;
// var page_size = 5;
//
// $(function(){
//     $(window).scroll(function(){
//         var scrollTop = $(window).scrollTop();
//         var owinH=$(window).height();
//         var odocH = $(document).height();
//         if(scrollTop + owinH >= odocH){
//             //console.log("这里是滚到底部的处理分页，这里需要你请求后台的数据！！")
//             ++cur_page;
//             loadList( cur_page,page_size);
//         }
//
//     });
// });



$(document).ready(function() {

    var csrf = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url:'/names/hundred_name/',
        type:'GET',
        dataType:'json',
        headers:{'X-CSRFToken':csrf},
        success: function (data) {
            var f_str = '';
            for(var j=0;j<data.length;j++){
                var title = data[j].title;
                var nums = data[j].nums;

                f_str += '<figure class="white">\n' +
                    '                                <a href="/names/name_list/' + title + '/">\n' +
                    '                                    <dl>\n' +
                    '                                        <dt>有' + nums + '个姓名</dt>\n' +
                    '                                    </dl>\n' +
                    '\n' +
                    '                                <div id="wrapper-part-info">\n' +
                    '                                    <div id="part-info" style="font-size:16px font">' + title + '姓名大全</div>\n' +
                    '                                </div>\n' +
                    '                                </a>\n' +
                    '                            </figure>'

            }
            $('.work').append(f_str)

        },
        error: function(data) {
            alert('请求失败')
        }


    });

});





