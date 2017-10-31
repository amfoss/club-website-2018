(function($) {

    "use strict";

    /* ---------------------------------------------- /*
     * Preloader
    /* ---------------------------------------------- */

    $(window).load(function() {
        $('.page-loader').delay(350).fadeOut('slow');
    });

    $(document).ready(function() {

        var moduleHero = $('.module-hero, .module-map'),
            mobileTest;

        /* ---------------------------------------------- /*
         * Mobile detect
        /* ---------------------------------------------- */

        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            mobileTest = true;
        } else {
            mobileTest = false;
        }

        /* ---------------------------------------------- /*
         * Full height module
        /* ---------------------------------------------- */

        $(window).resize(function() {
            if (moduleHero.length > 0) {
                if (moduleHero.hasClass('js-fullheight')) {
                    moduleHero.height($(window).height());
                } else {
                    moduleHero.height($(window).height() * 0.65);
                }
            }
        }).resize();

        /* ---------------------------------------------- /*
         * Intro slider setup
        /* ---------------------------------------------- */

        $('#slides').superslides({
            play: 10000,
            animation: 'fade',
            animation_speed: 800,
            pagination: true,
        });

        /* ---------------------------------------------- /*
         * Setting background of modules
        /* ---------------------------------------------- */

        var modules = $('.module-hero, .module, .module-sm, .module-xs, .sidebar');

        modules.each(function() {
            if ($(this).attr('data-background')) {
                $(this).css('background-image', 'url(' + $(this).attr('data-background') + ')');
            }
        });

        /* ---------------------------------------------- /*
         * Parallax
        /* ---------------------------------------------- */

        if (mobileTest === true) {
            modules.css({
                'background-attachment': 'scroll'
            });
        }

        /* ---------------------------------------------- /*
         * Youtube video background
        /* ---------------------------------------------- */

        $(function() {
            $('.video-player').mb_YTPlayer();
        });

        /* ---------------------------------------------- /*
         * Portfolio
        /* ---------------------------------------------- */

        var filters = $('#filters'),
            worksgrid = $('#works-grid');

        $('a', filters).on('click', function() {
            var selector = $(this).attr('data-filter');
            $('.current', filters).removeClass('current');
            $(this).addClass('current');
            worksgrid.isotope({
                filter: selector
            });
            return false;
        });

        $(window).on('resize', function() {
            worksgrid.imagesLoaded(function() {
                worksgrid.isotope({
                    layoutMode: 'masonry',
                    itemSelector: '.work-item',
                    transitionDuration: '0.3s',
                });
            });
        }).resize();

        /* ---------------------------------------------- /*
         * Team hover
        /* ---------------------------------------------- */

        var team_item = $('.team-item');

        team_item.mouseenter(function() {
            $(this).addClass('js-hovered');
            team_item.filter(':not(.js-hovered)').addClass('js-fade');
        });

        team_item.mouseleave(function() {
            $(this).removeClass('js-hovered');
            team_item.removeClass('js-fade');
        });

        /* ---------------------------------------------- /*
         * Owl sliders
        /* ---------------------------------------------- */

        $('.slider').owlCarousel({
            stopOnHover: !0,
            singleItem: !0,
            autoHeight: !0,
            navigation: !0,
            pagination: !1,
            slideSpeed: 400,
            paginationSpeed: 1000,
            goToFirstSpeed: 2000,
            autoPlay: 3000,
            navigationText: [
                '<i class="fa fa-angle-left"></i>',
                '<i class="fa fa-angle-right"></i>'
            ],
        });

        $('.slider-reviews').owlCarousel({
            stopOnHover: !0,
            singleItem: !0,
            autoHeight: !0,
            slideSpeed: 400,
            navigation: !0,
            pagination: !1,
            paginationSpeed: 1000,
            goToFirstSpeed: 2000,
            autoPlay: 3000,
            navigationText: [
                '<img src="assets/images/arrow-l.png" alt="arrow">',
                '<img src="assets/images/arrow-r.png" alt="arrow">'
            ],
        });

        $('.slider-clients').owlCarousel({
            stopOnHover: !0,
            singleItem: !1,
            autoHeight: !0,
            navigation: !1,
            pagination: !1,
            slideSpeed: 400,
            paginationSpeed: 1000,
            goToFirstSpeed: 2000,
            autoPlay: 3000,
            navigationText: [
                '<i class="fa fa-angle-left"></i>',
                '<i class="fa fa-angle-right"></i>'
            ],
        });

        /* ---------------------------------------------- /*
         * Progress bars, counters animations
        /* ---------------------------------------------- */

        $('.progress-bar').each(function() {
            $(this).appear(function() {
                var percent = $(this).attr('aria-valuenow');
                $(this).animate({
                    'width': percent + '%'
                });
                $(this).find('.progress-value').countTo({
                    from: 0,
                    to: percent,
                    speed: 900,
                    refreshInterval: 30
                });
            });
        });

        $('.counter').each(function() {
            $(this).appear(function() {
                var number = $(this).find('.counter-timer').attr('data-to');
                $(this).find('.counter-timer').countTo({
                    from: 0,
                    to: number,
                    speed: 1500,
                    refreshInterval: 30
                });
            });
        });

        /* ---------------------------------------------- /*
         * Gallery
        /* ---------------------------------------------- */

        $('.gallery-item a').magnificPopup({
            type: 'image',
            gallery: {
                enabled: true
            },
        });

        /* ---------------------------------------------- /*
         * A jQuery plugin for fluid width video embeds
        /* ---------------------------------------------- */

        $('body').fitVids();

        /* ---------------------------------------------- /*
         * Google Map
        /* ---------------------------------------------- */

        var mapID = $('#map');
        var isDraggable = Math.max($(window).width(), window.innerWidth) > 480 ? true : false;

        mapID.each(function() {

            var GMaddress = mapID.attr('data-address');

            mapID.gmap3({
                action: "init",
                marker: {
                    address: GMaddress,
                    options: {
                        icon: 'assets/images/map-icon.png'
                    }
                },
                map: {
                    options: {
                        zoom: 16,
                        zoomControl: true,
                        zoomControlOptions: {
                            style: google.maps.ZoomControlStyle.SMALL
                        },
                        mapTypeControl: true,
                        scaleControl: false,
                        scrollwheel: false,
                        streetViewControl: false,
                        draggable: isDraggable,
                        styles: [{
                            "featureType": "water",
                            "elementType": "geometry",
                            "stylers": [{
                                "color": "#e9e9e9"
                            }, {
                                "lightness": 17
                            }]
                        }, {
                            "featureType": "landscape",
                            "elementType": "geometry",
                            "stylers": [{
                                "color": "#f5f5f5"
                            }, {
                                "lightness": 20
                            }]
                        }, {
                            "featureType": "road.highway",
                            "elementType": "geometry.fill",
                            "stylers": [{
                                "color": "#ffffff"
                            }, {
                                "lightness": 17
                            }]
                        }, {
                            "featureType": "road.highway",
                            "elementType": "geometry.stroke",
                            "stylers": [{
                                "color": "#ffffff"
                            }, {
                                "lightness": 29
                            }, {
                                "weight": 0.2
                            }]
                        }, {
                            "featureType": "road.arterial",
                            "elementType": "geometry",
                            "stylers": [{
                                "color": "#ffffff"
                            }, {
                                "lightness": 18
                            }]
                        }, {
                            "featureType": "road.local",
                            "elementType": "geometry",
                            "stylers": [{
                                "color": "#ffffff"
                            }, {
                                "lightness": 16
                            }]
                        }, {
                            "featureType": "poi",
                            "elementType": "geometry",
                            "stylers": [{
                                "color": "#f5f5f5"
                            }, {
                                "lightness": 21
                            }]
                        }, {
                            "featureType": "poi.park",
                            "elementType": "geometry",
                            "stylers": [{
                                "color": "#dedede"
                            }, {
                                "lightness": 21
                            }]
                        }, {
                            "elementType": "labels.text.stroke",
                            "stylers": [{
                                "visibility": "on"
                            }, {
                                "color": "#ffffff"
                            }, {
                                "lightness": 16
                            }]
                        }, {
                            "elementType": "labels.text.fill",
                            "stylers": [{
                                "saturation": 36
                            }, {
                                "color": "#333333"
                            }, {
                                "lightness": 40
                            }]
                        }, {
                            "elementType": "labels.icon",
                            "stylers": [{
                                "visibility": "off"
                            }]
                        }, {
                            "featureType": "transit",
                            "elementType": "geometry",
                            "stylers": [{
                                "color": "#f2f2f2"
                            }, {
                                "lightness": 19
                            }]
                        }, {
                            "featureType": "administrative",
                            "elementType": "geometry.fill",
                            "stylers": [{
                                "color": "#fefefe"
                            }, {
                                "lightness": 20
                            }]
                        }, {
                            "featureType": "administrative",
                            "elementType": "geometry.stroke",
                            "stylers": [{
                                "color": "#fefefe"
                            }, {
                                "lightness": 17
                            }, {
                                "weight": 1.2
                            }]
                        }]
                    }
                }
            });

        });

        /* ---------------------------------------------- /*
         * Scroll Animation
        /* ---------------------------------------------- */

        $('.anim-scroll').on('click', function(e) {
            var target = this.hash;
            var $target = $(target);
            $('html, body').stop().animate({
                'scrollTop': $target.offset().top
            }, 900, 'swing');
            e.preventDefault();
        });

        /* ---------------------------------------------- /*
         * Scroll top
        /* ---------------------------------------------- */

        $('a[href="#top"]').on('click', function() {
            $('html, body').animate({
                scrollTop: 0
            }, 'slow');
            return false;
        });

        /* ---------------------------------------------- /*
         * Ajax options
        /* ---------------------------------------------- */

        var pageNumber = 0,
            workNumberToload = 5;

        var doneText = 'Done',
            loadText = 'More works',
            loadingText = 'Loading...',
            errorText = 'Error! Check the console for more information.';

        /* ---------------------------------------------- /*
         * Ajax portfolio
        /* ---------------------------------------------- */

        $('#show-more').on('click', function() {
            $(this).text(loadingText);

            setTimeout(function() {
                ajaxLoad(workNumberToload, pageNumber);
            }, 300);

            pageNumber++;

            return false;
        });

        function ajaxLoad(workNumberToload, pageNumber) {
            var $loadButton = $('#show-more');
            var dataString = 'numPosts=' + workNumberToload + '&pageNumber=' + pageNumber;

            $.ajax({
                type: 'GET',
                data: dataString,
                dataType: 'html',
                url: 'assets/php/ajax-load-more.html',
                success: function(data) {
                    var $data = $(data);
                    var start_index = (pageNumber - 1) * workNumberToload;
                    var end_index = +start_index + workNumberToload;

                    if ($data.find('.work-item').slice(start_index).length) {
                        var work = $data.find('.work-item').slice(start_index, end_index);

                        worksgrid.append(work).isotope('appended', work).resize();

                        setTimeout(function() {
                            $loadButton.text(loadText);
                        }, 300);
                    } else {
                        setTimeout(function() {
                            $loadButton.text(doneText);
                        }, 300);

                        setTimeout(function() {
                            $('#show-more').animate({
                                opacity: 0,
                            }).css('display', 'none');
                        }, 1500);
                    }
                },

                error: function(jqXHR, textStatus, errorThrown) {
                    console.log(jqXHR + " :: " + textStatus + " :: " + errorThrown);

                    setTimeout(function() {
                        $loadButton.removeClass('ss-loading');
                        $loadButton.text(errorText);
                    }, 300);

                }
            });
        }

    });

})(jQuery);
