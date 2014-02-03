var TEMPLATE = '<li data-model="{{id}}"><img src="{{image}}" width="200"><p></p></li>',
    last_timestamp_tumblr = null;

function tumblrCallback(response) {
    var tags = response.response,
        photos, template, photo;

    for (var i = 0, len = tags.length; i < len; i = i + 1) {
        tag = tags[i];
        photos = tag.photos;

        if (photos) {
            for (var j = 0, len_j = photos.length; j < len_j; j = j + 1) {
                photo = photos[j];
                template = TEMPLATE.replace('{{image}}', photo.original_size.url)
                                   .replace('{{id}}', tag.id)
                                   .replace('{{caption}}', photo.caption);

                $('#tiles').append($(template));
            } // end second loop
        }

    } // end first loop
    last_timestamp_tumblr = tag.timestamp;
}

$(document).ready(function () {
    var inst_clinet_id = $('#js-main').attr('data-client-inst-id'),
        tumblr_id = $('#js-main').attr('data-tumblr-id'),
        tag = $('#search').val(),
        $tiles = $('#tiles'),
        $handler = $('li', $tiles),
        $main = $('#main'),
        $window = $(window),
        $document = $(document),
        feed,
        tumblr_limit = 20,
        tumblr_page = 0;

    /**
     * Reinitializes the wookmark handler after all images have loaded
     */
    function applyLayout() {
        $tiles.imagesLoaded(function() {
            // Destroy the old handler
            if ($handler.wookmarkInstance) {
                $handler.wookmarkInstance.clear();
            }

            // Create a new layout handler.
            $handler = $('li', $tiles);
            $handler.wookmark({
                autoResize: true, // This will auto-update the layout when the browser window is resized.
                container: $main, // Optional, used for some extra CSS styling
                offset: 20, // Optional, the distance between grid items
                itemWidth: 210 // Optional, the width of a grid item
            });
        });
    }
    function reset() {
        $('#tiles').html('');
        $('#main').css('height', '0px');
        feed = new Instafeed({
            target: 'tiles',
            get: 'tagged',
            links: false,
            limit: 15,
            resolution: 'low_resolution',
            tagName: tag,
            clientId: inst_clinet_id,
            template: TEMPLATE,
            after: function () {
                // Call the layout function for the first time
                applyLayout();
            }
        });
        feed.run();
        tumblrPhotos();
    }

    function tumblrPhotos() {
        var script = $('<script type="text/javascript"></script>')
        script.attr('src', 'http://api.tumblr.com/v2/tagged?callback=tumblrCallback&offset=' +
                           (tumblr_page * tumblr_limit) + '&limit=' + tumblr_limit + '&api_key=' + tumblr_id +
                           '&tag=' + tag + (last_timestamp_tumblr ? '&before=' + last_timestamp_tumblr : ''));
        $('head').append(script);
        tumblr_page = tumblr_page + 1;
    }

    /**
     * When scrolled all the way to the bottom, add more tiles
     */
    function onScroll() {
        // Check if we're within 100 pixels of the bottom edge of the broser window.
        var winHeight = window.innerHeight ? window.innerHeight : $window.height(), // iphone fix
            closeToBottom = ($window.scrollTop() + winHeight > $document.height() - 100);

        if (closeToBottom) {
            feed.run();
            applyLayout();
            tumblrPhotos()
        }
    };

    $('#search').change(function () {
        tag = $('#search').val();
        reset();
    }).click(function () {
        $('#search')[0].select();
    }).keydown(function (e) {
        if (e.keyCode !== 8 && e.keyCode != 13 && (e.keyCode < 65 || e.keyCode > 90)) {
            return false;
        }
    });

    reset();

    // Capture scroll event.
    $window.bind('scroll.wookmark', onScroll);
});
