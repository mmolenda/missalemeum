

$(window).on("load", function () {

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
    const templateContentPrint = $("#template-content-print").text();

    const $window = $(window);
    const $sidebar = $("nav#sidebar");
    const $main = $("main");
    const $sidebarAndContent = $("#sidebar, #content");
    const $datetimepicker4 = $("#datetimepicker4");
    const $searchInput = $("input#search-input");
    const $sidebarTools = $("div#sidebar-tools");

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
      * Obtain calendar for the year specified in `date` through AJAX call and populate
      * the sidebar with <li> elements.
      * Once populated, fire the callback function to activate selected item and clear the search input.
     **/
    function loadSidebar(date, markItemActiveCallback) {
        showLoader();
        let year = date.split("-")[0];
        $.getJSON( config.calendarEndpoint + year, function( data ) {
            let sidebarUl = $sidebar.find("ul");
            sidebarUl.empty();

            let prevYear = parseInt(year) - 1;
            let prevYearLastDay = prevYear + "-12-31";
            if (prevYearLastDay >= $datetimepicker4.datetimepicker("minDate")._i) {
                $(renderTemplate(templateSidebarCalendarItemYear, {
                    date: prevYearLastDay,
                    year: prevYear
                })).appendTo(sidebarUl);
            }

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
                })).appendTo(sidebarUl);


            });

            let nextYear = parseInt(year) + 1;
            let nextYearFirstDay = nextYear + "-01-01";
            if (nextYearFirstDay <= $datetimepicker4.datetimepicker("maxDate")._i) {
                $(renderTemplate(templateSidebarCalendarItemYear, {
                    date: nextYearFirstDay,
                    year: nextYear
                })).appendTo(sidebarUl);
            }

            markItemActiveCallback(date);
            $searchInput.attr("placeholder", "Szukaj w " + year + "...");
            hideLoader();
        });
    }

    /**
      * Obtain a proper for the given `date` through AJAX call and populate
      * the main element with Bootstrap grid.
      * Once populated, mark corresponding element in the sidebar as active and select given date in the datepicker.
     **/
    function loadProper(date) {
        showLoader();
        $.getJSON( config.dateEndpoint + date, function( data ) {
            $main.empty();
            window.scrollTo(0, 0);

            $.each(data, function(index, item) {
                let title = item["info"].title;
                let description = item["info"].description;
                let sectionsVernacular = item.proper_vernacular;
                let sectionsLatin = item.proper_latin;
                let additional_info = [item["info"].date, mapRank(item["info"].rank)];
                if (item["info"].tempora != null) {
                    additional_info.push(item["info"].tempora);
                }
                if (item["info"].additional_info != null) {
                    $.merge(additional_info, item["info"].additional_info);
                }

                if (title == null) {
                    title = moment(item["info"].date, "YYYY-MM-DD").format("DD MMMM");
                }
                $(renderTemplate(templateContentIntro, {
                    title: title,
                    additional_info: additional_info.join('</em> | <em class="rubric">'),
                    description: description.split("\n").join("<br />")
                })).appendTo($main);

                $.each([sectionsVernacular, sectionsLatin], function(i, sections) {
                    // replacing all surrounding asterisks with surrounding <em>s in body
                    $.each(sections, function(x, y) {sections[x].body = y.body.replace(/\*([^\*]+)\*/g, "<em>$1</em>")})

                });
                for (let i = 0; i < sectionsVernacular.length; i++) {
                    let sectionVernacular = sectionsVernacular[i];
                    let sectionLatin = sectionsLatin[i];
                    if (sectionLatin == null) {
                        sectionLatin = {label: "", body: ""};
                        console.error("Latin sections missing in " + date);
                    }
                    $(renderTemplate(templateContentColumns, {
                        labelVernacular: sectionVernacular.label,
                        sectionVernacular: sectionVernacular.body.split("\n").join("<br />"),
                        labelLatin: sectionLatin.label,
                        sectionLatin: sectionLatin.body.split("\n").join("<br />")
                    })).appendTo($main);
                }
            });
            toggleSidebarItem(date);
            $datetimepicker4.datetimepicker("date", date);
            if (navbarIsCollapsed()) {
                $sidebarAndContent.removeClass("active");
            }
            hideLoader();
        });
    }

    /**
      * Mark sidebar element for given `date` as active. If an element is not present, reload the sidebar
      * with the data for proper year.
     **/
    function toggleSidebarItem(date) {
        function markItemActive(date) {
            $sidebar.find("li.sidebar-calendar-item").removeClass("active");
            let newActive = $("li#sidebar-calendar-item-" + date);
            newActive.addClass("active");

            let itemPosition = newActive.position().top;
            let sidebarPosition = Math.abs($sidebar.find("ul").position().top);

            if ((itemPosition > $sidebar.height() * 0.6) || itemPosition < $sidebarTools.height() * 1.5) {
                $sidebar.animate({scrollTop: sidebarPosition + itemPosition - 100}, 200);
            }
        }

        let newActive = $("li#sidebar-calendar-item-" + date);
        if (newActive.length == 0) {
            loadSidebar(date, markItemActive);
        } else {
            markItemActive(date);
        }
    }

    function mapRank(rank) {
        return {1: '1 klasy', 2: '2 klasy', 3: '3 klasy', 4: '4 klasy'}[rank]
    }

    /**
      *
      * Bindings
      *
     **/

    $window.on("resize", function(){
        adaptSectionColumns();
    });

    $window.on("hashchange", function() {
        loadProper(getDate());
    });

    $datetimepicker4.datetimepicker({
        format: "YYYY-MM-DD",
        minDate: config.minDate,
        maxDate: config.maxDate,
        useCurrent: false,
        locale: "pl",
        widgetPositioning: {
            horizontal: "right",
            vertical: "bottom"
        }
    });

    /**
     * When the date is selected from datepicker update url hash and clear the search input
     **/
    $datetimepicker4.find("input").on("input", function () {
        document.location.hash = this.value;
        $searchInput.val("").trigger("input");
    });

    /**
     * filter out the elements in the sidebar;
     * start filtering from 3 characters on;
     * show all elements on empty input
     **/
    $searchInput.on("input", function () {
        let searchString = $(this).val();
        if (searchString === "") {
            let itemsAll = $sidebar.find("li.sidebar-calendar-item");
            itemsAll.show();
            toggleSidebarItem(getDate());
        } else if (searchString.length > 2) {
            let itemsAll = $sidebar.find("li.sidebar-calendar-item");
            itemsAll.hide();
            $('li.sidebar-calendar-item div:contains("' + searchString + '")').parent().parent().show("fast");
        }
    });

    /**
     * X button in the search input clears current search
     **/
    //
    $("#search-clear").on("click", function () {
        $searchInput.val("").trigger("input");
    });

    /**
     * Switch between lang versions on small screens, where the switch is visible
     **/
    $("input[type=radio][name=lang-switch]").change(function() {
        toggleLangSections(this);
    });

    $("#print").on("click", function () {
        let newWindow = window.open('','', "width=650, height=750");
        let newContent = renderTemplate(templateContentPrint, {main: $main.html()});
        newWindow.document.write(newContent);
        newWindow.document.close();
        newWindow.focus();
        return true;
    });
});
