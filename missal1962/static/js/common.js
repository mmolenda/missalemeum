
const $window = $(window);
const $wrapper = $("div.wrapper");
const $main = $("main");
const $loadedContent = $("main div#loaded-content");
const $sidebarAndContent = $("#sidebar, #content");
const $buttonSidebarCollapse = $("button#sidebar-collapse");
const langSwithVernacular = "lang-switch-vernacular";
const $sidebar = $("nav#sidebar");
const $sidebarTools = $("div#sidebar-tools");
let cannotLoadMessage = "Nie udało się pobrać danych.";

// Making :contains case insensitive
$.expr[":"].contains = $.expr.createPseudo(function(arg) {
    return function( elem ) {
        return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };
});

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

class Loader {
    constructor() {
        this.loaderCounter = 0;
        this.loaderDiv = $("div#loader");
    }

    show() {
        if (this.loaderCounter === 0) {
            this.loaderDiv.fadeIn(300);
        }
        this.loaderCounter += 1;
    }

    hide() {
        this.loaderCounter -= 1;
        if (this.loaderCounter === 0) {
            this.loaderDiv.hide(0);
        }
    }
}

loader = new Loader();

function printContent(template, content) {
    let newWindow = window.open('','', "width=650, height=750");
    let newContent = renderTemplate(template, {main: content});
    newWindow.document.write(newContent);
    newWindow.document.close();
    newWindow.focus();
    return true;
}

function markSidebarItemActive(date) {
    $sidebar.find("li.sidebar-item").removeClass("active");
    let newActive = $("li#sidebar-item-" + date);
    newActive.addClass("active");

    let itemPosition = newActive.position().top;
    let sidebarPosition = Math.abs($sidebar.find("ul").position().top);

    if ((itemPosition > $sidebar.height() * 0.6) || itemPosition < $sidebarTools.height() * 1.5) {
        $sidebar.animate({scrollTop: sidebarPosition + itemPosition - 100}, 200);
    }
}

function filterSidebarItems(searchString, toggleSidebarItemCallback) {
    if (searchString === "") {
        let itemsAll = $sidebar.find("li.sidebar-item");
        itemsAll.show();
        toggleSidebarItemCallback();
    } else if (searchString.length > 2) {
        let itemsAll = $sidebar.find("li.sidebar-item");
        itemsAll.hide();
        $('li.sidebar-item div:contains("' + searchString + '")').parent().parent().show("fast");
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