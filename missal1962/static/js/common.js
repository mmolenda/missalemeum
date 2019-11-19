
const $window = $(window);
const $wrapper = $("div.wrapper");
const $main = $("main");
const $sidebarAndContent = $("#sidebar, #content");
const $buttonSidebarCollapse = $("button#sidebar-collapse");
const $loader = $("div#loader");
const langSwithVernacular = "lang-switch-vernacular";
let loaderCounter = 0;

/**
 * Render template, substitute placeholders with elements from `data` object.
 * Example:
 * ```render('<a href="${url}">x</a>', {"url": "http://foo.com"}) -> <a href="http://foo.com">x</a>
 * Idea from https://stackoverflow.com/a/39065147
 **/
function renderTemplate(template, data) {
    function _render(props) {
        return function (tok, i) {
            return (i % 2) ? props[tok] : tok;
        };
    }

    let parsedTpl = template.split(/\$\{(.+?)\}/g);
    return parsedTpl.map(_render(data)).join('');
}

/**
 * For large screens show both language columns adjacently.
 * For small screens show columns only for the language selected
 * in `#lang-switch`
 **/
function adaptSectionColumns() {
    if ($window.width() >= 576) {
        $("div.section-vernacular").show();
        $("div.section-latin").show();
    } else {
        let langId = $("#lang-switch>label.active>input").attr("id");
        if (langId == langSwithVernacular) {
            $("div.section-vernacular").show();
            $("div.section-latin").hide();
        } else {
            $("div.section-vernacular").hide();
            $("div.section-latin").show();
        }
    }
}

/**
 * Switch between lang versions on small screens, where the switch is visible
 **/
function toggleLangSections(id) {
    if (id === langSwithVernacular) {
        $("div.section-vernacular").show();
        $("div.section-latin").hide();
    } else {
        $("div.section-vernacular").hide();
        $("div.section-latin").show();
    }
}

function navbarIsCollapsed() {
    return $buttonSidebarCollapse.is(":visible");
}

function showLoader() {
    if (loaderCounter === 0) {
        $loader.fadeIn("slow");
    }
    loaderCounter += 1;
}

function hideLoader() {
    loaderCounter -= 1;
    if (loaderCounter === 0) {
        $loader.hide();
    }
}

$window.on("load", function () {
    /**
     * Toggle sidebar on hamburger menu click ..
     **/
    $("#sidebar-collapse").on("click", function () {
        $sidebarAndContent.toggleClass("active");
    });

    /**
     * .. and on swipe ..
     **/
    let sidebarTouchXPos = 0;
    $wrapper.on("touchstart", function (e) {
        sidebarTouchXPos = e.originalEvent.touches[0].pageX;
    }).on("touchend", function (e) {
        if (navbarIsCollapsed()) {
            if ((sidebarTouchXPos - e.originalEvent.changedTouches[0].pageX > 80 && $sidebarAndContent.hasClass("active")) ||
                (sidebarTouchXPos - e.originalEvent.changedTouches[0].pageX < -80 && !$sidebarAndContent.hasClass("active"))) {
                $sidebarAndContent.toggleClass("active");
            }
        }
    });

    /**
     * .. and close it on touch in the main area in small view
     **/
    $main.on("touchstart", function (e) {
        if (navbarIsCollapsed()) {
            $sidebarAndContent.removeClass("active");
        }
    });

});