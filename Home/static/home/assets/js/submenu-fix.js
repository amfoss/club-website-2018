(function($){

	$(document).ready(function() {

		/* ---------------------------------------------- /*
		 * Mobile detect
		/* ---------------------------------------------- */

		var mobileTest;

		if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
			mobileTest = true;
		} else {
			mobileTest = false;
		}

		/* ---------------------------------------------- /*
		 * Navbar submenu
		/* ---------------------------------------------- */

		$(window).on('resize', function() {

			var width = Math.max($(window).width(), window.innerWidth);

			if (width > 991) {
				$('.navbar-custom .navbar-nav > li.dropdown').hover(function() {
					var menuLeftOffset  = $('.dropdown-menu', $(this)).offset().left;
					var
						maxWidth1    = 0,
						maxWidth2    = 0,
						menuLevelOne = $(this).children('.dropdown-menu'),
						menuLevelTwo = $('.dropdown-menu', menuLevelOne),
						menuLevelOneWidth,
						menuLevelTwoWidth;

					menuLevelOne.each(function() {
						if ($(this).width() > maxWidth1) {
							menuLevelOneWidth = $(this).width();
						}
					});

					menuLevelTwo.each(function() {
						if ($(this).width() > maxWidth2) {
							menuLevelTwoWidth = $(this).width();
						}
					});

					if (typeof menuLevelTwoWidth === 'undefined') {
						menuLevelTwoWidth = 0;
					}

					if (width - menuLeftOffset - menuLevelOneWidth < menuLevelOneWidth + 20) {
						$(this).children('.dropdown-menu').addClass('leftauto');

						if (menuLevelTwo.length > 0) {
							if (width - menuLeftOffset - menuLevelOneWidth < menuLevelTwoWidth + 20) {
								menuLevelTwo.addClass('left-side');
							} else {
								menuLevelTwo.removeClass('left-side');
							}
						}
					} else {
						$(this).children('.dropdown-menu').removeClass('leftauto');
					}
				});
			}
		}).resize();

		/* ---------------------------------------------- /*
		 * Navbar hover dropdown on desktop
		/* ---------------------------------------------- */

		$(window).on('resize', function() {

			var width = Math.max($(window).width(), window.innerWidth);

			if ((width > 991) && (mobileTest !== true)) {

				$('.navbar-custom .navbar-nav > li.dropdown, .navbar-custom li.dropdown > ul > li.dropdown').removeClass('open');

				var delay = 0;
				var setTimeoutConst;

				$('.navbar-custom .navbar-nav > li.dropdown, .navbar-custom li.dropdown > ul > li.dropdown').hover(function() {
					var $this = $(this);
					setTimeoutConst = setTimeout(function() {
						$this.addClass('open');
						$this.find('.dropdown-toggle').addClass('disabled');
					}, delay);
				},
				function() {
					clearTimeout(setTimeoutConst);
					$(this).removeClass('open');
					$(this).find('.dropdown-toggle').removeClass('disabled');
				});
			} else {
				$('.navbar-custom .navbar-nav > li.dropdown, .navbar-custom li.dropdown > ul > li.dropdown').unbind('mouseenter mouseleave');
				$('.navbar-custom [data-toggle=dropdown]').not('.binded').addClass('binded').on('click', function(event) {
					event.preventDefault();
					event.stopPropagation();
					$(this).parent().siblings().removeClass('open');
					$(this).parent().siblings().find('[data-toggle=dropdown]').parent().removeClass('open');
					$(this).parent().toggleClass('open');
				});
			}

		}).resize();

	});

})(jQuery);