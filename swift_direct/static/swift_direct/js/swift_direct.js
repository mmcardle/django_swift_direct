;$(function () {
    'use strict';
    $('.swift_direct').each(function(i, swift_direct){

        var sd = $(swift_direct);
        var file_url_element = sd.find('input[type=hidden]').first();
        var progress_element = sd.find('progress').first();

        sd.find('input.fileinput').each(function(j, input){

            var progress = function(e, data){
                var progress = parseInt(data.loaded / data.total * 100, 10)
                progress_element.val(progress);
            }

            var fileuploaddone = function (e, data) {
                file_url_element.val(data.url);
            }

            var fileuploadadd = function (e, data) {
                file_url_element.val('');
                progress_element.val(0);
            }

            var data_url = $(swift_direct).attr('data-url');
            $(input).change(function(){
                $(this.files).each(function(i, up_file){
                    $.ajax({
                        url:data_url,
                        method:'POST',
                        data: { name: up_file.name },
                    }).done(function (result) {
                        var nf = $(input).clone();
                        nf.bind('fileuploaddone', fileuploaddone);
                        nf.bind('fileuploadadd', fileuploadadd);
                        nf.bind('fileprogress', progress);
                        nf.fileupload({type: 'PUT', multipart: false, progress:progress});
                        nf.fileupload('add', {files: [up_file], url: result.temp_url});
                    });
                });
            });
        });
    });

});