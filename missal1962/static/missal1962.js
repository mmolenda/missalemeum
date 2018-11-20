

$(document).ready(function()    {

    /**
     *
     * Globals
     *
    **/

    // Making :contains case insensitive
    $.expr[":"].contains = $.expr.createPseudo(function(arg) {
        return function( elem ) {
            return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
        };
    });

    const templateSidebarCalendarItem = $("#template-sidebar-calendar-item").text();
    const templateSidebarCalendarItemYear = $("#template-sidebar-calendar-item-year").text();
    const templateContentIntro = $("#template-content-intro").text();
    const templateContentColumns = $("#template-content-columns").text();

    function init() {
        moment.locale("pl");
        loadProper(getDate());
        adaptSectionColumns();
    }

    init();

    /**
     *
     * Functions
     *
     **/

    /**
      * Obtain date from url hash or use today date if not provided or invalid.
     **/
    function getDate() {
        let tmpDate = document.location.hash.replace("#", "");
        tmpDate = moment(tmpDate, "YYYY-MM-DD");
        if (! tmpDate.isValid()) {
            tmpDate = moment();
        }
        return tmpDate.format("YYYY-MM-DD");
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
      * Obtain calendar for the year specified in `date` through AJAX call and populate
      * the sidebar with <li> elements.
      * Once populated, fire the callback function to activate selected item and clear the search input.
     **/
    function loadPropersSidebar(date, markItemActiveCallback) {
        let year = date.split("-")[0];
        $.getJSON( calendarEndpoint + year, function( data ) {
            let sidebar = $("nav#sidebar>ul");
            sidebar.empty();

            let prevYear = parseInt(year) - 1;
            let prevYearLastDay = prevYear + "-12-31";
            $(renderTemplate(templateSidebarCalendarItemYear, {
                date: prevYearLastDay,
                year: prevYear
            })).appendTo(sidebar);

            $.each(data, function(date, day) {
                let additional_info = [date];
                let celebration;
                if (day.celebration.length > 0) {
                    celebration = day.celebration[0].title;
                } else {
                    celebration = moment(date, "YYYY-MM-DD").format("DD MMMM");
                }
                if (day.tempora.length > 0 && day.tempora[0].title != celebration) {
                    additional_info.push(day.tempora[0].title);
                }

                $(renderTemplate(templateSidebarCalendarItem, {
                    date: date,
                    celebration: celebration,
                    additional_info: additional_info.join(" | ")
                })).appendTo(sidebar);


            });

            let nextYear = parseInt(year) + 1;
            let nextYearFirstDay = nextYear + "-01-01";
            $(renderTemplate(templateSidebarCalendarItemYear, {
                date: nextYearFirstDay,
                year: nextYear
            })).appendTo(sidebar);

            markItemActiveCallback(date);
            $("input#search-input").attr("placeholder", "Szukaj w " + year + "...");
        });
    }

    /**
      * Obtain a proper for the given `date` through AJAX call and populate
      * the main element with Bootstrap grid.
      * Once populated, mark corresponding element in the sidebar as active and select given date in the datepicker.
     **/
    function loadProper(date) {
        $.getJSON( dateEndpoint + date, function( data ) {
            let title = data["info"].title;
            let description = data["info"].description;
            let sectionsVernacular = data.proper_vernacular;
            let sectionsLatin = data.proper_latin;
            let additional_info = [data["info"].date];
            if (data["info"].tempora != null) {
                additional_info.push(data["info"].tempora);
            }
            if (data["info"].additional_info != null) {
                $.merge(additional_info, data["info"].additional_info);
            }

            let main = $("main");
            main.empty();
            window.scrollTo(0, 0);

            if (title == null) {
                title = moment(data["info"].date, "YYYY-MM-DD").format("DD MMMM");
            }
            $(renderTemplate(templateContentIntro, {
                title: title,
                additional_info: additional_info.join('</em> | <em class="rubric">'),
                description: description
            })).appendTo(main);

            $.each([sectionsVernacular, sectionsLatin], function(i, sections) {
                $.each(sections, function(x, y) {sections[x].body = y.body.replace(/\*([^\*]+)\*/g, "<em>$1</em>")})

            });
            for (let i = 0; i < sectionsVernacular.length; i++) {
                $(renderTemplate(templateContentColumns, {
                    labelVernacular: sectionsVernacular[i].label,
                    sectionVernacular: sectionsVernacular[i].body.split("\n").join("<br />"),
                    labelLatin: sectionsLatin[i].label,
                    sectionLatin: sectionsLatin[i].body.split("\n").join("<br />")
                })).appendTo(main);
            }
            togglePropersSidebarItem(date);
            $("#datetimepicker4").datetimepicker("date", date);
        });
    }

    /**
      * Mark sidebar element for given `date` as active. If an element is not present, reload the sidebar
      * with data for proper year.
     **/
    function togglePropersSidebarItem(date) {
        function markItemActive(date) {
            $("nav#sidebar li.sidebar-calendar-item").removeClass("active");
            let newActive = $("li#sidebar-calendar-item-" + date);
            newActive.addClass("active");
            let sidebar = $("nav#sidebar");

            let itemPosition = newActive.position().top;
            let sidebarPosition = Math.abs(sidebar.find("ul").position().top);

            if (Math.abs(itemPosition) > sidebar.height() * 0.6) {
                sidebar.animate({scrollTop: sidebarPosition + itemPosition - 100}, 200);
            }
        }

        let newActive = $("li#sidebar-calendar-item-" + date);
        if (newActive.length == 0) {
            loadPropersSidebar(date, markItemActive);
        } else {
            markItemActive(date);
        }
    }

    /**
      * For large screens show both language columns adjacently.
      * For small screens show columns only for the language selected
      * in `#lang-switch`
     **/
    function adaptSectionColumns() {
        if ($(window).width() >= 576) {
            $("div.section-vernacular").show();
            $("div.section-latin").show();
        } else {
            let langId = $("#lang-switch>label.active>input").attr("id");
            if (langId == "lang-switch-vernacular") {
                $("div.section-vernacular").show();
                $("div.section-latin").hide();
            } else {
                $("div.section-vernacular").hide();
                $("div.section-latin").show();
            }
        }
    }

    /**
     *
     * Bindings
     *
     **/

    $(window).on("resize", function(){
        adaptSectionColumns();
    });

    $(window).on("hashchange", function() {
        loadProper(getDate());
    });

    $("#datetimepicker4").datetimepicker({
        format: "YYYY-MM-DD",
        useCurrent: false,
        locale: "pl",
        widgetPositioning: {
            horizontal: "right",
            vertical: "bottom"
        }
    });

    $("#datetimepicker4 input").on("input", function () {
        document.location.hash = this.value;
        // clear the search input after choosing the date
        $("input#search-input").val("").trigger("input");
    });

    $("#sidebar-collapse").on("click", function () {
        $("#sidebar, #content").toggleClass("active");
    });

    $("input#search-input").on("input", function () {
        let searchString = $(this).val();
        if (searchString === "") {
            let itemsAll = $(".sidebar-calendar-item");
            itemsAll.show();
            togglePropersSidebarItem(getDate());
        } else if (searchString.length > 2) {
            let itemsAll = $(".sidebar-calendar-item");
            itemsAll.hide();
            $('li.sidebar-calendar-item div:contains("' + searchString + '")').parent().parent().show("fast");
        }
    });

    $("#search-clear").on("click", function () {
        $("input#search-input").val("").trigger("input");
    });

    $("input[type=radio][name=lang-switch]").change(function() {
        if (this.id == "lang-switch-vernacular") {
            $("div.section-vernacular").show();
            $("div.section-latin").hide();
        } else {
            $("div.section-vernacular").hide();
            $("div.section-latin").show();
        }
    });
});
