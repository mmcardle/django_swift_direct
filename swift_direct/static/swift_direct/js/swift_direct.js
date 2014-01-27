;$(function () {
    'use strict';
    $('.swift_direct').each(function(i, swift_direct){
        var sd = $(swift_direct);
        if(sd.hasClass('sd-init')){
            // Don't initialize twice;
            return sd;
        }else{
            sd.addClass('sd-init');
        }
        var file_url_element = sd.find('input[type=hidden]').first();
        var progress_element = sd.find('progress').first();
        var data_url = $(swift_direct).attr('data-url');
        var slo_url = $(swift_direct).attr('data-slo-url');
        var slo_threshold = parseInt($(swift_direct).attr('data-slo-threshold'));
        var slo_chunk_size = parseInt($(swift_direct).attr('data-slo-chunk-size'));
        var filename = $(swift_direct).attr('data-filename');
        var filename_elements = $(swift_direct).find('.swift_direct_filename');

        sd.find('input.fileinput').each(function(j, input){

            var done = function(e, data){
                file_url_element.val(sd.file_url);
            }

            var progressall = function(e, data){
                var progress = parseInt(data.loaded / data.total * 100, 10)
                progress_element.val(progress);
            }

            var add = function(e, data){
                filename_elements.text(sd.upload_filename);
                file_url_element.val('');
                progress_element.val(0);
            }

            $(input).change(function(){
                $(this.files).each(function(i, up_file){
                    sd.upload_filename = filename || up_file.name;

                    var nf = $(input).clone();
                    nf.bind('fileuploaddone', done);
                    nf.bind('fileuploadadd', add);
                    nf.bind('fileuploadprogressall', progressall);
                    nf.fileupload({type: 'PUT', multipart: false});

                    if(up_file.size < slo_threshold){
                        // Upload as single file
                        $.ajax({
                            url:data_url,
                            method:'POST',
                            data: { name: sd.upload_filename },
                        }).done(function (result) {
                            nf.fileupload('add', {files: [up_file], url: result.temp_url});
                            sd.file_url =  result.file_url;
                        });
                    }else{
                        // Upload as SLO object

                        var file_chunks = [];
                        sd.slo_chunks = [];

                        var slo_done = function(e, data){
                            var etag = data.jqXHR.getResponseHeader('Etag')
                            sd.slo_chunks[data.url]['etag'] = etag;
                            sd.slo_chunks[data.url]['size'] = data.loaded;
                        }

                        var slo_stop = function(e){
                            var slo_array = [];

                            for(var x in sd.slo_chunks ) {
                                i = sd.slo_chunks[x].index;
                                slo_array[i] = {}
                                slo_array[i].path=sd.slo_chunks[x].path
                                slo_array[i].etag=sd.slo_chunks[x].etag
                                slo_array[i].size_bytes=sd.slo_chunks[x].size
                            }

                            var blob = JSON.stringify(slo_array)
                            $.ajax({
                                url:slo_url,
                                method:'POST',
                                data: {
                                    name: sd.upload_filename,
                                    slo: blob
                                },
                            }).done(function (result) {
                                sd.file_url =  result.file_url;
                                file_url_element.val(sd.file_url);
                            });
                        }

                        nf.bind('fileuploadstop', slo_stop);
                        nf.bind('fileuploaddone', slo_done);

                        var func = (up_file.slice ? 'slice' : (up_file.mozSlice ? 'mozSlice' : (up_file.webkitSlice ? 'webkitSlice' : 'slice')))

                        for(var start=0;start<up_file.size;start=start+slo_chunk_size){
                            var chunk_start = start;
                            var chunk_end = (chunk_start+slo_chunk_size>up_file.size) ? up_file.size : chunk_start + slo_chunk_size;
                            var file_slice  = up_file[func](chunk_start, chunk_end);
                            file_chunks.push(file_slice);
                        }

                        $(file_chunks).each(function(i, chunk){
                            var upload_filename = sd.upload_filename + '.chunk.'+i;
                            $.ajax({
                                url:data_url,
                                method:'POST',
                                data: { name: upload_filename },
                            }).done(function (result) {
                                nf.fileupload('add', {files: [chunk], url: result.temp_url});
                                sd.slo_chunks[result.temp_url] = {};
                                sd.slo_chunks[result.temp_url]['path'] = result.file_path;
                                sd.slo_chunks[result.temp_url]['index'] = i;
                            });
                        });
                    }
                });
            });
        });
    });
});