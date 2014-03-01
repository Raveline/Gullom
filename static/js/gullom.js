/* Gullom.js 
 * Small functions for Gullom */

var Gullom = new function() {
    this.tags_add = "";
    this.gifs_get = "";
    this.gifs_add = "";

    var SELECTED_TAGS = ".selected";
    var TAGS_REPO = "ul#every-tags";
    var TAGS_LIST = ".tags-list";
    var SUCCESS = "success";
    var PICKED_TAG = "picked";
    var TAG_ADDER = 'input[name="tags"]';
    var GIF_LIST = '.gifs-list';

var add_tag = function() {
    new_tag = $(TAG_ADDER).val();
    $.post(Gullom.tags_add, {tag : new_tag}, function(data) {
        if (data.result == SUCCESS) {
            append_new_tag(new_tag, data.id);
            $('#' + data.id).trigger('click');
        }
    });
};

/* When selecting tags in pick mode, display only relevant
 * gifs */
var discriminate = function() {
    clean_gifs();
    $.get(Gullom.gifs_get, {'tags[]':get_selected_tags()}, function(data) {
        if (data.result == SUCCESS) {
            append_gifs(data.gifs);
        }
    });
}

var get_selected_tags = function() {
    return $(".selected").map(function() { return this.id }).get();
}

var clean_gifs = function(gifs) {
    $(GIF_LIST).empty();
}

var append_gifs = function(gifs) {
    var to_append = []
    gifs.map(function(item) {
        to_append.push(get_append_gif(item));
    });
    $(GIF_LIST).append(to_append.join(''));
}

var get_append_gif = function(gif) {
    tags = get_ul_tags(gif);
    var to_append= ['<div class="gif"><a href="', gif.path, '">', gif.name, '</a><div class="gif-tags">', tags, '</div></div>'];
    return to_append.join('');
}

var get_ul_tags = function(gif) {
    var to_return = ["<ul>"];
    gif.tags.map(function(item) {
        to_return.push('<li>');
        to_return.push(item);
        to_return.push('</li>');
    });
    to_return.push("</ul>");
    return to_return.join('');
}


/**
 * When adding tags to a new gif,
 * will send those in the box under the gif **/
var append_selected_tag = function (label, id){
    tag = ['<li class="', PICKED_TAG, '" id="P', id, '">', label, '</li>'];
    $(TAGS_LIST).append(tag.join(''));
};

var append_new_tag = function(label, id) {
    tag = ['<li class="tag", id="', id, '">', label, '</li>'];
    $(TAGS_REPO).append(tag.join(''));
}

var delete_tag = function(tag_id) {
    $.ajax({
        url: Gullom.tags_add + '/' + tag_id, 
        method: 'DELETE',
        success: function(data) {
        if (data.result == SUCCESS)
            remove_tag(tag_id);
        }
    });
}

var turn_tag = function(tag) {
    if (tag.hasClass('selected')) {
        tag.removeClass('selected');
        tag.addClass('tag');
    } else {
        tag.removeClass('tag');
        tag.addClass('selected');
    }
    if (tag.hasClass('deletable'))
        tag.removeClass('deletable');
}

var remove_tag = function(tag_id) {
    $('#'+tag_id).remove();
    $('#P'+tag_id).remove();
}

this.init = function(tags, ggifs, agif, pmeme, rmeme) {
    this.tags_add = tags;
    this.gifs_get = ggifs;
    this.gifs_add = agif;
    this.meme_post = pmeme;
    this.render_meme = rmeme;
};

var reset_form = function() {
    $("form input[type='text']").val('');
    $('.selected').trigger('click');
}

var handle_deletion = function(item) {
    if (item.hasClass('deletable'))
        delete_tag(item.attr('id'));
    else 
        item.addClass('deletable');
}

var basic_events = function(tag_click_event) {
   $('ul#every-tags').on('contextmenu', 'li', function(e) {
       handle_deletion($(this));
       return false;
   });

   $('ul#every-tags').on('click', 'li', function(e) {
       tag_click_event($(this));
   });
}

this.pick_mode = function() {
    $(document).ready(function() {
        basic_events(function(tag) {
            turn_tag(tag);
            discriminate();
        });

        $('.gifs-list').on('mouseenter', 'div', function(e) {
            item = $(this);
            to_append=['<div class="gifpreview"><img src="', item.children('a').attr('href'), '"></div>'].join('');
            item.append(to_append);
        });

        $('.gifs-list').on('mouseleave', 'div', function(e) {
            $(this).children('.gifpreview').remove();
        });

    });
}

this.add_mode = function() {
    $(document).ready(function() {
        // To do when tag is selected
        basic_events(function(tag) {
            if (tag.hasClass('selected')) 
                $('.tags-list li#P' + tag.attr('id')).remove();
            else 
                append_selected_tag(tag.text(),tag.attr('id'));
            turn_tag(tag);
        });

        $(TAG_ADDER).keypress(function(e) {
            if (e.which == 13) {
                add_tag();
                return false;
            }
        });

        $('form').submit(function() {
            var name = $('input[name="name"]').val();
            var url = $('input[name="url"]').val();
            var tags = $(".tags-list li").map(function() { return this.id.substring(1) }).get().toString();
            if (name.length != 0 && url.length != 0) {
                $.post(Gullom.gifs_add, {'url' : url, 'name': name, 'tags' : tags}, (function(data) {
                    // TODO : add a temp message.
                }));
            }
            reset_form();
            return false;
        });
    });
};

this.memeadd_mode = function() {
    $('form').submit(function() {
        var name = $('input[name="name"]').val();
        var url = $('input[name="url"]').val();
        var text1 = $('input[name="text1"]').val();
        var text2 = $('input[name="text2"]').val();
        
        if (name.length != 0 && url.length != 0) {
            $.post(Gullom.meme_post, {'url' : url
                                    , 'name': name
                                    , 'text1' : text1
                                    , 'text2' : text2}, (function(data) {
                // TODO : add a temp message.
            }));
        }
        reset_form();
        return false;
    });
}

this.meme_mode = function() {
    $('form').submit(function() {
        var text1 = $('input[name="text1"]').val();
        var text2 = $('input[name="text2"]').val();
        var file = $('select :selected').val();
        
        $.post(Gullom.render_meme, {'text1' : text1 
                                 , 'text2' : text2
                                 , 'filename' : file}
                , (function(data) {
                // TODO : add a temp message.
            })).done(function(answer) {
                if (answer.result == SUCCESS) {
                    $("#currentMeme").attr("src", answer.file);
                }
            });
        reset_form();
        return false;
    });

    $('select').change(function() {
        $("#currentMeme").attr("src", '/static/storedmemes/' + $('select :selected').val());
    }).change();
}

};
