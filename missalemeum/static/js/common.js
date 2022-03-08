
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

const $templateProperTabs = $("#template-proper-tabs").text();
const $templateProperTab = $("#template-proper-tab").text();
const $templateProperActiveTab = $("#template-proper-active-tab").text();
const $templateProperTabsContent = $("#template-proper-tabs-content").text();
const $templateProperTabContent = $("#template-proper-tab-content").text();
const $templateProperActiveTabContent = $("#template-proper-active-tab-content").text();

const $templateContentIntro = $("#template-content-intro").text();
const $templateContentSupplementList = $("#template-content-supplement-list").text();
const $templateContentSupplementItemInternal = $("#template-content-supplement-item-internal").text();
const $templateContentSupplementItemExternal = $("#template-content-supplement-item-external").text();
const $templateContentColumnsLabel = $("#template-content-columns-label").text();
const $templateContentColumnsBody = $("#template-content-columns-body").text();
const $templateContentNoColumns = $("#template-content-nocolumns").text();
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

function markSidebarItemActive(resourceId) {
    resourceId = resourceId.replace("/", "-");
    $sidebar.find("li.sidebar-item").removeClass("active");
    let newActive = $("li#sidebar-item-" + resourceId);

    if (newActive.length !== 0) {
        newActive.addClass("active");
        let itemPosition = newActive.position().top;
        let sidebarPosition = Math.abs($sidebar.find("ul").position().top);

        if ((itemPosition > $sidebar.height() * 0.6) || itemPosition < $sidebarTools.height() * 1.5) {
            $sidebar.animate({scrollTop: sidebarPosition + itemPosition - 100}, 200);
        }
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
            let properTabsContent = $(renderTemplate($templateProperTabsContent));
            let properTabs = $(renderTemplate($templateProperTabs));
            window.scrollTo(0, 0);

            $.each(data, function (index, item) {
                let info = item["info"];
                let title = info.title;
                let description = info.description;
                let supplements = info.supplements;
                let sections = item.sections;
                let colors = info.colors;
                let colorMarkers = '';
                $.each(colors, function (i, color) {
                    colorMarkers += renderTemplate($templateColorMarker, {color: color});
                });
                let additional_info = [];
                let date = info.date;
                if (date !== undefined) {
                    let parsedDate = moment(date, "YYYY-MM-DD");
                    additional_info.push(parsedDate.format("dd DD.MM.YYYY"));
                }
                let mappedRank = self.mapRank(info.rank);
                if (mappedRank !== undefined) {
                    additional_info.push(mappedRank);
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

                let properTab;
                let properTabContent;
                if (index === 0) {
                    properTab = $(renderTemplate($templateProperActiveTab, {index: index, title:title}));
                    properTabContent = $(renderTemplate($templateProperActiveTabContent, {index: index}));
                } else {
                    properTab = $(renderTemplate($templateProperTab, {index: index, title:title}));
                    properTabContent = $(renderTemplate($templateProperTabContent, {index: index}));
                }
                properTab.appendTo(properTabs.find("div.dropdown-menu"));

                $(renderTemplate($templateContentIntro, {
                    title: title,
                    color_markers: colorMarkers,
                    additional_info: additional_info.join('</em> | <em class="rubric">'),
                    description: description.split("\n").join("<br />")
                })).appendTo(properTabContent);

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
                    supplementsList.appendTo(properTabContent);
                }

                $.each(sections, function(i, section) {
                    $(renderTemplate($templateContentColumnsLabel, {
                        labelVernacular: section.label,
                        labelLatin: section.id,
                    })).appendTo(properTabContent);
                    $.each(section.body, function(i, paragraph) {
                        if (paragraph.length === 2) {
                            $(renderTemplate($templateContentColumnsBody, {
                                sectionVernacular: self.htmlify(paragraph[0]),
                                sectionLatin: self.htmlify(paragraph[1])
                            })).appendTo(properTabContent);
                        } else {
                            $(renderTemplate($templateContentNoColumns, {
                                text: self.htmlify(paragraph[0])
                            })).appendTo(properTabContent);
                        }
                    });
                });
                properTabContent.appendTo(properTabsContent);
            });
            if (data.length > 1) {
                properTabs.appendTo($loadedContent);
            }
            properTabsContent.appendTo($loadedContent);
        }).done(function () {
            loadedResource = resourceId;
            if (isHistoryReplace === true) {
                window.history.replaceState({resourceId: resourceId}, '', '/' + self.urlPart + '/' + resourceId);
            } else {
                window.history.pushState({resourceId: resourceId}, '', '/' + self.urlPart + '/' + resourceId);
            }
            document.title = titles[0] + " | " + "Missale Meum";
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

    htmlify(text) {
        return text.replace(/\*([^\*]+)\*/g, "<em>$1</em>").split("\n").join("<br />");
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