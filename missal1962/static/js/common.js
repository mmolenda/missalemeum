
const $window = $(window);
const $wrapper = $("div.wrapper");
const $main = $("main");
const $loadedContent = $("main div#loaded-content");
const $sidebarAndContent = $("#sidebar, #content");
const $buttonSidebarCollapse = $("button#sidebar-collapse");
const langSwithVernacular = "lang-switch-vernacular";
const $sidebar = $("nav#sidebar");
const $sidebarTools = $("div#sidebar-tools");

const $templateSidebarCalendarItem = $("#template-sidebar-item").text();
const $templateSidebarCalendarItemYear = $("#template-sidebar-item-year").text();
const $templateContent = $("#template-content").text();
const $templateContentIntro = $("#template-content-intro").text();
const $templateContentSupplementList = $("#template-content-supplement-list").text();
const $templateContentSupplementItemInternal = $("#template-content-supplement-item-internal").text();
const $templateContentSupplementItemExternal = $("#template-content-supplement-item-external").text();
const $templateContentColumns = $("#template-content-columns").text();
const $templateContentPrint = $("#template-content-print").text();
const $templateColorMarker = $("#template-color-marker").text();
const $searchInput = $("input#search-input");

let loadedResource;
let selectedResource;
let textFeria = "Feria";

// Making :contains case insensitive
$.expr[":"].contains = $.expr.createPseudo(function(arg) {
    return function( elem ) {
        return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };
});


function setResourceId(resourceId) {
    selectedResource = resourceId;
}

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
        if (langId === langSwithVernacular) {
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

/**
 * Obtain a proper for the given `date` through AJAX call and populate
 * the main element with Bootstrap grid.
 * Once populated, mark corresponding element in the sidebar as active and select given date in the datepicker.
 **/
class ProperContentLoader {

    constructor(apiEndpoint, urlPart, doneCallback) {
        this.apiEndpoint = apiEndpoint;
        this.urlPart = urlPart;
        this.doneCallback = doneCallback;
    }

    load(resourceId, isHistoryReplace) {
        let self = this;
        if (loadedResource === resourceId) {
            return;
        }
        loader.show();
        let titles = [];
        $.getJSON(self.apiEndpoint + resourceId, function (data) {
            $loadedContent.empty();
            window.scrollTo(0, 0);

            $.each(data, function (index, item) {
                let info = item["info"];
                let title = info.title;
                let description = info.description;
                let supplements = info.supplements;
                let sectionsVernacular = item.proper_vernacular;
                let sectionsLatin = item.proper_latin;
                let colors = info.colors;
                let colorMarkers = '';
                $.each(colors, function (i, color) {
                    colorMarkers += renderTemplate($templateColorMarker, {color: color});
                });
                let additional_info = [];
                let date = info.date;
                if (date !== undefined) {
                    let parsedDate = moment(date, "YYYY-MM-DD");
                    additional_info.push(parsedDate.format("dd DD.MM.YYYY"), self.mapRank(info.rank));
                }
                if (info.tempora != null) {
                    additional_info.push(info.tempora);
                }
                if (info.additional_info != null) {
                    $.merge(additional_info, info.additional_info);
                }

                if (title == null) {
                    title = textFeria;
                }
                titles.push(title);
                $(renderTemplate($templateContentIntro, {
                    title: title,
                    color_markers: colorMarkers,
                    additional_info: additional_info.join('</em> | <em class="rubric">'),
                    description: description.split("\n").join("<br />")
                })).appendTo($loadedContent);

                if (supplements !== undefined && supplements.length > 0) {
                    let supplementsList = $(renderTemplate($templateContentSupplementList, {}));
                    $.each(supplements, function (index, supplement) {
                        let template;
                        if (supplement.path, supplement.path.valueOf().startsWith("http")) {
                            template = $templateContentSupplementItemExternal;
                        } else {
                            template = $templateContentSupplementItemInternal;
                        }
                        $(renderTemplate(template, {
                            path: supplement.path,
                            label: supplement.label,
                            resourceId: resourceId
                        })).appendTo(supplementsList);
                        if (index + 1 < supplements.length) {
                            supplementsList.append(",&nbsp;&nbsp;");
                        }
                    });
                    supplementsList.appendTo($loadedContent);
                }

                $.each([sectionsVernacular, sectionsLatin], function (i, sections) {
                    // replacing all surrounding asterisks with surrounding <em>s in body
                    $.each(sections, function (x, y) {
                        sections[x].body = y.body.replace(/\*([^\*]+)\*/g, "<em>$1</em>")
                    })

                });
                for (let i = 0; i < sectionsVernacular.length; i++) {
                    let sectionVernacular = sectionsVernacular[i];
                    let sectionLatin = sectionsLatin[i];
                    if (sectionLatin == null) {
                        sectionLatin = {label: "", body: ""};
                        console.error("Latin sections missing in " + date);
                    }
                    $(renderTemplate($templateContentColumns, {
                        labelVernacular: sectionVernacular.label,
                        sectionVernacular: sectionVernacular.body.split("\n").join("<br />"),
                        labelLatin: sectionLatin.label,
                        sectionLatin: sectionLatin.body.split("\n").join("<br />")
                    })).appendTo($loadedContent);
                }
            });
        }).done(function () {
            loadedResource = resourceId;
            if (isHistoryReplace === true) {
                window.history.replaceState({resourceId: resourceId}, '', '/' + self.urlPart + '/' + resourceId);
            } else {
                window.history.pushState({resourceId: resourceId}, '', '/' + self.urlPart + '/' + resourceId);
            }
            document.title = titles[0] + " | " + resourceId + " | " + "Missale Meum";
            if (navbarIsCollapsed()) {
                $sidebarAndContent.removeClass("active");
            }
            adaptSectionColumns();
            self.doneCallback();
        }).fail(function () {
            alert(config.translation.cannotLoadMessage);
        }).always(function () {
            loader.hide();
        });
    }

    mapRank(rank) {
        return {1: config.translation.class1,
            2: config.translation.class2,
            3: config.translation.class3,
            4: config.translation.class4}[rank]
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